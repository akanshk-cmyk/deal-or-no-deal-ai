"""Compact sidebar-only local readiness display; no provider calls."""
import json
from ..context import InputError


def render(st,root):
    key='local-ai-readiness:'+str(root)
    if st.button('Check live AI readiness'):
        from ..live_setup import readiness
        try:st.session_state[key]=readiness(root)
        except (InputError,ValueError,OSError):
            st.session_state.pop(key,None)
            st.error('Local readiness check could not finish. Check the local configuration and model setup. No AI request was sent.')
    result=st.session_state.get(key)
    if not result:return
    st.markdown('**Local setup check**')
    if result['status']=='READY_TO_START':st.success('Local setup checks passed')
    else:st.warning('Local setup needs attention')
    st.write('API key: '+('Configured' if result['api_key_present'] else 'Not configured'))
    st.write('Generation model: '+result['generation_model'])
    st.caption('No network or paid request was made. This does not verify network access, remaining allowance, a new upload’s token fit, or completion of a live review.')
    messages={
        'NEBIUS_API_KEY_NOT_CONFIGURED':'Add NEBIUS_API_KEY to the local .env file.',
        'PROVIDER_MODEL_SCHEMA_RATE_AND_FULL_INPUT_FIT_UNVERIFIED':'Provider setup and exact request-size verification are still required.',
        'EXACT_EXTRACTION_PACKET_VERIFICATION_REQUIRED':'The extraction request still needs exact token-size verification.',
        'EXTRACTOR_LOCAL_COMPONENTS_EXCEED_APPROVED_LIVE_INPUT_CAP':'The local extraction-size estimate exceeds its limit; exact provider verification is needed.',
        'SYNTHESIZER_LOCAL_COMPONENTS_EXCEED_APPROVED_LIVE_INPUT_CAP':'The local synthesis-size estimate exceeds its limit; review its request fit.',
    }
    for blocker in result.get('blockers',[]):st.write('• '+messages.get(blocker,'A local configuration check requires attention; see technical details.'))
    st.caption('Run this check again after changing configuration.')
    with st.expander('Technical readiness details',expanded=False):
        st.code(json.dumps(result,indent=2,ensure_ascii=False),language='text',wrap_lines=True,height=320)
