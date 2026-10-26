"""Lazy native RAGAS ID metrics only; no default LLM/embedding/judge client."""
import asyncio
import os

from .context import InputError


def native_id_scores(retrieved_ids, reference_ids, *, ranked):
    if type(ranked) is not bool or not reference_ids or len(set(reference_ids)) != len(reference_ids) or len(set(retrieved_ids)) != len(retrieved_ids):
        raise InputError("EXACT_RETRIEVAL_IDS_REQUIRED")
    os.environ["RAGAS_DO_NOT_TRACK"] = "true"
    from ragas import __version__
    from ragas.dataset_schema import SingleTurnSample
    from ragas.metrics import IDBasedContextPrecision, IDBasedContextRecall
    sample = SingleTurnSample(retrieved_context_ids=retrieved_ids, reference_context_ids=reference_ids)
    async def score():
        return (await IDBasedContextPrecision().single_turn_ascore(sample),
                await IDBasedContextRecall().single_turn_ascore(sample))
    precision, recall = asyncio.run(score())
    return dict(package="ragas", version=__version__, evidence="EXECUTED_NATIVE_ID_METRICS_NOT_LLM_QUALITY",
        native_id_context_precision=precision if ranked else None, native_id_context_recall=recall,
        precision_applicability="RANKED_ARM" if ranked else "NOT_APPLICABLE_UNRANKED_DIRECT",
        faithfulness=None, response_relevancy=None, custom_rubric=None, judge_requests=0,
        limitation="ID overlap does not measure answer truth, claim support or source currentness.")
