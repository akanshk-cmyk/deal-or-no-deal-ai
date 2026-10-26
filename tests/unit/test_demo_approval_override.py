from deal_or_no_deal_ai.uploaded_decisions import demo_override_available


def test_only_pending_checks_can_use_demo_override():
    a=dict(outcome='Pending Review',blockers=['covenant'],evaluated_requirements=[dict(requirement_id='covenant',status='PENDING')])
    assert demo_override_available(a)
    for outcome in ('Recovery Required','Exception Review Required','Additional Information Required'):
        assert not demo_override_available({**a,'outcome':outcome})
    for status in ('STALE','MISSING','EXCEPTION','RECOVERY'):
        assert not demo_override_available({**a,'evaluated_requirements':[dict(requirement_id='covenant',status=status)]})
