from deal_or_no_deal_ai.profile_suggestions import suggest_profile


def package(*texts):
    return dict(observed_at_utc='2026-10-26T02:00:00+00:00',sources=[dict(pages=[dict(ref='uploaded-page-'+str(i),text=t)]) for i,t in enumerate(texts)])


def test_cited_prefill_and_explicit_calendar_projection():
    p=package('Borrower and legal entity: Fictional Co\nProposed transaction date: 2026-10-23\nAnnual projection: 2027-01-01 through 2027-12-31.',
        '2026 and 2027 columns below are supplied annual projections, not actuals.\nCalendar years: 01 January through 31 December of each named year.')
    result=suggest_profile(p);v=result['values']
    assert v['borrower']=='Fictional Co'
    assert v['review_as_of']=='2026-10-26'
    assert v['annual_start']=='2027-01-01' and v['previous_end']=='2026-12-31'
    assert v['annual_kind']=='SUPPLIED_ANNUAL_PROJECTION'
    assert result['evidence']['borrower'][0]['source']=='uploaded-page-0'
    assert 'secured_equipment' not in v and 'kyc_required' not in v


def test_unknown_conflicting_and_prepared_dates_not_invented():
    result=suggest_profile(package('Borrower: One LLC\nPrepared: 2025-01-01','Borrower: Two LLC\nRevenue 2024 2025'))
    assert 'borrower' not in result['values'] and 'borrower' in result['conflicts']
    assert 'annual_start' not in result['values'] and 'transaction_date' not in result['values']
    assert result['values']['review_as_of']=='2026-10-26'


def test_conflicting_explicit_review_dates_remain_blank():
    result=suggest_profile(package('Review date: 2026-01-01','Review date: 2026-02-01'))
    assert 'review_as_of' not in result['values']
