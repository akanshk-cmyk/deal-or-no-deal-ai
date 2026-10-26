"""Shared read-only uploaded arithmetic preview, identical across permitted roles."""
from ..context import InputError


def render(st,root,actor,run,names):
    from ..uploaded_calculations import preview
    try:data=preview(root,actor,run)
    except (InputError,ValueError,OSError):
        st.warning('Uploaded calculation preview is unavailable because source or reporting-basis validation needs attention.')
        return
    if not data:return
    with st.expander('Uploaded deal calculations - preliminary',expanded=True):
        st.caption('Calculated automatically from this deal’s actual extracted inputs. Not human-verified, not a completed specialist stage, and not policy clearance. Deal ID: '+data['deal_id'])
        if not data['policy_applicability_confirmed']:
            st.caption('LTV is arithmetic only; equipment-policy applicability remains unconfirmed.')
        st.dataframe([{'Calculation':names.get(m['metric_id'],m['metric_id']),'Calculated value':m['display'] or 'Not available','Unit':m['unit'],'Arithmetic status':m['validity'],'Reason':m['reason'],'Sources':', '.join(m['source_refs'])} for m in data['metrics']],hide_index=True)
    render_policy(st,data)
    render_risk(st,data)


def render_policy(st,data):
    with st.expander('Uploaded policy checks - preliminary',expanded=True):
        st.caption('Configured educational policy evaluated on unverified extracted data. No policy clearance or completed agent stage is recorded. Unknown applicability stays Unknown.')
        st.dataframe([{'Policy rule':r['rule_id'],'Predicate':r['predicate'],'Observed':r['observed'] or 'Not available','Threshold':r['threshold'] or 'Not applicable','Applicability':r['applicability'],'Result':'No breach on extracted data' if r['outcome']=='Pass' else r['outcome'] or r['control_result'] or 'Not evaluated','Evaluation':r['evaluation_state'],'Sources':', '.join(r['source_refs'])} for r in data['policy']['rules']],hide_index=True)


def render_risk(st,data):
    with st.expander('Uploaded risk assessment - preliminary',expanded=True):
        st.warning('Composite credit risk: Insufficient Data. No approved borrower factor ratings were supplied; no Low score is inferred from DSCR or LTV.')
        if data['risk']['risk_flags']:
            st.dataframe(data['risk']['risk_flags'],hide_index=True)
        else:st.write('No numeric exception-based risk flags were found on the current extracted inputs. This does not establish low risk or verified compliance.')
        st.write('**Outstanding risk information**')
        for item in data['risk']['score']['missing']:
            st.write('• '+item.removeprefix('factor:').replace('_',' ').capitalize()+' — supported assessment not supplied')
        st.caption('Fact verification, covenant evaluation and full-term repayment assessment remain separate requirements. Policy applicability, source support and any AI interpretations still need review.')
