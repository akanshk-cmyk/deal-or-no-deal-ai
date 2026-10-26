"""Real saver/interrupt checks for TEST-008-04/07, TEST-011-03/04.

Requires actual LangGraph/SQLite saver dependencies. Never substitutes a fake
saver, skips a missing dependency or claims this test graph is a deal workflow.
"""

from dataclasses import asdict, replace
from pathlib import Path
import sqlite3
import tempfile
from typing import TypedDict

from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.review import (
    AcceptedReview, Actor, PendingReview, accept_review, consume_own_receipt,
)
from deal_or_no_deal_ai.storage import RecordWrite, Store, decode_state, encode_state
from tests.support import OfflineTest, snapshot, uid


class CompatibilityState(TypedDict):
    snapshot: dict
    resumed_operation_id: str | None


def compile_test_graph(store, connection):
    def human(state):
        signal = interrupt({"request_id": uid("pending"), "kind": "APPLICATION_TEST"})
        saved_request = store.get_record("pending")[1]
        request = PendingReview(**{**saved_request, "requirements": ()})
        saved_disposition = store.get_record("disposition")[1]
        accepted = AcceptedReview(**{**saved_disposition,
                                     "condition_target_refs": tuple(saved_disposition["condition_target_refs"])})
        if signal != {"operation_id": accepted.operation_id}:
            raise InputError("WRONG_RESUME_OPERATION")
        consume_own_receipt(request, accepted)
        # Force typed restoration before any dependent use.
        restored = decode_state(state["snapshot"])
        return {"snapshot": encode_state(restored), "resumed_operation_id": accepted.operation_id}

    builder = StateGraph(CompatibilityState)
    builder.add_node("human", human)
    builder.add_edge(START, "human")
    builder.add_edge("human", END)
    serializer = JsonPlusSerializer(pickle_fallback=False,
        allowed_json_modules=None, allowed_msgpack_modules=None)
    return builder.compile(checkpointer=SqliteSaver(connection, serde=serializer))


class CheckpointCompatibilityTests(OfflineTest):
    def test_restart_and_own_receipt_with_or_without_pre_resume_crash_gap(self):
        for crash_gap in (False, True):
            with self.subTest(crash_gap=crash_gap), tempfile.TemporaryDirectory() as folder:
                path = Path(folder) / "shared.sqlite3"
                store = Store(path); store.initialize()
                current = PendingReview(uid("pending"), uid("workspace"), uid("deal"),
                    uid("thread"), 1, "test-analytical-basis", 1, "NORMAL", ())
                store.put_record(RecordWrite("pending", "TEST_REVIEW_REQUEST", asdict(current)))
                scope = {"workspace_id": uid("workspace"), "deal_id": uid("deal"), "review_id": uid("review")}
                initial = store.admit(uid("start"), scope, {"action": "TEST_START"})
                config = {"configurable": {"thread_id": uid("thread")}}
                original = snapshot()
                connection = sqlite3.connect(path, check_same_thread=False)
                try:
                    store.assert_claim(initial)
                    graph = compile_test_graph(store, connection)
                    result = graph.invoke({"snapshot": encode_state(original), "resumed_operation_id": None}, config)
                    self.assertIn("__interrupt__", result)
                    self.assertEqual(graph.get_state(config).next, ("human",))
                finally:
                    connection.close()
                store.release(initial, confirmed_idle=True)

                actor = Actor("AuthorizedApprover", uid("workspace"), frozenset({uid("deal")}), frozenset({"NORMAL"}))
                accepted = accept_review(current, actor, uid("resume"), "Approve",
                    expected_basis=current.analytical_basis_digest, expected_gate_version=1)
                recorded = replace(current, state="RECORDED", recorded_operation_id=accepted.operation_id)
                receipt = store.admit(accepted.operation_id, scope, {"action": "TEST_RESUME"}, writes=(
                    RecordWrite("pending", "TEST_REVIEW_REQUEST", asdict(recorded), 1),
                    RecordWrite("disposition", "TEST_DISPOSITION", asdict(accepted)),
                ))
                if crash_gap:
                    # Acceptance committed; graph progress not yet written.
                    store.mark_unknown(receipt)
                    store = Store(path); store.initialize()
                    store.reconcile_idle(receipt, evidence_ref="test:no-graph-work-dispatched",
                                         administrator_authorized=True)
                    receipt = store.admit(uid("explicit-recovery"), scope,
                                          {"action": "TEST_LOCAL_GRAPH_RECOVERY", "accepted_operation_id": accepted.operation_id})
                connection = sqlite3.connect(path, check_same_thread=False)
                try:
                    store.assert_claim(receipt)
                    graph = compile_test_graph(store, connection)
                    self.assertEqual(decode_state(graph.get_state(config).values["snapshot"]), original)
                    result = graph.invoke(Command(resume={"operation_id": accepted.operation_id}), config)
                    self.assertEqual(graph.get_state(config).next, ())
                    self.assertEqual(result["resumed_operation_id"], accepted.operation_id)
                    self.assertEqual(decode_state(result["snapshot"]), original)
                    self.assertEqual(store.get_record("disposition")[0], 1)
                finally:
                    connection.close()
                store.release(receipt, confirmed_idle=True)
