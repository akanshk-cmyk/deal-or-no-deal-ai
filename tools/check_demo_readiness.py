"""Read-only demo preflight. Never loads secrets, starts reviews or calls providers."""
import json
import sqlite3
import tomllib
from datetime import datetime, timezone
from pathlib import Path


def inspect(root):
    root = Path(root)
    config = tomllib.loads((root / "config/app.toml").read_text(encoding="utf-8"))
    database = (root / config["database_path"]).resolve()
    result = dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),
                  evidence="READ_ONLY_LOCAL_PREFLIGHT", configured_source=config["mode"],
                  provider_calls=0, active_execution=[], live_reviews=[],
                  quarantined_reviews=[],
                  saved_answer_evaluations=[], limitations=[
                      "This check does not establish browser usability or live answer quality.",
                      "Human evidence verification and provider usage reconciliation cannot be automated by this check."])
    if not database.is_file():
        result.update(status="DATABASE_UNAVAILABLE", interactive_execution="NOT_VERIFIED")
        return result
    connection = sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)
    try:
        connection.execute("PRAGMA query_only=ON")
        result["active_execution"] = [dict(operation_id=row[0], status=row[1]) for row in
            connection.execute("SELECT operation_id,state FROM app_operations WHERE active_execution_key IS NOT NULL")]
        allowance = connection.execute("SELECT payload FROM app_records WHERE record_key=?",
                                       ("paid-allowance:first-synthetic-010",)).fetchone()
        if allowance:
            payload = json.loads(allowance[0])
            result["allowance"] = {key: payload.get(key) for key in
                                    ("committed_usd", "limit_usd", "reservations")}
        for row in connection.execute("SELECT payload FROM app_records WHERE kind='LIVE_QUARANTINE'"):
            audit = json.loads(row[0])
            result["quarantined_reviews"].append(dict(operation_id=audit["operation_id"],
                review_id=audit["scope"]["review_id"],provider_usage_status=audit["provider_usage_status"],
                retained_reservation_usd=audit["retained_reservation_usd"],replay_permitted=False))
        for key, payload in connection.execute("SELECT record_key,payload FROM app_records WHERE kind='LIVE_PROGRESS'"):
            progress = json.loads(payload)
            operation = key.removeprefix("live-progress:")
            claim = next((r for r in result["active_execution"] if r["operation_id"] == operation), None)
            status = "RECOVERY_REQUIRED" if claim and claim["status"] == "RECOVERY_REQUIRED" else progress.get("status")
            quarantine = next((r for r in result["quarantined_reviews"] if r["operation_id"] == operation),None)
            if quarantine:
                status = "RECOVERY_REQUIRED"
            result["live_reviews"].append(dict(operation_id=operation,
                status=status, persisted_progress_status=progress.get("status"), pending_stage=progress.get("pending_stage"),
                quarantined=bool(quarantine),
                synthesis_available="synthesizer" in progress.get("artifacts", {}),
                report_available=bool(progress.get("report_markdown"))))
    finally:
        connection.close()
    for path in sorted((root / "var/evaluations").glob("answer-quality-*.json")):
        report = json.loads(path.read_text(encoding="utf-8"))
        if report.get("sample", {}).get("application_mode") == "FIXTURE":
            result["saved_answer_evaluations"].append(dict(
                report=path.relative_to(root).as_posix(), status=report.get("result", {}).get("status")))
    result.update(status="BLOCKED_FOR_INTERACTIVE_EXECUTION" if result["active_execution"] else "NO_ACTIVE_EXECUTION_LOCK",
                  interactive_execution="BLOCKED" if result["active_execution"] else "NOT_VERIFIED",
                  read_only_presentation="AVAILABLE_SUBJECT_TO_UI_CHECKS",
                  live_answer_available=any(r["synthesis_available"] for r in result["live_reviews"]))
    return result


if __name__ == "__main__":
    print(json.dumps(inspect(Path(__file__).resolve().parents[1]), indent=2))
