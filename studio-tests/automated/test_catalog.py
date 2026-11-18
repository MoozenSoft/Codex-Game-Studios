"""按实际 catalog 派生完整迁移集合，不用抽样数量代替覆盖率。"""
from pathlib import Path
import re
import tomllib
import unittest

ROOT=Path(__file__).resolve().parents[2]


class CatalogTests(unittest.TestCase):
    def names(self):
        text=(ROOT/'studio-tests/catalog.yaml').read_text(encoding='utf-8')
        skills,agents=re.split(r'^agents:',text,maxsplit=1,flags=re.M)
        return (set(re.findall(r'^  - name: ([\w-]+)',skills,re.M)),set(re.findall(r'^  - name: ([\w-]+)',agents,re.M)))

    def test_formal_skill_set_is_complete(self):
        expected,_=self.names()
        actual={p.parent.name for p in (ROOT/'.agents/skills').glob('*/SKILL.md')}
        self.assertEqual(actual,expected)

    def test_role_set_is_complete_and_uses_native_schema(self):
        _,expected=self.names()
        configs=[tomllib.loads(p.read_text(encoding='utf-8')) for p in (ROOT/'.codex/agents').glob('*.toml')]
        self.assertEqual({item['name'] for item in configs},expected)
        for item in configs:
            if 'model' in item:
                self.assertIsInstance(item['model'], str)
                self.assertTrue(item['model'])
            self.assertNotIn('model_reasoning_effort',item)


if __name__=='__main__':unittest.main()
