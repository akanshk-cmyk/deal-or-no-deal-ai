"""Local educational entry point. Importing does not execute the application."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

if __name__ == "__main__":
    from deal_or_no_deal_ai.ui.command_center import main
    main(ROOT)
