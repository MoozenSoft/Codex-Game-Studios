"""框架自检必须读取 Codex 原生文件，而不是继续解释旧客户端清单。"""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]


class InspectionTests(unittest.TestCase):
    def test_compat_separates_source_quotes_from_active_legacy_references(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);roles=root/'.codex/agents';roles.mkdir(parents=True)
            (roles/'reader.toml').write_text("name='reader'\ndescription='reader'\ndeveloper_instructions='''\n<!-- BEGIN UPSTREAM ROLE -->\n.claude/source.md\n<!-- END UPSTREAM ROLE -->\n.claude/active.md\n'''\n",encoding='utf-8')
            result=subprocess.run([sys.executable,str(ROOT/'.agents/scripts/studio-inspect.py'),'compat','--root',str(root)],capture_output=True,text=True,encoding='utf-8',timeout=10)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn('REFERENCE\tlegacy_runtime_path',result.stdout)
            self.assertIn('FOUND\tlegacy_runtime_path',result.stdout)
            self.assertIn('FOUND_LINES\t1',result.stdout)

    def run_helper(self,name,*args):
        env=dict(os.environ);env['PATH']=str(Path(sys.executable).parent)+os.pathsep+env['PATH']
        bash=os.environ.get('CGS_TEST_BASH') or shutil.which('bash')
        return subprocess.run([bash,str(ROOT/'.agents/scripts'/name),*args],env=env,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',timeout=30)

    def test_agent_check_reads_native_role(self):
        result=self.run_helper('agent-check.sh','--agent','qa-tester')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('.codex/agents/qa-tester.toml',result.stdout)
        self.assertIn('model=inherit',result.stdout)

    def test_skill_lint_uses_codex_metadata(self):
        result=self.run_helper('skill-lint.sh','dev-story')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('allow_implicit_invocation=false',result.stdout)
        self.assertNotIn('missing=allowed-tools',result.stdout)


if __name__=='__main__':unittest.main()
