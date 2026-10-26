"""Explicit offline registered-page DIRECT/KEYWORD comparison and native ID metrics."""
from dataclasses import asdict
from pathlib import Path
import json
import sys
from hashlib import sha256
from uuid import uuid4
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from deal_or_no_deal_ai.context import fingerprint
from deal_or_no_deal_ai.services import load_registered_case
from deal_or_no_deal_ai.retrieval_benchmark import Passage, retrieve
from deal_or_no_deal_ai.ragas_evaluation import native_id_scores
from deal_or_no_deal_ai.configuration import load_configuration
from deal_or_no_deal_ai.command_center import workspace_id
from deal_or_no_deal_ai.storage import Store, RecordWrite


def main():
    case = load_registered_case(ROOT)
    passages = [Passage(b.block_id, b.text, case.dependency_digest, b.source.content_digest, b.page, True) for b in case.inventory]
    # Evaluator-only annotations, never sent to runtime extraction or retrieval.
    queries = [("Cash available for debt service", ["FIN-P2"]), ("Net income depreciation amortization", ["FIN-P1"]),
               ("Requested principal maturity loan", ["AGREEMENT-P1"])]
    store = Store(load_configuration(ROOT).database); store.initialize()
    operation = str(uuid4())
    receipt = store.admit(operation, dict(workspace_id=workspace_id(ROOT), review_id=operation), dict(action="OFFLINE_RETRIEVAL_ID_BENCHMARK"))
    try:
        rows = []
        for query, expected in queries:
            for strategy in ("DIRECT", "KEYWORD"):
                result = retrieve(passages, query, scope_digest=case.dependency_digest, strategy=strategy, top_k=2)
                scores = native_id_scores(result["passage_ids"], expected, ranked=result["ranked"])
                rows.append(dict(query=query, evaluator_reference_ids=expected, retrieval=result, native_ragas=scores))
        report = dict(evidence="EXECUTED_OFFLINE_RETRIEVAL_AND_NATIVE_ID_METRICS", annotation_status="AI_AUTHORED_SYNTHETIC_DIAGNOSTIC_NOT_INDEPENDENTLY_REVIEWED",
            source_scope=case.dependency_digest, passage_unit="ORIGINAL_REGISTERED_PAGE_NOT_SEMANTIC_TOKEN_CHUNK", rows=rows,
            arms=dict(DIRECT="EXECUTED", KEYWORD="EXECUTED_BM25", VECTOR="NOT_RUN_ACTUAL_EMBEDDINGS_REQUIRED", HYBRID="NOT_RUN_ACTUAL_EMBEDDINGS_REQUIRED"),
            provider_requests=0, cost_usd="0", faithfulness=None, custom_rubric=None, live_journey=False)
        destination = ROOT / "var/evaluations/retrieval-baselines" / operation
        destination.mkdir(parents=True, exist_ok=False)
        raw = (json.dumps(report, indent=2, allow_nan=False) + "\n").encode()
        (destination / "report.json").write_bytes(raw)
        store.put_record(RecordWrite("retrieval-evaluation:" + operation, "RETRIEVAL_EVALUATION", dict(path=str(destination.relative_to(ROOT)), report_sha256=sha256(raw).hexdigest())))
        store.release(receipt, confirmed_idle=True)
        print(json.dumps(dict(report=str(destination / "report.json"), arms=report["arms"], provider_requests=0)))
    except BaseException:
        store.mark_unknown(receipt)
        raise


if __name__ == "__main__":
    main()
