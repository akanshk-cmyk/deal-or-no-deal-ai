"""Explicit SQLite foundation and schema-known codec (SPEC-007/011).

Low-level repository primitives are not authorization APIs. Review services must
validate simulated capabilities, scope and current gates before submitting writes.
"""

from contextlib import contextmanager
from dataclasses import asdict, dataclass, fields, replace
from decimal import Decimal
import json
from pathlib import Path
import sqlite3

from .budgets import Ledger, Usage
from .context import FINANCIAL_FIELDS, InputError, canonical_json, exact_confidence, fingerprint, primitive, _pairs


CODEC = "STATE-CODEC-1.0"
SCHEMA = "CONTRACT-1.0"
DATABASE_SCHEMA = SCHEMA + "/" + CODEC + "/M1-SQLITE-1.0"


class RunBusy(ValueError):
    pass


class OperationConflict(ValueError):
    pass


class StaleRecord(ValueError):
    pass


@dataclass(frozen=True)
class StateSnapshot:
    """M1 typed compatibility snapshot, not the full future deal graph state."""

    workspace_id: str
    deal_id: str
    review_id: str
    run_id: str
    thread_id: str
    input_revision: int
    confidence: Decimal | None
    financial_inputs: dict[str, Decimal | None]
    risk_score: Decimal | None
    source_text: str
    references: list[str]
    conditions: list[str]
    panel_refs: list[str]
    report_markdown: str | None

    def __post_init__(self):
        for name in ("workspace_id", "deal_id", "review_id", "run_id", "thread_id"):
            value = getattr(self, name)
            if type(value) is not str or not value.strip():
                raise InputError("INVALID_STATE_IDENTITY")
        if type(self.input_revision) is not int or self.input_revision < 1:
            raise InputError("INVALID_REVISION")
        if self.confidence is not None:
            exact_confidence(self.confidence)
        if type(self.financial_inputs) is not dict or not self.financial_inputs.keys() <= set(FINANCIAL_FIELDS):
            raise InputError("INVALID_FINANCIAL_FIELDS")
        for value in self.financial_inputs.values():
            if value is not None and (not isinstance(value, Decimal) or not value.is_finite()):
                raise InputError("EXACT_FINANCIAL_VALUE_REQUIRED")
        if self.risk_score is not None and (not isinstance(self.risk_score, Decimal)
                or not self.risk_score.is_finite() or not 0 <= self.risk_score <= 100):
            raise InputError("INVALID_RISK_SCORE")
        if type(self.source_text) is not str or (
            self.report_markdown is not None and type(self.report_markdown) is not str
        ):
            raise InputError("INVALID_STATE_TEXT")
        for value in (self.references, self.conditions, self.panel_refs):
            if type(value) is not list or any(type(item) is not str for item in value):
                raise InputError("INVALID_STATE_LIST")
        primitive(asdict(self))


def encode_state(state: StateSnapshot) -> dict:
    if type(state) is not StateSnapshot:
        raise InputError("KNOWN_STATE_SCHEMA_REQUIRED")
    # Revalidate mutable children rather than trusting dataclass construction alone.
    state = StateSnapshot(**asdict(state))
    return {"state_codec_version": CODEC, "schema_version": SCHEMA,
            "snapshot": primitive(asdict(state))}


def _saved_decimal(value):
    if type(value) is not str:
        raise InputError("SAVED_DECIMAL_STRING_REQUIRED")
    number = Decimal(value)
    if not number.is_finite() or primitive(number) != value:
        raise InputError("INVALID_SAVED_DECIMAL")
    return number


def decode_state(saved: dict) -> StateSnapshot:
    if type(saved) is not dict or set(saved) != {"state_codec_version", "schema_version", "snapshot"}:
        raise InputError("INVALID_SAVED_STATE")
    if saved["state_codec_version"] != CODEC or saved["schema_version"] != SCHEMA:
        raise InputError("INCOMPATIBLE_STATE_VERSION")
    source = saved["snapshot"]
    if type(source) is not dict or set(source) != {field.name for field in fields(StateSnapshot)}:
        raise InputError("INVALID_SAVED_STATE_SCHEMA")
    data = dict(source)
    for name in ("confidence", "risk_score"):
        if data[name] is not None:
            data[name] = _saved_decimal(data[name])
    if type(data["financial_inputs"]) is not dict:
        raise InputError("INVALID_FINANCIAL_FIELDS")
    data["financial_inputs"] = {key: None if value is None else _saved_decimal(value)
                                for key, value in data["financial_inputs"].items()}
    return StateSnapshot(**data)


