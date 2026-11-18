"""验证原始验收证据在暂存区/新clone中仍符合归档SHA。"""
import hashlib
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = Path('studio-tests/results/runtime-evidence/app-core')


class RuntimeArchiveTests(unittest.TestCase):
    def test_app_raw_archive_matches_manifest(self):
        rows = json.loads((ROOT / ARCHIVE / 'archive-manifest.json').read_text(encoding='utf-8'))
        if (ROOT / '.git').exists():
            # 检查实际交付字节，不能让本地CRLF掩盖暂存时的LF归一化。
            names = [f':{(ARCHIVE / row["path"]).as_posix()}' for row in rows]
            raw = subprocess.check_output(['git', 'cat-file', '--batch'], cwd=ROOT, input=('\n'.join(names) + '\n').encode())
            blobs = []
            offset = 0
            for row in rows:
                end = raw.index(b'\n', offset)
                header = raw[offset:end].split()
                self.assertEqual(header[-2], b'blob', f'暂存区缺少归档：{row["path"]}')
                size = int(header[-1])
                blobs.append(raw[end + 1:end + 1 + size])
                offset = end + 2 + size
        else:
            blobs = [(ROOT / ARCHIVE / row['path']).read_bytes() for row in rows]
        mismatches = [row['path'] for row, blob in zip(rows, blobs)
                      if len(blob) != row['bytes'] or hashlib.sha256(blob).hexdigest() != row['sha256']]
        self.assertEqual(mismatches, [], '原始证据的交付字节必须匹配manifest')


if __name__ == '__main__':
    unittest.main()
