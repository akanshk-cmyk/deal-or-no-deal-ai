"""Metadata-only setup check; never load clients, weights, browsers or an index."""

from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from deal_or_no_deal_ai.public_sources import load_reference_profile


def check(root=ROOT):
    profile = load_reference_profile(root)
    packages = {}
    for name in ("pypdf", "crawl4ai", "sentence-transformers", "torch", "transformers", "playwright"):
        try:
            packages[name] = version(name)
        except PackageNotFoundError:
            packages[name] = None
    return dict(evidence_type="SETUP_METADATA_ONLY", python=platform.python_version(),
                packages=packages, mode=profile.mode,
                inspection_adapter="IMPLEMENTED_LOCAL_BYTES_ONLY",
                origin_verification=False, model_weights_verified=False,
                embedding_revision=profile.embedding.artifact_revision,
                embedding_provider=profile.embedding.provider,
                embedding_enabled=profile.embedding.enabled,
                embedding_model=profile.embedding.model_id,
                embedding_capability_status=profile.embedding.capability_status,
                embedding_input_usd_per_million_tokens=profile.embedding.input_usd_per_million_tokens,
                embedding_output_usd_per_million_tokens=profile.embedding.output_usd_per_million_tokens,
                embedding_pricing_checked_on=profile.embedding.pricing_checked_on,
                embedding_dimensions=profile.embedding.dimensions,
                embedding_max_input_tokens=profile.embedding.max_input_tokens,
                embedding_budget_status=profile.embedding.budget_status,
                crawler_enabled=profile.crawler_enabled, index_enabled=profile.storage.index_enabled,
                model_or_browser_loaded=False, requests_sent=0,
                limitation="Installed distributions do not establish browser/model/index or retrieval readiness")


if __name__ == "__main__":
    print(json.dumps(check()))
