"""Explicit Nebius chat transport with durable shared allowance; no import dispatch."""
from dataclasses import asdict
from decimal import Decimal
import json
from pathlib import Path
import tomllib
from urllib.request import Request, build_opener, HTTPRedirectHandler
from uuid import UUID
import time

from .command_center import workspace_id
from .context import InputError, fingerprint, canonical_decimal
from .configuration import load_configuration
from .live_setup import read_api_key
from .provider import prepare_request, normalize_response, MODELS, stage_caps
from .storage import Store, RecordWrite
from .budgets import Ledger, Usage


# Three total submitted generation requests, not three extra retries. This is
# separate from the five-attempt aggregate ledger limit and evaluator limits.
# Keep it out of the verified provider profile to preserve existing request IDs.
LIVE_GENERATION_REQUEST_LIMIT = 3


def _generation_request_count(store, review_id):
    with store.connection() as connection:
        rows = connection.execute(
            "SELECT payload FROM app_records WHERE kind='PAID_GENERATION_REQUEST'").fetchall()
    return sum(json.loads(row[0]).get("scope", {}).get("review_id") == review_id for row in rows)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise InputError("PROVIDER_REDIRECT_REJECTED")


def _post(payload, key):
    request = Request("https://api.tokenfactory.nebius.com/v1/chat/completions",
        data=json.dumps(payload, ensure_ascii=False, allow_nan=False).encode(),
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + key}, method="POST")
    with build_opener(NoRedirect).open(request, timeout=45) as response:
        raw = response.read(262145)
    if len(raw) > 262144:
        raise InputError("PROVIDER_RESPONSE_LIMIT")
    return json.loads(raw)


