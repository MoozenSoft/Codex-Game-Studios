"""跨引擎路径规则必须保持原适用范围，避免目录改名后静默漏读。"""
import importlib.util
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]


class RoutingTests(unittest.TestCase):
    def router(self):
        path=ROOT/'.agents/scripts/rule-routing.py'
        self.assertTrue(path.is_file(), '尚未提供 Codex 路径规则选择器')
        spec=importlib.util.spec_from_file_location('rule_routing', path)
        module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_cross_engine_gameplay_and_shader_paths(self):
        module=self.router()
        for path in ('src/gameplay/move.ts','Assets/Game/Gameplay/Move.cs','Source/Game/Gameplay/Move.cpp'):
            with self.subTest(path=path):
                self.assertIn('.agents/rules/gameplay-code.md', module.rules_for_paths(ROOT,[path]))
        for path in ('water.gdshader','assets/shaders/water.frag','Source/Game/Shaders/water.usf'):
            with self.subTest(path=path):
                self.assertIn('.agents/rules/shader-code.md', module.rules_for_paths(ROOT,[path]))

    def test_rule_does_not_expand_to_unrelated_directories(self):
        module=self.router()
        self.assertNotIn('.agents/rules/gameplay-code.md', module.rules_for_paths(ROOT,['docs/gameplay-notes.md']))
        self.assertIn('.agents/rules/skill-authoring.md', module.rules_for_paths(ROOT,['.codex/agents/qa-tester.toml']))

    def test_windows_relative_paths_are_normalized(self):
        module=self.router()
        self.assertIn('.agents/rules/data-files.md', module.rules_for_paths(ROOT,[r'Assets\Game\Data\items.json']))


if __name__=='__main__': unittest.main()
