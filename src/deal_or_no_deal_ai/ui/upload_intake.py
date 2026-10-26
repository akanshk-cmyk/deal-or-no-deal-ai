"""Local PDF upload inspection and retained citation explorer; no financial dispatch."""
from .labels import friendly, FINANCIAL_HELP

from uuid import UUID, uuid4, uuid5
from hashlib import sha256
import sqlite3

from ..context import InputError, fingerprint
from ..storage import Store
from ..upload_intake import inspect_package, list_packages, load_package


def render(st, root, actor):
    st.info("Upload synthetic deal PDFs, inspect their pages, declare their reporting basis, then Run AI Deal Review. New reviews pause for human evidence verification. Inspection makes no model calls.")
    st.caption("1–3 text PDFs · 10 pages combined · 10 MB combined (10,000,000 bytes). No scans/OCR or encrypted files. Originals are retained locally; no automatic expiry.")
    st.subheader("Step 1 - Upload and validate documents")
    if actor.persona == "Analyst":
        nonce = st.session_state.setdefault("upload_nonce", str(uuid4()))
        with st.form("upload-inspection:" + nonce):
            files = st.file_uploader("Upload synthetic deal PDFs", type=["pdf"], accept_multiple_files=True)
            confirmed = st.checkbox("I confirm these documents contain only synthetic educational data")
            submitted = st.form_submit_button("Validate and inspect uploads", type="primary")
        if submitted:
            if not files or not confirmed:
                st.error("Select PDFs and confirm synthetic educational data. Nothing was saved.")
            else:
                values = [(f.name, f.getvalue()) for f in files]
                operation = str(uuid5(UUID(nonce), fingerprint("UPLOAD_UI_FILES", [(n, sha256(b).hexdigest()) for n, b in values])))
                try:
                    with st.spinner("Checking PDF bytes and extracting cited pages…"):
                        package = inspect_package(root, actor, operation, values, synthetic_confirmed=confirmed)
                except (InputError, ValueError, OSError, sqlite3.Error) as error:
                    # Only explicit safe reason codes; never echo parser/raw content errors.
                    code = str(error) if isinstance(error, InputError) else "UPLOAD_NOT_COMPLETED"
                    st.error("Upload inspection stopped: " + code + ". No financial review was started. If recovery is required, retain the operation ID: " + operation)
                    if getattr(error, "filename", None):
                        st.text("File requiring attention: " + error.filename)
                else:
                    st.session_state.selected_upload_operation = package["operation_id"]
                    st.success("PDF validation completed and cited pages saved. Inspected—not reviewed.")
        if st.button("Prepare another upload package"):
            st.session_state.upload_nonce = str(uuid4())
            st.rerun()
    else:
        st.caption("Switch to simulated Analyst to submit uploads. You may inspect retained packages in this local workspace.")
    packages = list_packages(root, actor)
    if not packages:
        st.info("No retained upload packages. Upload inspection does not create sample deals or financial decisions.")
        return
    options = [p["operation_id"] for p in packages]
    selected = st.session_state.get("selected_upload_operation")
    operation = st.selectbox("Retained upload package", options, index=options.index(selected) if selected in options else 0,
        format_func=lambda op: next(p["observed_at_utc"] + " · " + str(p["page_count"]) + " pages · " + p["package_id"][:8] for p in packages if p["operation_id"] == op))
    package = load_package(root, actor, operation)
    st.subheader("Inspected—not reviewed")
    st.caption("Origin, borrower, reporting period and source authority remain unverified. Page text is not verified table/year alignment. Document search and AI analysis have not been performed.")
    st.dataframe([dict(File=s["filename"], Pages=len(s["pages"]), Bytes=s["byte_count"], Result="Text extracted · not semantic verification") for s in package["sources"]], hide_index=True)
    source_id = st.selectbox("Uploaded source", [s["sha256"] for s in package["sources"]], key="upload-source:" + operation,
        format_func=lambda h: next(s["filename"] for s in package["sources"] if s["sha256"] == h))
    source = next(s for s in package["sources"] if s["sha256"] == source_id)
    page_key = "upload-page:" + operation
    if st.session_state.get(page_key, 1) > len(source["pages"]):
        st.session_state[page_key] = 1
    number = st.selectbox("Uploaded source page", list(range(1, len(source["pages"]) + 1)), key=page_key)
    page = source["pages"][number - 1]
    st.text("Citation: " + page["ref"])
    with st.expander('Read parsed page text',expanded=False):
        st.text(page["text"])
    with st.expander("Technical details"):
        st.caption("Page text SHA256: " + page["text_sha256"] + " · Parser: " + package["parser"])
    raw = (root / "var/uploads" / actor.workspace_id / package["package_id"] / (source_id + ".pdf")).read_bytes()
    st.download_button("Download retained original PDF", raw, file_name=source["filename"], mime="application/pdf")
    st.subheader('Step 2 - Confirm reporting basis')
    st.caption('Review prefilled dates and policy settings, then confirm. No financial amounts to type.')
    from ..configuration import load_configuration
    from ..upload_live import load_uploaded_case,run_uploaded,identities
    supported=False
    if load_configuration(root).mode=='LIVE':
        try:
            _,origin=load_uploaded_case(root,actor,operation)
            supported=True
        except (InputError,ValueError,OSError):
            pass
    declared=Store(load_configuration(root).database).get_record('upload-profile:'+operation)
    if declared:
        with st.expander('Saved reporting details for this uploaded deal',expanded=False):
            st.caption('Shared with every permitted demo role. These are saved declarations, not evidence verification.')
            st.dataframe([{'Detail':name.replace('_',' ').title(),'Saved value':str(value) if value is not None else 'Unknown'} for name,value in declared[1]['profile'].items()],hide_index=True)
    if (not supported or declared) and load_configuration(root).mode=='LIVE' and actor.persona=='Analyst':
        from ..upload_profile import UploadProfile,save_profile
        from ..profile_suggestions import suggest_profile
        suggestions=suggest_profile(package)
        defaults=declared[1]['profile'] if declared else suggestions['values']
        field_key=lambda name:'upload-profile-field:'+operation+':'+name
        # Older browser sessions can retain blank widget state despite new defaults.
        seed_key='upload-profile-prefill-v2:'+operation
        if not st.session_state.get(seed_key):
            for name,value in defaults.items():
                if st.session_state.get(field_key(name)) in (None,'') and value not in (None,''):
                    st.session_state[field_key(name)]=value
            st.session_state[seed_key]=True
        with st.expander('Declare the uploaded deal and reporting basis',expanded=True):
            st.caption('Check the suggestions before saving. Review date defaults to the upload date (UTC); edit it for a historical review. Unknown policy settings require review.')
            if st.button('Refill from uploaded documents',key='refill-profile:'+operation):
                fields=('borrower','review_as_of','annual_start','annual_end','previous_start','previous_end','transaction_date','annual_kind')
                for name in fields:
                    st.session_state[field_key(name)]=suggestions['values'].get(name,None if name=='annual_kind' else '')
                st.session_state[field_key('confirmed')]=False
                st.info('Document suggestions restored. Review them and confirm before saving; existing saved analysis was not changed.')
            if suggestions['conflicts']:st.warning('Different values found; enter the correct documented value for: '+', '.join(suggestions['conflicts']))
            with st.expander('Sources for suggested values'):
                st.dataframe([dict(Field=k,Value=suggestions['values'][k],Citation=e['source'],Quote=e['quote']) for k,items in suggestions['evidence'].items() for e in items],hide_index=True)
            with st.form('upload-profile:'+operation):
                borrower_col,review_col=st.columns([2,1])
                borrower=borrower_col.text_input('Documented borrower / legal entity',value=defaults.get('borrower',''),key=field_key('borrower'))
                review_date=review_col.text_input('Review date (YYYY-MM-DD)',value=defaults.get('review_as_of',''),key=field_key('review_as_of'))
                start_col,end_col,balance_col=st.columns(3)
                annual_start=start_col.text_input('Annual period start (YYYY-MM-DD)',value=defaults.get('annual_start',''),key=field_key('annual_start'))
                annual_end=end_col.text_input('Annual period end (YYYY-MM-DD)',value=defaults.get('annual_end',''),key=field_key('annual_end'))
                transaction_date=balance_col.text_input('Balance-sheet / transaction as-of date (YYYY-MM-DD)',value=defaults.get('transaction_date',''),key=field_key('transaction_date'))
                kinds=('HISTORICAL_ANNUAL_STATEMENT','SUPPLIED_ANNUAL_PROJECTION')
                kind=st.selectbox('Annual figures are',kinds,index=kinds.index(defaults['annual_kind']) if defaults.get('annual_kind') in kinds else None,format_func=lambda v:v.replace('_',' ').title(),key=field_key('annual_kind'))
                with st.expander('Optional comparative period - used for revenue growth',expanded=False):
                    previous_start_col,previous_end_col=st.columns(2)
                    previous_start=previous_start_col.text_input('Comparative annual period start (YYYY-MM-DD, optional)',value=defaults.get('previous_start',''),key=field_key('previous_start'))
                    previous_end=previous_end_col.text_input('Comparative annual period end (YYYY-MM-DD, optional)',value=defaults.get('previous_end',''),key=field_key('previous_end'))
                fmt=lambda v:'Unknown' if v is None else 'Yes' if v else 'No'
                equipment_col,kyc_col,sanctions_col=st.columns(3)
                secured=equipment_col.selectbox('Sample equipment lending policy applicable?',(None,True,False),index=(None,True,False).index(defaults.get('secured_equipment')),format_func=fmt,key=field_key('secured_equipment'))
                kyc=kyc_col.selectbox('Sample KYC control required?',(None,True,False),index=(None,True,False).index(defaults.get('kyc_required')),format_func=fmt,key=field_key('kyc_required'))
                sanctions=sanctions_col.selectbox('Sample sanctions control required?',(None,True,False),index=(None,True,False).index(defaults.get('sanctions_required')),format_func=fmt,key=field_key('sanctions_required'))
                confirmed=st.checkbox('I checked borrower, periods and USD whole-unit basis against the uploaded documents',key=field_key('confirmed'))
                saved=st.form_submit_button('Save reporting basis')
            if saved:
                try:
                    if not confirmed:raise InputError('PROFILE_DECLARATION_CONFIRMATION_REQUIRED')
                    save_profile(root,actor,operation,UploadProfile(borrower=borrower,review_as_of=review_date,annual_start=annual_start,annual_end=annual_end,previous_start=previous_start,previous_end=previous_end,transaction_date=transaction_date,annual_kind=kind,secured_equipment=secured,kyc_required=kyc,sanctions_required=sanctions))
                except (InputError,ValueError,OSError,sqlite3.Error) as error:
                    missing=[label for label,value in [('borrower',borrower.strip()),('review date',review_date),('annual start',annual_start),('annual end',annual_end),('transaction date',transaction_date),('actual results or projection',kind),('confirmation checkbox',confirmed)] if not value]
                    if isinstance(error,InputError) and str(error)=='REVIEW_PROFILE_ALREADY_BOUND':
                        st.error('Reporting basis is locked because this deal review already started. The saved dates cannot be changed for that review.')
                    elif isinstance(error,sqlite3.Error):
                        st.error('Reporting basis could not be saved because local storage is unavailable or busy. Your entries are still displayed; no AI call was made.')
                    else:
                        st.error('Reporting basis not saved. '+('Complete: '+', '.join(missing)+'.' if missing else 'Check YYYY-MM-DD dates; annual end must follow annual start and the comparative period must precede it. If all dates are valid, retained upload validation may need attention.'))
                else:st.rerun()
    st.subheader('Step 3 - Run AI Deal Review')
    if supported:
        st.success('Uploaded reporting profile available. This permits live extraction, not evidence verification or credit approval.' if origin['profile']=='USER_DECLARED_UPLOAD-1.0' else 'Complete Standard Deal source profile matched. This permits live analysis, not credit approval.')
        st.caption('Deal ID: '+origin['deal_id'])
        st.warning('Run sends uploaded fictional content to Nebius within the shared USD0.10 allowance. Human verification pauses must be completed before analysis/report continuation. No automatic credit approval.')
        store=Store(load_configuration(root).database)
        with store.connection() as connection:
            blockers=connection.execute('SELECT operation_id,state FROM app_operations WHERE active_execution_key IS NOT NULL').fetchall()
        if blockers:
            st.error('Reporting basis is saved. AI analysis cannot start because another review is still running or needs recovery. Editing dates or uploading again will not clear that lock.')
            for blocker in blockers:
                st.caption('Blocking attempt: '+blocker['operation_id']+' | '+('Recovery required' if blocker['state']=='RECOVERY_REQUIRED' else 'Execution in progress'))
        if st.button('Run AI Deal Review',type='primary',disabled=actor.persona!='Analyst' or bool(blockers)):
            try:
                with st.spinner('Running extraction → calculations → compliance → risk → synthesis → draft memo…'):
                    result=run_uploaded(root,actor,operation)
                st.session_state.selected_financial_operation=identities(operation)['operation_id']
                st.session_state.next_financial_run=identities(operation)['operation_id']
                if result['status']=='COMPLETED':
                    st.success('Uploaded deal analysis completed. Review findings and download the draft memo. No human approval was recorded.')
                else:
                    st.warning('Review needs attention: '+friendly(result['status'])+'. Open Review Workspace for details.')
            except (InputError,ValueError,OSError,sqlite3.Error) as error:
                st.error('Live review could not complete. No saved answers were substituted. Open Review Workspace or Agent Activity to inspect the retained attempt; do not automatically retry.')
                from ..storage import RunBusy
                if isinstance(error,RunBusy):
                    st.warning('Another review holds the execution lock. Your reporting basis is saved, but no analysis started for this upload. Resolve that review before running another one.')
                reasons={
                    'EVALUATION_REQUEST_UNCERTAIN_NO_RETRY':'The request to measure this document packet reached an uncertain result. Deal analysis has not started. Its spending reservation is retained; the matching provider status/usage must be checked before retrying.',
                    'EVALUATION_REQUEST_REQUIRES_RECONCILIATION':'The earlier document-sizing request has no reconciled result. Do not repeat Run or re-upload to bypass this check. Check its provider status/usage first.',
                    'PROVIDER_INPUT_EXCEEDS_APPROVED_CAP':'The uploaded document packet exceeds the approved AI input limit. No analysis request was sent. The documents need a reviewed smaller scope before continuing.',
                    'SHARED_ALLOWANCE_EXHAUSTED_OR_UNCERTAIN':'The shared demo spending allowance cannot cover this request while outstanding reservations remain. Reconcile the existing requests before continuing.',
                }
                if isinstance(error,InputError) and str(error) in reasons:
                    st.warning(reasons[str(error)])
                    st.caption('Support reference: '+str(error)+' | Uploaded package: '+package['package_id'])
        store=Store(root/'var/deal_review.sqlite3')
        if store.get_record('live-context:'+identities(operation)['operation_id']):
            from ..command_center import get_run
            from .command_center import METRIC_NAMES
            from .uploaded_calculations import render as render_uploaded_calculations
            render_uploaded_calculations(st,root,actor,get_run(store,actor,identities(operation)['operation_id']),METRIC_NAMES)
            from .command_center import go
            st.session_state.selected_financial_operation=identities(operation)['operation_id']
            for target in ('Review Workspace','Agent Activity','Credit Memo'):
                st.button('Open '+target,on_click=go,args=(st,target))
    else:
        st.button('Run AI Deal Review',type='primary',disabled=True)
        st.info('Save reporting basis in Step 2 to enable Run. Use the Analyst demo role; live analysis must be enabled in the application configuration.')
        st.caption('Save the documented reporting basis to enable a new uploaded-deal review. Missing information is not filled from sample data. Large requests may stop at the approved token limit; no pages are silently removed.')
    with st.expander('Optional manual financial evidence entry',expanded=False):
        st.caption('This older manual entry tool is optional. It is not required to save reporting basis or start live AI extraction. Verify live-extracted facts later in Review Workspace.')
        from .upload_facts import render as render_facts
        render_facts(st, root, actor, operation, page)