def dispatch_generation(root, operation_id, review_id, *, stage, instruction, context, verified_input_tokens, _held_receipt=None):
    """Only explicit verified caller. No CLI or app path currently asserts readiness."""
    root = Path(root); config = load_configuration(root)
    if str(UUID(operation_id)) != operation_id or str(UUID(review_id)) != review_id:
        raise InputError("PROVIDER_CANONICAL_ID_REQUIRED")
    with (root / "config/live_smoke.toml").open("rb") as stream:
        profile = tomllib.load(stream)
    if (profile["version"] != "LIVE-SMOKE-1.0" or profile["total_allowance_usd"] != "0.10"
        or profile["generation_model"] != MODELS[0] or profile["provider_contract_verified"] is not True):
        raise InputError("VERIFIED_PROVIDER_CONTRACT_REQUIRED")
    if profile.get("token_count_strategy") != "PROVIDER_VERIFIED_WHOLE_REQUEST":
        raise InputError("VERIFIED_FULL_REQUEST_TOKEN_ACCOUNTING_REQUIRED")
    rates = tuple(Decimal(profile[key]) for key in ("input_usd_per_million", "output_usd_per_million"))
    if any(not r.is_finite() or r <= 0 for r in rates) or not profile.get("rates_verified_on"):
        raise InputError("VERIFIED_POSITIVE_PROVIDER_RATES_REQUIRED")
    token_profile = profile.get("prompt_profile")
    caps = stage_caps(token_profile)
    if token_profile is not None:
        expected = {"extraction_input_cap": 4000, "extraction_output_cap": 1000, "synthesis_input_cap": 2500, "synthesis_output_cap": 650, "aggregate_input_cap": 8000, "aggregate_output_cap": 2000, "correction_input_reserve": 1500, "correction_output_reserve": 350}
        if any(profile.get(k) != v for k, v in expected.items()):
            raise InputError("LIVE_PROFILE_LIMITS_CHANGED")
    payload = prepare_request(model_id=MODELS[0], stage=stage, instruction=instruction, context=context,
        verified_input_tokens=verified_input_tokens, max_output_tokens=caps[stage][1], profile=token_profile)
    digest = fingerprint("LIVE_GENERATION_REQUEST", dict(payload=payload, review_id=review_id, profile=profile))
    key = read_api_key(root)
    store = Store(config.database); store.initialize()
    store.assert_review_open(review_id)
    result_key = "paid-result:" + operation_id
    prior = store.get_record(result_key)
    if prior:
        if prior[1]["request_digest"] != digest:
            raise InputError("PAID_OPERATION_CONFLICT")
        return prior[1]
    # Submitted requests include uncertain outcomes. Cached results above do not
    # spend another attempt; a fresh operation ID cannot bypass this review cap.
    if _generation_request_count(store, review_id) >= LIVE_GENERATION_REQUEST_LIMIT:
        raise InputError("LIVE_GENERATION_REQUEST_LIMIT_REACHED")
    budget_key = "paid-allowance:" + profile["allowance_id"]
    saved = store.get_record(budget_key)
    version, budget = saved if saved else (0, dict(limit_usd="0.10", committed_usd="0", reservations={}))
    maximum = (rates[0] * caps[stage][0] + rates[1] * caps[stage][1]) / Decimal(1000000)
    total = Decimal(budget["committed_usd"]) + sum((Decimal(v) for v in budget["reservations"].values()), Decimal(0))
    if budget["limit_usd"] != "0.10" or total + maximum > Decimal("0.10") or operation_id in budget["reservations"]:
        raise InputError("SHARED_ALLOWANCE_EXHAUSTED_OR_UNCERTAIN")
    reserved = {**budget, "reservations": {**budget["reservations"], operation_id: canonical_decimal(maximum)}}
    scope = dict(workspace_id=workspace_id(root), review_id=review_id)
    request_write=RecordWrite("paid-request:"+operation_id,"PAID_GENERATION_REQUEST",
        dict(request_digest=digest,scope=scope,payload=payload,verified_input_tokens=verified_input_tokens,prompt_profile=token_profile),0)
    reservation_usage = Usage(input_tokens=caps[stage][0], output_tokens=caps[stage][1], attempts=1, active_ms=45000, cost_usd=maximum)
    if _held_receipt is None:
        receipt = store.admit(operation_id, scope, dict(action="LIVE_GENERATION", digest=digest),
            writes=(RecordWrite(budget_key, "PAID_ALLOWANCE", reserved, version),request_write),
            reservation=(operation_id, reservation_usage, "ORDINARY"))
        if receipt.duplicate:
            raise InputError("PAID_OPERATION_REQUIRES_RECONCILIATION")
    else:
        receipt = _held_receipt
        store.assert_claim(receipt)
        with store.connection() as connection:
            row = connection.execute("SELECT scope_payload FROM app_operations WHERE operation_id=?", (receipt.operation_id,)).fetchone()
        if row is None or json.loads(row[0]).get("review_id") != review_id:
            raise InputError("PAID_PARENT_SCOPE_MISMATCH")
        ledger_version, ledger_data = store.get_record("ledger:" + review_id)
        ledger = Ledger.from_dict(ledger_data).reserve(operation_id, reservation_usage)
        with store.transaction() as connection:
            store.assert_claim(receipt, connection=connection)
            store._write(connection, RecordWrite(budget_key, "PAID_ALLOWANCE", reserved, version))
            store._write(connection, request_write)
            store._write(connection, RecordWrite("ledger:" + review_id, "BUDGET_LEDGER", ledger.to_dict(), ledger_version))
    try:
        started = time.monotonic()
        outcome = normalize_response(_post(payload, key), model_id=MODELS[0], stage=stage, profile=token_profile)
        elapsed = max(1, int((time.monotonic() - started) * 1000))
        if outcome.prompt_tokens is None or outcome.completion_tokens is None or outcome.usage_status == "UNKNOWN":
            raise InputError("PAID_USAGE_RECONCILIATION_REQUIRED")
        actual = (rates[0] * outcome.prompt_tokens + rates[1] * outcome.completion_tokens) / Decimal(1000000)
        if actual > maximum or outcome.reason == "PROVIDER_USAGE_EXCEEDS_STAGE_CAP":
            raise InputError("PAID_USAGE_EXCEEDS_RESERVATION")
        version, current = store.get_record(budget_key)
        settled = {**current, "committed_usd": canonical_decimal(Decimal(current["committed_usd"]) + actual),
            "reservations": {k: v for k, v in current["reservations"].items() if k != operation_id}}
        result = dict(request_digest=digest, purpose="GENERATION", stage=stage,
            response={**asdict(outcome), "wire": None if outcome.wire is None else outcome.wire.model_dump()},
            actual_provider_response=True, cost_at_verified_rates_usd=canonical_decimal(actual), human_support=False)
        with store.transaction() as connection:
            store.assert_claim(receipt, connection=connection)
            ledger_version, ledger_data = store.get_record("ledger:" + review_id)
            ledger = Ledger.from_dict(ledger_data).settle(operation_id, Usage(input_tokens=outcome.prompt_tokens,
                output_tokens=outcome.completion_tokens, attempts=1, active_ms=elapsed, cost_usd=actual))
            store._write(connection, RecordWrite(budget_key, "PAID_ALLOWANCE", settled, version))
            store._write(connection, RecordWrite("ledger:" + review_id, "BUDGET_LEDGER", ledger.to_dict(), ledger_version))
            store._write(connection, RecordWrite(result_key, "PAID_GENERATION_RESULT", result))
        if _held_receipt is None:
            store.release(receipt, confirmed_idle=True)
        return result
    except BaseException:
        # Retain maximum reservation and active claim; never retry an uncertain call.
        store.assert_review_open(review_id)
        if _held_receipt is not None:
            saved_ledger=store.get_record("ledger:"+review_id)
            if saved_ledger and operation_id in saved_ledger[1]["reservations"]:
                ledger=Ledger.from_dict(saved_ledger[1]).mark_unknown(operation_id)
                store.put_record(RecordWrite("ledger:"+review_id,"BUDGET_LEDGER",ledger.to_dict(),saved_ledger[0]))
        store.mark_unknown(receipt)
        raise InputError("PAID_DISPATCH_REQUIRES_RECONCILIATION") from None
