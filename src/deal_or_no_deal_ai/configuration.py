"""Explicit offline configuration; importing this module opens no files."""

from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class Configuration:
    workspace: Path
    database: Path
    mode: str = "FIXTURE"


def load_configuration(workspace: Path) -> Configuration:
    root = workspace.resolve(strict=True)
    with (root / "config/app.toml").open("rb") as stream:
        app = tomllib.load(stream)
    with (root / "config/model.toml").open("rb") as stream:
        model = tomllib.load(stream)
    if (app["schema_version"] != "CONTRACT-1.0" or app["state_codec_version"] != "STATE-CODEC-1.0"
            or app["input_profile"] != "INPUT-EDU-1.0"):
        raise ValueError("UNSUPPORTED_CONFIGURATION_VERSION")
    expected_limits = {"input_tokens": 8000, "output_tokens": 2000, "attempts": 5,
        "nodes": 20, "tools": 12, "active_ms": 180000, "operation_ms": 45000, "cost_usd": "0.25"}
    if app["limits"] != expected_limits or any(type(app["limits"][key]) is not type(value)
                                              for key, value in expected_limits.items()):
        raise ValueError("UNAPPROVED_LIMIT_CONFIGURATION")
    if app["mode"] not in ("FIXTURE", "LIVE") or app["tracing_enabled"] is not False:
        raise ValueError("M1_OFFLINE_ONLY")
    if app["automatic_expiry"] is not False or any(
        model[key] is not False
        for key in ("live_enabled", "evaluation_enabled", "hosted_tracing_enabled")
    ):
        raise ValueError("M1_OFFLINE_ONLY")
    database = (root / app["database_path"]).resolve()
    if not database.is_relative_to(root):
        raise ValueError("DATABASE_OUTSIDE_WORKSPACE")
    return Configuration(root, database, app["mode"])
