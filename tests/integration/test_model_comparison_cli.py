"""Explicit preparation writes ignored artifacts; never runs a model."""

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from deal_or_no_deal_ai.context import InputError
from deal_or_no_deal_ai.model_comparison import prepare_comparison
from tests.support import OfflineTest, ROOT
from tools import prepare_model_comparison as command


class ModelComparisonCLITests(OfflineTest):
    def test_content_addressed_artifact_is_reused_and_altered_history_is_not_overwritten(self):
        report = prepare_comparison(ROOT)
        with TemporaryDirectory() as folder:
            root = Path(folder)
            for _ in range(2):
                output = StringIO()
                with patch.object(command, "ROOT", root), patch.object(command, "prepare_comparison", return_value=report), \
                        patch("sys.argv", ["prepare_model_comparison"]), redirect_stdout(output):
                    self.assertEqual(command.main(), 0)
                summary = json.loads(output.getvalue())
                self.assertEqual(summary["status"], "PREPARED_OFFLINE_NOT_RUN")
                self.assertNotIn("FIN-P1", output.getvalue())
            artifact = root / summary["report"]
            self.assertTrue(artifact.is_file())
            artifact.write_text("Changed historical artifact", encoding="utf-8")
            with patch.object(command, "ROOT", root), patch.object(command, "prepare_comparison", return_value=report), \
                    patch("sys.argv", ["prepare_model_comparison"]), self.assertRaisesRegex(InputError, "ARTIFACT_CHANGED"):
                command.main()
            self.assertEqual(artifact.read_text(encoding="utf-8"), "Changed historical artifact")

    def test_no_live_or_arbitrary_output_flag_is_available(self):
        with patch("sys.argv", ["prepare_model_comparison", "--live"]), \
                patch.object(command, "prepare_comparison", side_effect=AssertionError("NO_PREPARATION")), \
                self.assertRaisesRegex(InputError, "NO_EXECUTION_FLAGS"):
            command.main()
