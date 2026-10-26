"""Unverified, reviewer-declared source fit for new uploads; no sample facts."""
from dataclasses import replace
from datetime import date,datetime,timezone
from hashlib import sha256
from pathlib import Path
from types import SimpleNamespace
from uuid import UUID,uuid5
from typing import Literal
from .contracts import StrictModel,Text,DealTermsWire
from .context import InputError,fingerprint,strict_json
from .documents import SourceVersion,OriginalBlock
from .services import RegisteredFixtureCase,_scope,_binding
from .upload_intake import load_package
from .storage import Store,RecordWrite
from .configuration import load_configuration


class UploadProfile(StrictModel):
    borrower: Text
    review_as_of: str
    annual_start: str
    annual_end: str
    previous_start: str
    previous_end: str
    transaction_date: str
    annual_kind: Literal['SUPPLIED_ANNUAL_PROJECTION','HISTORICAL_ANNUAL_STATEMENT']
    secured_equipment: bool|None=None
    kyc_required: bool|None=None
    sanctions_required: bool|None=None

    def validate_dates(self):
        for k in ('review_as_of','annual_start','annual_end','transaction_date')+ (('previous_start','previous_end') if self.previous_start or self.previous_end else ()):
            if date.fromisoformat(getattr(self,k)).isoformat()!=getattr(self,k):raise InputError('EXPLICIT_ISO_PERIODS_REQUIRED')
        if self.annual_start>=self.annual_end or (self.previous_start or self.previous_end) and (self.previous_start>=self.previous_end or self.previous_end>=self.annual_start):
            raise InputError('NON_OVERLAPPING_ANNUAL_PERIODS_REQUIRED')


class UploadRegistration(SimpleNamespace):
    def model_dump(self):return vars(self)


def save_profile(root,actor,operation,profile):
    from .upload_live import identities
    profile=UploadProfile.model_validate(profile.model_dump());profile.validate_dates()
    package=load_package(root,actor,operation)
    if actor.persona!='Analyst':raise InputError('ANALYST_PROFILE_REQUIRED')
    store=Store(load_configuration(Path(root)).database);key='upload-profile:'+operation
    payload=dict(profile=profile.model_dump(),package_digest=package['package_digest'],status='USER_DECLARED_NOT_VERIFIED')
    # A declaration is metadata, not execution: do not acquire the global AI lock.
    # Serialize with review admission and recheck binding inside the same transaction.
    with store.transaction() as connection:
        row=connection.execute('SELECT version,payload FROM app_records WHERE record_key=?',(key,)).fetchone()
        prior=(row['version'],strict_json(row['payload'],envelope=True)) if row else None
        if prior and prior[1]==payload:return payload
        if connection.execute('SELECT 1 FROM app_records WHERE record_key=?',('live-context:'+identities(operation)['operation_id'],)).fetchone():
            raise InputError('REVIEW_PROFILE_ALREADY_BOUND')
        version=prior[0] if prior else 0
        store._write(connection,RecordWrite(key,'UPLOAD_PROFILE',payload,version))
        store._write(connection,RecordWrite('upload-profile-declaration:'+operation+':'+str(version+1),'UPLOAD_PROFILE_DECLARATION',dict(
            operation_id=operation,workspace_id=actor.workspace_id,reviewer_role=actor.persona,
            attribution='SIMULATED',timestamp_utc=datetime.now(timezone.utc).isoformat(),
            profile_revision=version+1,declaration_digest=fingerprint('PROFILE',payload),status='USER_DECLARED_NOT_VERIFIED'),0))
    return payload


