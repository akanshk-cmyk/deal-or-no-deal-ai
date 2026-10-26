"""Explicit read-only readiness; never print a secret or invoke a provider."""
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from deal_or_no_deal_ai.live_setup import readiness

if __name__ == "__main__":
    print(json.dumps(readiness(ROOT), indent=2))
