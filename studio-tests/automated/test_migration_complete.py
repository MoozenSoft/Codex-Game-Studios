"""最终退役检查；与中间批次的依赖检查分开。"""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]


class CompleteMigrationTests(unittest.TestCase):
    def test_old_runtime_entrypoints_are_retired(self):
        self.assertFalse((ROOT/'.claude').exists(),'旧运行目录仍存在')
        for prefix in ('','src/','design/','docs/','studio-tests/'):
            self.assertFalse((ROOT/(prefix+'CLAUDE.md')).exists())
            self.assertTrue((ROOT/(prefix+'AGENTS.md')).is_file())
        self.assertFalse((ROOT/'.worktreeinclude').exists())

    def test_every_source_has_final_disposition(self):
        data=json.loads((ROOT/'studio-tests/migration-inventory.json').read_text(encoding='utf-8'))
        for entry in data['entries']:
            with self.subTest(source=entry['source']):
                self.assertIn(entry['status'],('active','retired'))
                if entry['status']=='active':self.assertTrue((ROOT/entry['target']).is_file())
                else:self.assertTrue(entry.get('reason') or entry.get('replacement'))


if __name__=='__main__':unittest.main()
