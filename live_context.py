"""Approved LIVE-COMPACT-1.0 packets; no dispatch or fixture prompt changes."""
from pathlib import Path
from .services import load_registered_case
from .synthesis import prepare_synthesis
from .provider import SCHEMAS


def live_wire_schema(stage):
    """Expose existing financial basis invariants to structured decoding, too."""
    from copy import deepcopy
    from .services import _expected_basis
    schema = compact_schema(SCHEMAS[stage].model_json_schema())
    if stage == "extractor":
        fields = schema["$defs"]["FinancialInputsWire"]["properties"]
        for field, reference in list(fields.items()):
            fact = schema["$defs"][reference["$ref"].rsplit("/",1)[1]]
            known = deepcopy(fact); missing = deepcopy(fact)
            known["properties"]["value"] = next(v for v in known["properties"]["value"]["anyOf"] if v.get("type") != "null")
            known["properties"]["basis_id"] = dict(type="string",const=_expected_basis(field))
            known["properties"]["refs"]["minItems"] = 1
            missing["properties"]["value"] = dict(type="null")
            missing["properties"]["basis_id"] = dict(type="null")
            missing["properties"]["refs"]["maxItems"] = 0
            fields[field] = dict(anyOf=[known,missing])
    return alias_definitions(schema)

def compact_schema(value):
    if isinstance(value, dict):
        return {k: compact_schema(v) for k, v in value.items() if k not in {'title', 'description', 'default'}}
    if isinstance(value, list):
        return [compact_schema(v) for v in value]
    return value


def alias_definitions(schema):
    aliases={name:'d'+str(i) for i,name in enumerate(schema.get('$defs',{}))}
    def rewrite(value):
        if isinstance(value,dict):
            return {k:('#/$defs/'+aliases[v[len('#/$defs/'):]] if k=='$ref' and isinstance(v,str) and v.startswith('#/$defs/') else
                {aliases[name]:rewrite(definition) for name,definition in v.items()} if k=='$defs' else rewrite(v)) for k,v in value.items()}
        if isinstance(value,list):
            return [rewrite(v) for v in value]
        return value
    return rewrite(schema)


def prepare_live_tasks(root, *, case=None):
    case = case if case is not None else load_registered_case(Path(root))
    general=case.registration.version=='UPLOAD-PROFILE-1.0'
    request = None if general else prepare_synthesis(case)["request"]
    extraction_instruction = (Path(root) / "docs/agents/live-extractor.md").read_text(encoding="utf-8").split("## Runtime prompt\n", 1)[1].strip()
    synthesis_instruction = (Path(root) / "docs/agents/live-synthesizer.md").read_text(encoding="utf-8").split("## Runtime prompt\n", 1)[1].strip()
    extraction = dict(sources={b.block_id:b.text for b in case.inventory}, bases=case.case_data['bases'],
        review_as_of=case.registration.review_as_of, evidence_cutoff=case.registration.evidence_cutoff_at)
    return dict(extractor=dict(instruction=extraction_instruction, context=extraction, schema=live_wire_schema("extractor")), synthesizer=(dict(instruction=synthesis_instruction,context={},schema=live_wire_schema('synthesizer')) if general else live_synthesis_task(root, request)))


def live_synthesis_task(root, request):
    instruction = (Path(root) / "docs/agents/live-synthesizer.md").read_text(encoding="utf-8").split("## Runtime prompt\n", 1)[1].strip()
    return dict(instruction=instruction, context=_synthesis_context(request), schema=alias_definitions(compact_schema(SCHEMAS["synthesizer"].model_json_schema())))


def _synthesis_context(request):
    financial = [{k:m[k] for k in ('metric_id','display','unit','validity','reason')} for m in request['financial']['metrics']]
    for metric in financial:
        metric['ref']='calc:DSCR' if metric['metric_id']=='CALC-004' else 'calc:'+metric['metric_id']
    policy = [{k:r[k] for k in ('ref','result','state','applicability','workflow','observed','threshold','predicate')} for r in request['compliance']['rules']]
    score = request['risk']['score']
    columns=list(policy[0])
    financial_columns=list(financial[0])
    return dict(terms=request['terms'], financial=dict(columns=financial_columns,rows=[[m[k] for k in financial_columns] for m in financial]), policy=dict(columns=columns,rows=[[r[k] for k in columns] for r in policy]),
        risk={k:score[k] for k in ('status','display','band','missing','workflow')},
        factors=[{k:f[k] for k in ('factor_id','rating','weight','contribution')} for f in score['factors']],
        source_and_panel_refs=[k for k,v in request['reference_dictionary'].items() if v['kind'] in {'SOURCE','PANEL'}], analysis_scope=request['financial']['analysis_scope'],
        covenant_status=request['financial']['covenant_status'], concentration='NOT_ASSESSED')
