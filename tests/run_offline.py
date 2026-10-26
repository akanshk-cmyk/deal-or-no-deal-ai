"""Run only the stdlib M1 subset with Python 3.12; never installs dependencies.

The normal pytest command remains the full required M1 suite. This runner is an
explicit partial check, not a missing-dependency skip or a completed M1 gate.
"""

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def main():
    if sys.version_info[:2] != (3, 12):
        raise SystemExit("This project check requires the approved Python 3.12 interpreter.")
    modules = ["tests.unit.test_context_identity", "tests.unit.test_state_codec",
               "tests.unit.test_budget_boundaries", "tests.unit.test_review_basis",
               "tests.integration.test_admission"]
    suite = unittest.defaultTestLoader.loadTestsFromNames(modules)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
