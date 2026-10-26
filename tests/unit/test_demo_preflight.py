"""Demo preflight must preserve recovery and never create application state."""
import json
import sqlite3
from contextlib import closing
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.check_demo_readiness import inspect


def test_missing_database_is_not_created():
    with TemporaryDirectory() as folder:
        root = Path(folder)
        (root / "config").mkdir()
        (root / "config/app.toml").write_text('mode="FIXTURE"\ndatabase_path="var/deal_review.sqlite3"')
        assert inspect(root)["status"] == "DATABASE_UNAVAILABLE"
        assert not (root / "var").exists()


def test_recovery_overrides_stale_running_progress_without_writes():
    with TemporaryDirectory() as folder:
        root = Path(folder)
        (root / "config").mkdir()
        (root / "var").mkdir()
        (root / "config/app.toml").write_text('mode="LIVE"\ndatabase_path="var/deal_review.sqlite3"')
        path = root / "var/deal_review.sqlite3"
        with closing(sqlite3.connect(path)) as connection:
            connection.execute('CREATE TABLE app_operations(operation_id,state,active_execution_key)')
            connection.execute('CREATE TABLE app_records(record_key,kind,payload)')
            connection.execute('INSERT INTO app_operations VALUES(?,?,?)', ('example','RECOVERY_REQUIRED','LOCAL_EXECUTION'))
            connection.execute('INSERT INTO app_records VALUES(?,?,?)', ('live-progress:example','LIVE_PROGRESS',json.dumps(
                dict(status='RUNNING',artifacts={'extractor':{}},pending_stage=None))))
            connection.commit()
        before = path.read_bytes()
        result = inspect(root)
        assert result['status'] == 'BLOCKED_FOR_INTERACTIVE_EXECUTION'
        assert result['live_reviews'][0]['status'] == 'RECOVERY_REQUIRED'
        assert result['live_reviews'][0]['persisted_progress_status'] == 'RUNNING'
        assert result['live_answer_available'] is False
        assert result['provider_calls'] == 0
        assert path.read_bytes() == before
