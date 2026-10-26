"""Actual bounded PDF inspection, scoped retention, citations and no deal inference."""
from dataclasses import replace
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import subprocess

from pypdf import PdfWriter, PdfReader
from deal_or_no_deal_ai.command_center import workspace_id, list_runs
from deal_or_no_deal_ai.context import InputError, strict_json
from deal_or_no_deal_ai.review import Actor
from deal_or_no_deal_ai.storage import Store, OperationConflict
from deal_or_no_deal_ai.upload_intake import inspect_package, load_package, list_packages
from tests.integration.test_normal_fixture_graph import copy_workspace
from tests.integration.test_human_review_ui import widget
from tests.support import OfflineTest, uid


class UploadIntakeTests(OfflineTest):
    def setUp(self):
        super().setUp()
        folder = TemporaryDirectory(); self.addCleanup(folder.cleanup)
        self.root = Path(folder.name); copy_workspace(self.root)
        self.actor = Actor("Analyst", workspace_id(self.root), frozenset())
        self.operation = uid("upload-intake")
        pack = self.root / "fixtures/development/e-n01"
        manifest = strict_json((pack / "manifest.json").read_bytes())
        self.files = [("source" + str(i) + ".pdf", (pack / s["path"]).read_bytes()) for i, s in enumerate(manifest["sources"])]

    def inspect(self, files=None, **kwargs):
        return inspect_package(self.root, self.actor, self.operation, files if files is not None else self.files,
                               synthetic_confirmed=kwargs.pop("synthetic_confirmed", True), **kwargs)

    def test_actual_retained_inspection_reopen_page_citations_and_no_financial_records(self):
        with patch("deal_or_no_deal_ai.worker.run_normal_fixture", side_effect=AssertionError("NO_GRAPH")):
            package = self.inspect()
        self.assertEqual(package["status"], "INSPECTED_NOT_REVIEWED")
        self.assertEqual(package["page_count"], 5)
        self.assertEqual(package["model_calls"], 0)
        self.assertIsNone(package["subject"])
        self.assertFalse(package["final_ready"])
        for source, (_, raw) in zip(package["sources"], self.files):
            self.assertEqual(source["sha256"], sha256(raw).hexdigest())
            self.assertEqual(source["pages"][0]["page"], 1)
            self.assertIn("upload:" + package["package_id"], source["pages"][0]["ref"])
        with patch("deal_or_no_deal_ai.upload_intake._parse", side_effect=AssertionError("NO_REPARSE_ON_READ_OR_DUPLICATE")):
            self.assertEqual(self.inspect(), package)
            self.assertEqual(load_package(self.root, replace(self.actor, persona="Administrator"), self.operation), package)
        store = Store(self.root / "var/deal_review.sqlite3")
        self.assertFalse(list_runs(store, self.actor))
        self.assertEqual(len(list_packages(self.root, self.actor)), 1)
        with self.assertRaises(OperationConflict):
            self.inspect([(name + ".pdf", raw) for name, raw in self.files])

    def test_invalid_inputs_and_permissions_write_nothing(self):
        for files in ([], self.files * 2, [("x.pdf", b"not a PDF")], [("../x.pdf", self.files[0][1])], [self.files[0], self.files[0]], [("x.pdf", b"%PDF-" + b"x" * 10_000_000)]):
            with self.subTest(files=len(files)), self.assertRaises(InputError):
                self.inspect(files)
        with self.assertRaises(InputError):
            self.inspect(synthetic_confirmed=False)
        for role in ("RiskManager", "ComplianceOfficer", "AuthorizedApprover", "Administrator"):
            with self.assertRaisesRegex(InputError, "PERMISSION"):
                inspect_package(self.root, replace(self.actor, persona=role), self.operation, self.files, synthetic_confirmed=True)
        with self.assertRaises(InputError):
            inspect_package(self.root, replace(self.actor, workspace_id=uid("other")), self.operation, self.files, synthetic_confirmed=True)
        self.assertFalse((self.root / "var").exists())

    def test_corrupt_encrypted_blank_and_page_limits_fail_without_persistence(self):
        blank = PdfWriter(); blank.add_blank_page(width=100, height=100); output = BytesIO(); blank.write(output)
        encrypted = PdfWriter(); encrypted.append(PdfReader(BytesIO(self.files[0][1]))); encrypted.encrypt("secret")
        encrypted_raw = BytesIO(); encrypted.write(encrypted_raw)
        large = PdfWriter()
        for _ in range(11):
            large.add_blank_page(width=100, height=100)
        large_raw = BytesIO(); large.write(large_raw)
        for raw in (b"%PDF-corrupt", output.getvalue(), encrypted_raw.getvalue(), large_raw.getvalue()):
            with self.subTest(size=len(raw)), self.assertRaises(InputError):
                self.inspect([("bad.pdf", raw)])
        self.assertFalse((self.root / "var").exists())

    def test_timeout_and_combined_page_limit(self):
        with patch("deal_or_no_deal_ai.upload_intake.subprocess.run", side_effect=subprocess.TimeoutExpired("parser", 45)):
            with self.assertRaisesRegex(InputError, "TIMEOUT"):
                self.inspect()
        with patch("deal_or_no_deal_ai.upload_intake._parse", return_value=["synthetic text"] * 6):
            with self.assertRaisesRegex(InputError, "PAGE_OR_TEXT_LIMIT"):
                self.inspect()
        self.assertFalse((self.root / "var").exists())

    def test_changed_source_scope_and_partial_persistence_require_recovery(self):
        package = self.inspect()
        with self.assertRaises(InputError):
            load_package(self.root, replace(self.actor, workspace_id=uid("other")), self.operation)
        path = self.root / "var/uploads" / self.actor.workspace_id / package["package_id"] / (package["sources"][0]["sha256"] + ".pdf")
        path.write_bytes(b"changed")
        with self.assertRaisesRegex(InputError, "SOURCE_CHANGED"):
            load_package(self.root, self.actor, self.operation)
        with patch.object(Store, "put_record", side_effect=OSError("simulated write failure")):
            with self.assertRaises(OSError):
                inspect_package(self.root, self.actor, uid("upload-gap"), self.files, synthetic_confirmed=True)
        with self.assertRaisesRegex(InputError, "RECOVERY_REQUIRED"):
            inspect_package(self.root, self.actor, uid("upload-gap"), self.files, synthetic_confirmed=True)

    def test_upload_screen_and_retained_source_explorer(self):
        from tests.integration.test_command_center import CommandCenterTests
        self.inspect()
        app = CommandCenterTests.app(self)
        widget(app.sidebar.radio, "Page").set_value("New Deal").run()
        widget(app.radio, "Intake mode").set_value("Upload New Deal").run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(widget(app.selectbox, "Uploaded source page").value, 1)
        self.assertTrue(any("Citation: upload:" in t.value for t in app.text))
        widget(app.button, "Validate and inspect uploads").click().run()
        self.assertTrue(any("Nothing was saved" in e.value for e in app.error))
        widget(app.sidebar.selectbox, "Demo role").select("Administrator").run()
        self.assertFalse(any(b.label == "Validate and inspect uploads" for b in app.button))
        self.assertEqual(len(app.exception), 0)
