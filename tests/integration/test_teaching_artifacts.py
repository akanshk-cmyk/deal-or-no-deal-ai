"""Teaching artifacts share graph/read services; no optional notebook installation."""
import ast
import json
from hashlib import sha256
from pathlib import Path
import re
from tempfile import TemporaryDirectory

from deal_or_no_deal_ai.ui.workflow_diagram import workflow_svg
from deal_or_no_deal_ai.worker import run_normal_fixture
from deal_or_no_deal_ai.command_center import get_run, policy_display, source_packet, workspace_id
from deal_or_no_deal_ai.review import Actor
from deal_or_no_deal_ai.storage import Store
from tools.export_html_demo import render
from tests.integration.test_normal_fixture_graph import copy_workspace
from tests.support import OfflineTest, ROOT, uid


class TeachingArtifactTests(OfflineTest):
    def test_notebook_code_is_valid_and_svg_uses_actual_graph_without_dispatch(self):
        notebook = json.loads((ROOT / "notebooks/01_workflow.ipynb").read_text(encoding="utf-8"))
        self.assertEqual(notebook["nbformat"], 4)
        for cell in notebook["cells"]:
            if cell["cell_type"] == "code":
                ast.parse(''.join(cell["source"]))
                self.assertEqual(cell["outputs"], [])
        svg = workflow_svg()
        self.assertIn("Human Review", svg)
        self.assertIn("Review Prepare", svg)
        self.assertIn("<path", svg)
        self.assertNotIn("http://mermaid", svg)
        live_svg=workflow_svg(live=True)
        self.assertIn("Fact Review",live_svg)
        self.assertIn("Evidence Review",live_svg)
        self.assertIn("Human Review",live_svg)
        self.assertIn("stroke-dasharray",live_svg)

    def test_offline_html_has_six_destinations_exact_source_data_and_no_writes(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            copy_workspace(root)
            empty = render(root)
            self.assertIn("No recorded financial analysis", empty)
            self.assertFalse((root / "var/deal_review.sqlite3").exists())
            operation = uid("html-fixture")
            outcome = run_normal_fixture(root, operation)
            store = Store(root / "var/deal_review.sqlite3")
            before = sha256(store.path.read_bytes()).hexdigest()
            html = render(root)
            self.assertEqual(len(re.findall(r'<section id="page-', html)), 6)
            raw = re.search(r'<script type="application/json" id="sources">(.*?)</script>', html, re.S)[1]
            actor = Actor("Analyst", workspace_id(root), frozenset({outcome["scope"]["deal_id"]}))
            run = get_run(store, actor, operation)
            self.assertEqual(json.loads(raw), policy_display(run, source_packet(root, run))["references"])
            self.assertIn("Offline snapshot", html)
            self.assertIn("No human decisions recorded", html)
            self.assertIn("Current approval readiness",html)
            self.assertIn("Pending Review",html)
            self.assertIn("original AI proposal does not clear mandatory blockers",html)
            self.assertIn("Run AI Deal Review",html)
            self.assertEqual(sha256(store.path.read_bytes()).hexdigest(), before)
