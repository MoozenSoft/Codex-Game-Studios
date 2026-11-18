"""验证迁移来源覆盖与启用依赖，防止漏迁移或把未验证项当作通过。"""

import json
import hashlib
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
INVENTORY = ROOT / "studio-tests/migration-inventory.json"
ALIASES = {"help": "next-step", "settings": "project-settings", "changelog": "write-changelog"}


class InventoryTests(unittest.TestCase):
    def entries(self):
        self.assertTrue(INVENTORY.is_file(), "缺少迁移清单，不能证明全部来源已登记")
        document = json.loads(INVENTORY.read_text(encoding="utf-8"))
        self.assertEqual(document["schema_version"], 1)
        return document["entries"]

    def test_inventory_covers_sources(self):
        entries = self.entries()
        sources = [item["source"] for item in entries]
        self.assertEqual(len(sources), len(set(sources)), "同一来源重复登记")
        document = json.loads(INVENTORY.read_text(encoding="utf-8"))
        expected = set(document['source_files'])
        expected.update(p.relative_to(ROOT).as_posix() for p in (ROOT / ".claude").rglob("*") if p.is_file())
        expected.update({"CLAUDE.md", "src/CLAUDE.md", "design/CLAUDE.md", "docs/CLAUDE.md", "studio-tests/CLAUDE.md", ".worktreeinclude"})
        self.assertFalse(expected - set(sources), f"漏登记来源：{sorted(expected - set(sources))}")
        for item in entries:
            with self.subTest(source=item["source"]):
                self.assertIn(item["disposition"], ("migrate", "retire"))
                self.assertIn(item["status"], ("pending", "active", "retired"))
                original = item['source'].split('#', 1)[0]
                self.assertEqual(item['source_sha256'], document['source_files'][original])
                if item['status'] == 'pending':
                    self.assertTrue((ROOT / original).is_file(), '待迁移来源不能提前删除')
                if item["disposition"] == "migrate":
                    self.assertTrue(item["target"], "迁移项必须有计划目标")

    def test_formal_skills_match_catalog(self):
        entries = self.entries()
        catalog = (ROOT / "studio-tests/catalog.yaml").read_text(encoding="utf-8")
        skill_section = re.split(r"(?m)^agents:", catalog)[0]
        expected = set(re.findall(r"(?m)^  - name: ([\w-]+)", skill_section))
        actual = {Path(item["source"]).parent.name for item in entries
                  if item["kind"] == "skill" and item["disposition"] == "migrate"}
        self.assertEqual(actual, expected)
        agents = {Path(item["source"]).stem for item in entries if item["kind"] == "agent"}
        self.assertEqual(agents, set(re.findall(r"(?m)^  - name: ([\w-]+)", catalog.split("\nagents:", 1)[1])))

    def test_retirement_has_replacement(self):
        entries = {item["source"]: item for item in self.entries()}
        for old, new in ALIASES.items():
            with self.subTest(alias=old):
                item = entries[f".claude/skills/{old}/SKILL.md"]
                self.assertEqual(item["disposition"], "retire")
                self.assertEqual(item["replacement"], f".agents/skills/{new}/SKILL.md")
                self.assertTrue(item["reason"])
        for item in entries.values():
            if item["disposition"] == "retire":
                self.assertTrue(item.get("replacement") or item.get("reason"))

    def test_hook_events_have_explicit_dispositions(self):
        document = json.loads(INVENTORY.read_text(encoding="utf-8"))
        expected = {f".claude/settings.json#hooks/{event}" for event in document['source_hooks']}
        actual = {item["source"] for item in self.entries() if item["kind"] == "hook_event"}
        self.assertEqual(actual, expected)

    def test_source_snapshot_survives_retirement_without_git_history(self):
        document = json.loads(INVENTORY.read_text(encoding='utf-8'))
        snapshot = document['source_files']
        self.assertEqual(set(snapshot), {item['source'].split('#', 1)[0] for item in document['entries']})
        self.assertTrue(all(re.fullmatch(r'[a-f0-9]{64}', value) for value in snapshot.values()))
        payload=json.dumps(snapshot,sort_keys=True,separators=(',',':')).encode('utf-8')
        self.assertEqual(hashlib.sha256(payload).hexdigest(),document['source_manifest_sha256'])
        self.assertEqual(len(document['source_hooks']),8)

    def test_dependencies_resolve_and_active_targets_exist(self):
        entries = self.entries()
        by_source = {item["source"]: item for item in entries}
        for item in entries:
            with self.subTest(source=item["source"]):
                if item["status"] == "active":
                    self.assertEqual(item["disposition"], "migrate")
                    self.assertTrue((ROOT / item["target"]).is_file())
                for dependency in item["dependencies"]:
                    self.assertIn(dependency["type"], ("required", "next_step"))
                    self.assertIn(dependency["source"], by_source)
                    if item["status"] == "active" and dependency["type"] == "required":
                        self.assertEqual(by_source[dependency["source"]]["status"], "active")

    def test_pass_claims_require_evidence(self):
        for item in self.entries():
            for layer in ("static", "script", "runtime"):
                state = item["validation"][layer]
                self.assertIn(state, ("not_assessed", "passed", "failed", "not_applicable"))
                if state == "passed":
                    paths = item["evidence"].get(layer, [])
                    self.assertTrue(paths, f"{item['source']} 的 {layer} 缺少通过证据")
                    for path in paths:
                        self.assertTrue((ROOT / path).is_file(), f"证据文件不存在：{path}")

    def test_runtime_matrix_covers_clients_and_catalog_categories(self):
        path = ROOT / "studio-tests/runtime-matrix.json"
        self.assertTrue(path.is_file(), "缺少运行验收矩阵")
        cases = json.loads(path.read_text(encoding="utf-8"))["cases"]
        self.assertEqual(len(cases), len({case["id"] for case in cases}))
        catalog = (ROOT / "studio-tests/catalog.yaml").read_text(encoding="utf-8")
        skills, agents = re.split(r"(?m)^agents:", catalog, maxsplit=1)
        for kind, section in (("skill", skills), ("agent", agents)):
            expected = set(re.findall(r"(?m)^    category: ([\w-]+)", section))
            actual = {case["category"] for case in cases if case["kind"] == kind}
            self.assertEqual(actual, expected)
        for surface in ("app", "cli"):
            for capability in ("discovery", "delegation", "hooks", "interaction", "worktree", "web_core"):
                self.assertTrue(any(case["surface"] == surface and case["capability"] == capability
                                    and case["required"] for case in cases), (surface, capability))
        for case in cases:
            self.assertTrue(case["request"])
            self.assertTrue(case["expected"])
            if case["status"] == "passed":
                self.assertTrue(case["evidence"], case["id"])
                for evidence in case["evidence"]:
                    self.assertTrue((ROOT / evidence).is_file())


if __name__ == "__main__":
    unittest.main()
