from dataclasses import replace
from decimal import Decimal
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5
import unittest
from unittest.mock import patch

from deal_or_no_deal_ai.storage import StateSnapshot


ROOT = Path(__file__).resolve().parents[1]


def uid(name):
    return str(uuid5(NAMESPACE_URL, "educational-test:" + name))


def snapshot(**changes):
    value = StateSnapshot(
        workspace_id=uid("workspace"), deal_id=uid("deal"), review_id=uid("review"),
        run_id=uid("run"), thread_id=uid("thread"), input_revision=1,
        confidence=Decimal("0.699999999999999999999999"),
        financial_inputs={"cash_available_for_debt_service": Decimal("-50000"),
                          "prior_ranking_liens": Decimal("0"), "net_income": None},
        risk_score=Decimal("25.000001"), source_text="Synthetic source: café; USD; \u2212; page 2",
        references=["P2", "rule:v1"], conditions=["First", "Second"],
        panel_refs=["panel:financial"], report_markdown="Historical report",
    )
    return replace(value, **changes)


class OfflineTest(unittest.TestCase):
    def setUp(self):
        super().setUp()
        def denied(*args, **kwargs):
            raise AssertionError("OUTBOUND_NETWORK_FORBIDDEN_IN_APPLICATION_TESTS")
        for target in ("socket.socket.connect", "socket.socket.connect_ex",
                       "socket.create_connection", "socket.getaddrinfo"):
            guard = patch(target, denied)
            guard.start()
            self.addCleanup(guard.stop)
        for key in ("LANGCHAIN_TRACING_V2", "LANGSMITH_TRACING"):
            guard = patch.dict("os.environ", {key: "false"})
            guard.start()
            self.addCleanup(guard.stop)