def apply_patch(state: StateSnapshot, patch: dict) -> StateSnapshot:
    allowed = {field.name for field in fields(StateSnapshot)} - {
        "workspace_id", "deal_id", "review_id", "run_id", "thread_id", "input_revision"
    }
    if not patch.keys() <= allowed:
        raise InputError("IMMUTABLE_IDENTITY_OR_UNKNOWN_PATCH")
    return replace(state, **patch)


@dataclass(frozen=True)
class RecordWrite:
    key: str
    kind: str
    payload: dict
    expected_version: int = 0


@dataclass(frozen=True)
class Receipt:
    operation_id: str
    payload_digest: str
    state: str
    duplicate: bool


class Store:
    def __init__(self, path: Path):
        self.path = path.resolve()

    @contextmanager
    def connection(self):
        connection = sqlite3.connect(self.path, timeout=5, isolation_level=None)
        connection.row_factory = sqlite3.Row
        try:
            connection.execute("PRAGMA foreign_keys=ON")
            connection.execute("PRAGMA busy_timeout=5000")
            yield connection
        finally:
            connection.close()

    @contextmanager
    def transaction(self):
        with self.connection() as connection:
            connection.execute("BEGIN IMMEDIATE")
            try:
                yield connection
                connection.execute("COMMIT")
            except BaseException:
                connection.execute("ROLLBACK")
                raise

    def initialize(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.transaction() as connection:
            tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if "app_meta" in tables:
                row = connection.execute("SELECT value FROM app_meta WHERE key='schema'").fetchone()
                if row is None or row[0] != DATABASE_SCHEMA:
                    raise InputError("INCOMPATIBLE_DATABASE_VERSION")
            elif any(name.startswith("app_") for name in tables):
                raise InputError("UNVERSIONED_APPLICATION_DATABASE")
            connection.execute("CREATE TABLE IF NOT EXISTS app_meta(key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            connection.execute("INSERT OR IGNORE INTO app_meta VALUES('schema', ?)", (DATABASE_SCHEMA,))
            connection.execute("""CREATE TABLE IF NOT EXISTS app_operations(
                operation_id TEXT PRIMARY KEY, payload_digest TEXT NOT NULL,
                scope_payload TEXT NOT NULL, command_kind TEXT NOT NULL,
                review_id TEXT NOT NULL, reservation_id TEXT,
                state TEXT NOT NULL CHECK(state IN ('HELD','RECOVERY_REQUIRED','RELEASED')),
                active_execution_key TEXT UNIQUE,
                CHECK((state='RELEASED' AND active_execution_key IS NULL) OR
                      (state!='RELEASED' AND active_execution_key='LOCAL_EXECUTION'))
            )""")
            connection.execute("""CREATE TABLE IF NOT EXISTS app_records(
                record_key TEXT PRIMARY KEY, kind TEXT NOT NULL,
                version INTEGER NOT NULL CHECK(version>0), payload TEXT NOT NULL)""")
            connection.execute("""CREATE TABLE IF NOT EXISTS app_record_history(
                record_key TEXT NOT NULL, kind TEXT NOT NULL,
                version INTEGER NOT NULL CHECK(version>0), payload TEXT NOT NULL,
                PRIMARY KEY(record_key,version))""")

    @staticmethod
    def _assert_review_open(connection, review_id):
        if review_id and connection.execute("SELECT 1 FROM app_records WHERE record_key=?",
                                           ("quarantine-review:" + review_id,)).fetchone():
            raise InputError("LIVE_REVIEW_QUARANTINED")

    def assert_review_open(self, review_id):
        with self.connection() as connection:
            self._assert_review_open(connection, review_id)

    @staticmethod
    def _write(connection, write: RecordWrite):
        if write.kind in {"LIVE_CONTEXT", "LIVE_PROGRESS", "BUDGET_LEDGER", "PAID_GENERATION_REQUEST", "LIVE_REVIEW_REQUEST", "LIVE_PROVIDER_REQUEST"}:
            scope = write.payload.get("context", write.payload).get("scope", {})
            Store._assert_review_open(connection, scope.get("review_id") or write.payload.get("review_id"))
        if type(write.expected_version) is not int or write.expected_version < 0:
            raise InputError("INVALID_RECORD_VERSION")
        row = connection.execute("SELECT version,kind FROM app_records WHERE record_key=?", (write.key,)).fetchone()
        version = 0 if row is None else row["version"]
        if version != write.expected_version or (row is not None and row["kind"] != write.kind):
            raise StaleRecord("RECORD_VERSION_CONFLICT")
        encoded = canonical_json(write.payload)
        connection.execute("INSERT INTO app_record_history VALUES(?,?,?,?)",
                           (write.key, write.kind, version + 1, encoded))
        connection.execute("""INSERT INTO app_records VALUES(?,?,?,?)
            ON CONFLICT(record_key) DO UPDATE SET version=excluded.version,payload=excluded.payload""",
            (write.key, write.kind, version + 1, encoded))

    def put_record(self, write: RecordWrite):
        """Metadata-only repository write; caller must enforce its domain guard."""
        with self.transaction() as connection:
            self._write(connection, write)

    def get_record(self, key: str) -> tuple[int, dict] | None:
        with self.connection() as connection:
            row = connection.execute("SELECT version,payload FROM app_records WHERE record_key=?", (key,)).fetchone()
            if row is None:
                return None
            # Saved records are not subject to model-content size/collection limits.
            return row["version"], json.loads(row["payload"], object_pairs_hook=_pairs)

    def admit(self, operation_id: str, scope: dict, command: dict, *,
              writes: tuple[RecordWrite, ...] = (), reservation: tuple[str, Usage, str] | None = None,
              expected_records: tuple[tuple[str, int], ...] = ()) -> Receipt:
        if not scope.get("review_id") or type(command.get("action")) is not str or not command["action"].strip():
            raise InputError("SCOPED_COMMAND_IDENTITY_REQUIRED")
        digest = fingerprint("COMMAND", {"scope": scope, "command": command,
            "writes": [asdict(write) for write in writes],
            "reservation": None if reservation is None else [reservation[0], reservation[1].to_dict(), reservation[2]],
            **({"expected_records": list(expected_records)} if expected_records else {})})
        with self.transaction() as connection:
            self._assert_review_open(connection, scope["review_id"])
            prior = connection.execute("SELECT * FROM app_operations WHERE operation_id=?", (operation_id,)).fetchone()
            if prior:
                if prior["payload_digest"] != digest:
                    raise OperationConflict("OPERATION_CONFLICT")
                return Receipt(operation_id, digest, prior["state"], True)
            for record_key, expected_version in expected_records:
                current=connection.execute("SELECT version FROM app_records WHERE record_key=?",(record_key,)).fetchone()
                if (current[0] if current else 0)!=expected_version:
                    raise StaleRecord("STALE_TRANSACTIONAL_REVIEW_VERSION")
            if connection.execute("SELECT 1 FROM app_operations WHERE active_execution_key IS NOT NULL").fetchone():
                raise RunBusy("RUN_BUSY")
            connection.execute("""INSERT INTO app_operations
                (operation_id,payload_digest,scope_payload,command_kind,review_id,reservation_id,state,active_execution_key)
                VALUES(?,?,?,?,?,?,'HELD','LOCAL_EXECUTION')""",
                (operation_id, digest, canonical_json(scope), command["action"], scope["review_id"],
                 None if reservation is None else reservation[0]))
            for write in writes:
                self._write(connection, write)
            if reservation is not None:
                review_id = scope["review_id"]
                key = "ledger:" + review_id
                row = connection.execute("SELECT version,payload FROM app_records WHERE record_key=?", (key,)).fetchone()
                ledger = Ledger(review_id) if row is None else Ledger.from_dict(json.loads(row["payload"]))
                ledger = ledger.reserve(reservation[0], reservation[1], purpose=reservation[2])
                self._write(connection, RecordWrite(key, "BUDGET_LEDGER", ledger.to_dict(), 0 if row is None else row["version"]))
        return Receipt(operation_id, digest, "HELD", False)

    def assert_claim(self, receipt: Receipt, *, connection=None):
        if connection is None:
            with self.connection() as current:
                return self.assert_claim(receipt, connection=current)
        if receipt.duplicate:
            raise InputError("DUPLICATE_RECEIPT_IS_READ_ONLY")
        row = connection.execute("SELECT * FROM app_operations WHERE operation_id=?", (receipt.operation_id,)).fetchone()
        if row is None or row["payload_digest"] != receipt.payload_digest or row["state"] != "HELD":
            raise InputError("EXECUTION_CLAIM_NOT_HELD")
        self._assert_review_open(connection, row["review_id"])

    def release(self, receipt: Receipt, *, confirmed_idle: bool):
        if confirmed_idle is not True:
            raise InputError("CONFIRMED_IDLE_REQUIRED")
        with self.transaction() as connection:
            row = connection.execute("SELECT * FROM app_operations WHERE operation_id=?", (receipt.operation_id,)).fetchone()
            if row is None or row["payload_digest"] != receipt.payload_digest or row["state"] == "RECOVERY_REQUIRED":
                raise InputError("EXPLICIT_RECOVERY_REQUIRED")
            connection.execute("UPDATE app_operations SET state='RELEASED',active_execution_key=NULL WHERE operation_id=?", (receipt.operation_id,))

    def mark_unknown(self, receipt: Receipt):
        with self.transaction() as connection:
            row = connection.execute("SELECT * FROM app_operations WHERE operation_id=?", (receipt.operation_id,)).fetchone()
            if row is None or row["payload_digest"] != receipt.payload_digest or row["state"] == "RELEASED":
                raise InputError("EXECUTION_CLAIM_NOT_HELD")
            if row["reservation_id"] is not None:
                key = "ledger:" + row["review_id"]
                saved = connection.execute("SELECT version,payload FROM app_records WHERE record_key=?", (key,)).fetchone()
                if saved is None:
                    raise InputError("RESERVATION_LEDGER_MISSING")
                ledger = Ledger.from_dict(json.loads(saved["payload"]))
                if row["reservation_id"] in ledger.reservations:
                    updated = ledger.mark_unknown(row["reservation_id"])
                    if updated != ledger:
                        self._write(connection, RecordWrite(key, "BUDGET_LEDGER", updated.to_dict(), saved["version"]))
            connection.execute("UPDATE app_operations SET state='RECOVERY_REQUIRED' WHERE operation_id=?", (receipt.operation_id,))

    def reconcile_idle(self, receipt: Receipt, *, evidence_ref: str, administrator_authorized: bool):
        """Internal primitive after explicit guarded technical reconciliation.

        Never invoked automatically by age, restart or PID lookup. Does not release
        unknown provider ledger reservations; those need separate usage evidence.
        """
        if administrator_authorized is not True or not evidence_ref.strip():
            raise InputError("AUTHORIZED_RECOVERY_EVIDENCE_REQUIRED")
        with self.transaction() as connection:
            row = connection.execute("SELECT * FROM app_operations WHERE operation_id=?", (receipt.operation_id,)).fetchone()
            if row is None or row["payload_digest"] != receipt.payload_digest or row["state"] != "RECOVERY_REQUIRED":
                raise InputError("RECOVERY_IDENTITY_MISMATCH")
            self._write(connection, RecordWrite("recovery:" + receipt.operation_id, "TECHNICAL_RECOVERY", {"evidence_ref": evidence_ref}))
            connection.execute("UPDATE app_operations SET state='RELEASED',active_execution_key=NULL WHERE operation_id=?", (receipt.operation_id,))
