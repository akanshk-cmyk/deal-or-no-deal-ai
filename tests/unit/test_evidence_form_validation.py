from deal_or_no_deal_ai.ui.live_workflow import assessment_errors
from deal_or_no_deal_ai.live_review import required_checks


def setup():
    return dict(stage='fact_review',sources={'A':'Borrower: Fictional LLC','B':'Entity: Fictional LLC'}),dict(source_refs=['A','B'])


def test_comments_and_checkboxes_do_not_replace_source_quotes():
    request,target=setup()
    errors=assessment_errors(request,target,'HUMAN_SUPPORTED',{'A':'','B':''},required_checks('fact_review'),'verified-test')
    assert any('comments alone are not evidence' in e for e in errors)
    assert any('A, B' in e for e in errors)


def test_exact_quotes_and_all_checks_required():
    request,target=setup()
    assert not assessment_errors(request,target,'HUMAN_SUPPORTED',request['sources'],required_checks('fact_review'),'Checked both pages.')
    errors=assessment_errors(request,target,'HUMAN_SUPPORTED',{'A':'Fictional LLC','B':'Wrong borrower'},[],'Reviewed')
    assert any('Complete these checks' in e for e in errors)
    assert any('quote for B' in e for e in errors)


def test_withholding_does_not_require_claiming_all_checks_passed():
    request,target=setup()
    assert not assessment_errors(request,target,'WITHHELD',{'A':'Borrower: Fictional LLC','B':''},[],'Other page does not establish this claim.')
