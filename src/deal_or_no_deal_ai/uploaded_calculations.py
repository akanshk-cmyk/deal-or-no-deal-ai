"""Source-bound arithmetic preview; never a verified graph stage or approval."""
from pathlib import Path
from dataclasses import asdict
from .context import InputError,primitive,fingerprint
from .contracts import parse_extraction
from .finance import calculate_metrics
from .policy import evaluate_policy,PolicyConfig
from .risk import assess_risk


def preview(root,actor,run):
    from .command_center import _scope
    from .upload_live import case_for_context
    from .services import _validate_inputs
    _scope(actor,run['context']['scope'])
    if not run['context'].get('upload_origin') or 'extractor' not in run['artifacts'] or 'financial_analyst' in run['artifacts']:
        return None
    if run.get('outcome',{}).get('source_validation_failed') or run.get('outcome',{}).get('quarantine'):
        raise InputError('UPLOADED_PREVIEW_SOURCE_UNAVAILABLE')
    case=case_for_context(Path(root),actor,run['context'])
    wire=parse_extraction(run['artifacts']['extractor']['payload']['wire_json'])
    _validate_inputs(case.registration,case.scope,wire,case.case_data,case.inventory,registered_extraction=False)
    applicable=case.case_data['policy_config']['secured_equipment']
    metrics=calculate_metrics({k:f.value for k,f in wire.financial_inputs},secured_equipment=applicable is not False)
    rows=[]
    for metric in metrics.values():
        row=primitive(asdict(metric))
        row['source_refs']=sorted({r for k in metric.inputs for r in getattr(wire.financial_inputs,k).refs})
        row['basis_ids']=sorted({getattr(wire.financial_inputs,k).basis_id for k in metric.inputs if getattr(wire.financial_inputs,k).basis_id})
        rows.append(row)
    digest=fingerprint('UPLOADED_ARITHMETIC_INPUT',dict(wire=wire.model_dump(),source_binding=run['context']['source_binding']))
    cfg=case.case_data['policy_config']
    metric_refs={m.metric_id:tuple(sorted({ref for field in m.inputs for ref in getattr(wire.financial_inputs,field).refs})) for m in metrics.values()}
    policy=evaluate_policy(metrics,wire.terms,config=PolicyConfig(cfg['secured_equipment'],cfg['kyc_fixture_required'],cfg['sanctions_fixture_required'],cfg['basis']),
        dependency_digest=digest,metric_source_refs=metric_refs,material_financial_ready=False,
        term_conflicts=bool(wire.conflicts),synthesis_complete=False)
    # Source data alone is not an approved factor rating or human verification.
    risk=assess_risk(factors=(),metrics=metrics,financial_values={k:f.value for k,f in wire.financial_inputs},
        available_refs=frozenset(b.block_id for b in case.inventory),scope=case.scope,
        as_of=case.registration.review_as_of,compliance=policy,dependency_digest=digest)
    return dict(deal_id=run['context']['scope']['deal_id'],run_id=run['context']['scope']['run_id'],
        provenance='UNVERIFIED_EXTRACTION_ARITHMETIC_PREVIEW',human_verified=False,
        policy_applicability_confirmed=applicable is not None,metrics=rows,
        policy=primitive(asdict(policy)),risk=primitive(asdict(risk)),input_digest=digest)