def load_profile_case(root,actor,operation):
    from .upload_live import identities
    root=Path(root);package=load_package(root,actor,operation)
    stored=Store(load_configuration(root).database).get_record('upload-profile:'+operation)
    if not stored or stored[1]['package_digest']!=package['package_digest']:raise InputError('UPLOAD_REPORTING_PROFILE_REQUIRED')
    p=UploadProfile.model_validate(stored[1]['profile']);p.validate_dates()
    from .policy import sample_policy_spec
    if strict_json((root/'config/sample_policy.json').read_bytes())!=sample_policy_spec():raise InputError('POLICY_PROFILE_CHANGED')
    ids=identities(operation);subject=str(uuid5(UUID(operation),'borrower'));facility=str(uuid5(UUID(operation),'facility'))
    bases={'FY-ASSESS':dict(kind=p.annual_kind,start=p.annual_start,end=p.annual_end,currency='USD',scale='1'),
        'FY-PREV':dict(kind=p.annual_kind,start=p.previous_start,end=p.previous_end,currency='USD',scale='1'),
        'TXN-1':dict(kind='USER_DECLARED_TRANSACTION',as_of=p.transaction_date,currency='USD',scale='1')}
    if not p.previous_start and not p.previous_end:bases['FY-PREV']=dict(kind='NOT_PROVIDED',currency='USD',scale='1')
    mapping={};blocks=[];expected={}
    for i,source in enumerate(sorted(package['sources'],key=lambda s:s['sha256']),1):
        for page in source['pages']:
            handle='DOC'+str(i)+'-P'+str(page['page'])
            mapping[handle]=dict(filename=source['filename'],source_sha256=source['sha256'],page=page['page'],upload_ref=page['ref'])
            expected[handle]=SimpleNamespace(source_id='UPLOADED-DOC'+str(i),source_version='1',source_sha256=source['sha256'],page=page['page'],text_sha256=page['text_sha256'])
            blocks.append((handle,source,page,i))
    data=dict(scope=dict(deal_id=ids['deal_id'],subject_id=subject,facility_id=facility),bases=bases,
        source_basis=dict(proposed_review_as_of=p.review_as_of,proposed_field_authority={k:list(mapping) for k in ('terms','financials','equipment')}),
        subject_registry=dict(subject_label=p.borrower,status='USER_DECLARED_NOT_VERIFIED'),factor_assessments=[],required_page_dependencies={},
        policy_config=dict(secured_equipment=p.secured_equipment,kyc_fixture_required=p.kyc_required,sanctions_fixture_required=p.sanctions_required,basis='Reviewer-declared educational applicability; verification required'))
    registration=UploadRegistration(version='UPLOAD-PROFILE-1.0',scenario_id='UPLOADED',deal_id=ids['deal_id'],subject_id=subject,facility_id=facility,input_revision=1,
        review_as_of=p.review_as_of,evidence_cutoff_at=package['observed_at_utc'],source_profile_version='USER_DECLARED_UPLOAD-1.0',package_digest=package['package_digest'],
        case_semantic_digest=fingerprint('APPROVED_CASE_METADATA',data),policy_sha256=sha256((root/'config/sample_policy.json').read_bytes()).hexdigest())
    scope=_scope(registration)
    inventory=tuple(OriginalBlock(h,scope,SourceVersion('UPLOADED-DOC'+str(i),'1',s['sha256']),pg['page'],0,pg['text'],parser_verified=True,fit_verified=False) for h,s,pg,i in blocks)
    empty={'value':None,'refs':[],'basis_id':None}
    wire=DealTermsWire.model_validate(dict(terms={k:empty for k in DealTermsWire.model_fields['terms'].annotation.model_fields},financial_inputs={k:empty for k in DealTermsWire.model_fields['financial_inputs'].annotation.model_fields},conflicts=[]))
    case=RegisteredFixtureCase(registration,scope,wire,data,inventory,_binding(registration,scope,wire,data,inventory))
    origin=dict(upload_operation_id=operation,package_id=package['package_id'],package_digest=package['package_digest'],deal_id=ids['deal_id'],profile='USER_DECLARED_UPLOAD-1.0',profile_digest=fingerprint('UPLOAD_DECLARATION',stored[1]),page_map=mapping)
    return case,origin


def verify_new_task_tokens(root,task,stage,workspace):
    """Explicit Run setup only; exact existing provider token probe and allowance."""
    import json,tomllib
    from .evaluation_transport import EvaluationTransport
    from .provider import LIVE_STAGE_CAPS,prepare_request
    root=Path(root);digest=fingerprint('LIVE_PACKET',task)
    payload=dict(model='Qwen/Qwen3-30B-A3B-Instruct-2507',messages=[dict(role='system',content=task['instruction']),dict(role='user',content=json.dumps(task['context'],ensure_ascii=False,allow_nan=False,separators=(',',':')))],response_format=dict(type='json_schema',json_schema=dict(name=stage,strict=True,schema=task['schema'])),max_tokens=1,temperature=0,stream=False,n=1)
    scope=dict(workspace_id=workspace,review_id=str(uuid5(UUID(workspace),'input-token-probe:'+digest)),purpose='INPUT_TOKEN_PROBE')
    transport=EvaluationTransport(root,str(uuid5(UUID(workspace),'input-token-evaluation:'+digest)),scope)
    response=transport._dispatch('chat/completions',payload,_token_probe=True);count=response['usage']['prompt_tokens']
    if count>LIVE_STAGE_CAPS[stage][0]:raise InputError('PROVIDER_INPUT_EXCEEDS_APPROVED_CAP')
    actual=prepare_request(model_id=payload['model'],stage=stage,instruction=task['instruction'],context=task['context'],verified_input_tokens=count,max_output_tokens=LIVE_STAGE_CAPS[stage][1],profile='LIVE-COMPACT-1.0')
    if {k:v for k,v in actual.items() if k!='max_tokens'}!={k:v for k,v in payload.items() if k!='max_tokens'}:raise InputError('PROBE_AND_ACTUAL_INPUT_DIFFER')
    path=root/'config/live_smoke.toml';text=path.read_text(encoding='utf-8');counts=tomllib.loads(text).get('verified_packet_tokens',{});counts[digest]=count
    temporary=path.with_suffix('.tmp');temporary.write_text(text.partition('[verified_packet_tokens]')[0]+'[verified_packet_tokens]\n'+'\n'.join(json.dumps(k)+' = '+str(v) for k,v in counts.items())+'\n',encoding='utf-8');temporary.replace(path)
    return count
