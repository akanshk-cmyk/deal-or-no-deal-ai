"""Bounded upload onboarding: exact approved source profile, never fixture answers."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from uuid import UUID,uuid5

from .context import InputError,fingerprint
from .services import load_registered_case,RegisteredFixtureCase,_scope,_binding,validate_registered_case
from .upload_intake import load_package,list_packages
from .configuration import load_configuration


def identities(operation):
    return dict(deal_id=str(uuid5(UUID(operation),'uploaded-deal')),
                operation_id=str(uuid5(UUID(operation),'uploaded-live-review')))


def uploaded_deal_ids(root,actor):
    return {identities(p['operation_id'])['deal_id'] for p in list_packages(root,actor)}


def load_uploaded_case(root,actor,upload_operation):
    """Recheck original retained bytes/pages; use uploaded text, not reference copies."""
    package=load_package(root,actor,upload_operation)
    from .storage import Store
    if Store(load_configuration(Path(root)).database).get_record('upload-profile:'+upload_operation):
        from .upload_profile import load_profile_case
        return load_profile_case(root,actor,upload_operation)
    base=load_registered_case(Path(root))
    sources={s['sha256']:s for s in package['sources']}
    expected={b.source.content_digest for b in base.inventory}
    if set(sources)!=expected or len(package['sources'])!=len(expected):
        raise InputError('UPLOAD_COMPLETE_STANDARD_DEAL_REQUIRED')
    pages={}
    for block in base.inventory:
        source=sources[block.source.content_digest]
        if block.page>len(source['pages']):raise InputError('UPLOAD_PROFILE_PAGE_MISMATCH')
        page=source['pages'][block.page-1]
        if page['text']!=block.text:raise InputError('UPLOAD_PROFILE_TEXT_MISMATCH')
        pages[block.block_id]=dict(filename=source['filename'],source_sha256=source['sha256'],page=block.page,upload_ref=page['ref'])
    if package['page_count']!=len(base.inventory):raise InputError('UPLOAD_PROFILE_PAGE_MISMATCH')
    ids=identities(upload_operation)
    data=deepcopy(base.case_data)
    data['scope']['deal_id']=ids['deal_id']
    registration=base.registration.model_copy(update=dict(deal_id=ids['deal_id'],case_semantic_digest=fingerprint('APPROVED_CASE_METADATA',data)))
    scope=_scope(registration)
    inventory=tuple(replace(b,scope=scope,text=sources[b.source.content_digest]['pages'][b.page-1]['text']) for b in base.inventory)
    case=RegisteredFixtureCase(registration,scope,base.wire,data,inventory,_binding(registration,scope,base.wire,data,inventory))
    validate_registered_case(case)
    origin=dict(upload_operation_id=upload_operation,package_id=package['package_id'],package_digest=package['package_digest'],
                deal_id=ids['deal_id'],profile='EXACT_STANDARD_DEAL_UPLOAD',page_map=pages)
    return case,origin


def case_for_context(root,actor,context):
    origin=context.get('upload_origin')
    if not origin:return load_registered_case(Path(root))
    case,current=load_uploaded_case(root,actor,origin['upload_operation_id'])
    if current!=origin:raise InputError('UPLOADED_REVIEW_SOURCE_CHANGED')
    return case


def run_uploaded(root,actor,upload_operation):
    from .command_center import _scope as authorize
    from .live_worker import verification_policy
    from .live_demo import run_demo
    root=Path(root);config=load_configuration(root)
    if config.mode!='LIVE':
        raise InputError('LIVE_DEMO_CONFIGURATION_REQUIRED')
    case,origin=load_uploaded_case(root,actor,upload_operation)
    authorize(actor,dict(workspace_id=actor.workspace_id,deal_id=case.scope.deal_id))
    if actor.persona!='Analyst':raise InputError('LIVE_ANALYST_COMMAND_REQUIRED')
    return run_demo(root,actor,identities(upload_operation)['operation_id'],upload_operation_id=upload_operation)
