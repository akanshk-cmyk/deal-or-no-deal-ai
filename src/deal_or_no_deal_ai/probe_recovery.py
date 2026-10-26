"""Prepared exact-request isolation; activation requires explicit human approval."""
import json
from datetime import datetime,timezone
from .context import InputError
from .storage import RecordWrite

TARGET='fbb6ba9d-ba4b-5c5a-b0b8-11f350b413ea'
REVIEW='74985f6f-5825-5e39-9ae9-ceaf13f36e35'
RESERVATION='0.0262147'


def isolate_probe(store,actor,*,expected_versions,approved=False):
    if approved is not True or actor.persona!='Administrator':
        raise InputError('EXPLICIT_PROBE_ISOLATION_APPROVAL_REQUIRED')
    with store.transaction() as connection:
        def read(key):
            row=connection.execute('SELECT version,payload FROM app_records WHERE record_key=?',(key,)).fetchone()
            if not row:raise InputError('PROBE_RECOVERY_RECORD_REQUIRED')
            return row['version'],json.loads(row['payload'])
        rv,request=read('evaluation-paid-request:'+TARGET)
        av,allowance=read('paid-allowance:first-synthetic-010')
        scope=request['scope']
        if expected_versions!=dict(request=rv,allowance=av):raise InputError('PROBE_RECOVERY_STALE_VERSION')
        claim=connection.execute('SELECT * FROM app_operations WHERE operation_id=?',(TARGET,)).fetchone()
        payload=request.get('payload',{})
        if (scope.get('workspace_id')!=actor.workspace_id or scope.get('review_id')!=REVIEW
            or scope.get('purpose')!='INPUT_TOKEN_PROBE' or payload.get('max_tokens')!=1
            or claim is None or claim['state']!='RECOVERY_REQUIRED'
            or claim['review_id']!=REVIEW or claim['active_execution_key']!='LOCAL_EXECUTION'
            or json.loads(claim['scope_payload'])!=scope
            or allowance.get('reservations',{}).get(TARGET)!=RESERVATION
            or request.get('maximum_cost_usd')!=RESERVATION
            or connection.execute('SELECT 1 FROM app_records WHERE record_key=?',('evaluation-paid-result:'+TARGET,)).fetchone()):
            raise InputError('EXACT_UNKNOWN_PROBE_REQUIRED')
        audit=dict(version='PROBE-ISOLATION-1.0',operation_id=TARGET,scope=scope,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),reviewer_role=actor.persona,
            attribution='SIMULATED_ADMINISTRATOR',retained_reservation_usd=RESERVATION,
            provider_usage_status='UNKNOWN',provider_usage_reconciled=False,replay_permitted=False,
            expected_versions=expected_versions,request_digest=request['request_digest'],
            reason='Explicitly approved abandonment of this exact sizing attempt; preserve unknown cost and prevent replay or late publication. Not a credit decision.')
        store._write(connection,RecordWrite('quarantine-review:'+REVIEW,'LIVE_QUARANTINE',audit,0))
        connection.execute("UPDATE app_operations SET state='RELEASED',active_execution_key=NULL WHERE operation_id=?",(TARGET,))
        return audit
