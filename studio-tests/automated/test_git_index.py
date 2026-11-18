"""暂存区校验必须检查提交的字节，不能用工作区的修复掩盖坏暂存内容。"""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]

class GitIndexTests(unittest.TestCase):
    def checker(self):
        path=ROOT/'.agents/scripts/git-index-check.py'
        self.assertTrue(path.is_file(),'缺少暂存区校验入口')
        spec=importlib.util.spec_from_file_location('git_index_check',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        return module

    def fixture(self):
        temp=tempfile.TemporaryDirectory(prefix='暂存 检查-');self.addCleanup(temp.cleanup)
        root=Path(temp.name)
        subprocess.run(['git','init','--quiet',str(root)],check=True,capture_output=True)
        return root

    def stage(self,root,file):
        subprocess.run(['git','-C',str(root),'add','--',file],check=True,capture_output=True)

    def test_invalid_index_is_not_hidden_by_repaired_worktree(self):
        checker=self.checker();root=self.fixture();file=root/'中文 数据.json'
        file.write_text('{broken',encoding='utf-8');self.stage(root,file.name)
        file.write_text('{}\n',encoding='utf-8')
        result=checker.check_index(root)
        self.assertEqual(result['exit_code'],1)
        self.assertEqual(result['checks'][0]['file'],file.name)

    def test_valid_index_does_not_validate_unstaged_worktree(self):
        checker=self.checker();root=self.fixture();file=root/'数据.json'
        file.write_bytes(b'\xef\xbb\xbf{\r\n "value": 1\r\n}\r\n');self.stage(root,file.name)
        file.write_text('{broken',encoding='utf-8')
        self.assertEqual(checker.check_index(root)['exit_code'],0)

    def test_non_repository_is_unassessed(self):
        checker=self.checker()
        with tempfile.TemporaryDirectory() as temp:
            result=checker.check_index(Path(temp))
            self.assertEqual(result['exit_code'],2)
            self.assertEqual(result['checks'][0]['status'],'not_assessed')

    def test_native_cmd_commit_checks_actual_staged_json(self):
        root=self.fixture();(root/'bad.json').write_text('{broken',encoding='utf-8');self.stage(root,'bad.json')
        import sys
        event={'hook_event_name':'PreToolUse','tool_name':'functions.exec_command','tool_input':{'cmd':'git commit -m test'}}
        result=subprocess.run([sys.executable,str(ROOT/'.codex/hooks/dispatch.py'),'--root',str(root)],input=json.dumps(event),capture_output=True,text=True,encoding='utf-8',timeout=10)
        self.assertEqual(result.returncode,0,result.stderr)
        report=json.loads(result.stdout)
        self.assertEqual(report['hookSpecificOutput']['permissionDecision'],'deny')
        self.assertIn('bad.json',report['hookSpecificOutput']['permissionDecisionReason'])

    def test_commit_detection_ignores_quoted_prose_and_supports_global_options(self):
        checker=self.checker()
        self.assertTrue(checker.is_commit('git -C "a repo" -c user.name=Fixture commit -m "提交"'))
        self.assertTrue(checker.is_commit('git add a.json && git commit -m "提交"'))
        self.assertFalse(checker.is_commit('Write-Output "git commit -m example"'))
        self.assertFalse(checker.is_commit('git log --grep commit'))

    def test_native_commit_context_never_checks_a_different_index(self):
        import sys
        root=self.fixture();other=self.fixture()
        (other/'bad.json').write_text('{broken',encoding='utf-8');self.stage(other,'bad.json')
        sub=root/'sub';sub.mkdir()
        nested=root/'nested';nested.mkdir()
        subprocess.run(['git','init','--quiet',str(nested)],check=True,capture_output=True)
        cases=(
            ({'cmd':'git commit -m test','workdir':str(other)},True),
            ({'cmd':'git commit -m test','workdir':str(sub)},False),
            ({'cmd':'git commit -m test','workdir':str(nested)},True),
            ({'cmd':f'git -C "{other.as_posix()}" commit -m test'},True),
            ({'cmd':'git -C sub commit -m test'},False),
            ({'cmd':'GIT_INDEX_FILE=other-index git commit -m test'},True),
            ({'cmd':'cd nested && git commit -m test'},True),
            ({'cmd':'echo setup\ncd nested\ngit commit -m test'},True),
            ({'cmd':'Write-Output setup\r\n\r\nSet-Location nested\r\ngit commit -m test'},True),
        )
        for arguments,deny in cases:
            with self.subTest(arguments=arguments):
                event={'hook_event_name':'PreToolUse','tool_name':'functions.exec_command','tool_input':arguments}
                result=subprocess.run([sys.executable,str(ROOT/'.codex/hooks/dispatch.py'),'--root',str(root)],input=json.dumps(event),capture_output=True,text=True,encoding='utf-8',timeout=10)
                self.assertEqual(result.returncode,0,result.stderr)
                if deny:
                    self.assertTrue(result.stdout.strip(),'不能把另一个索引的检查当成通过')
                    report=json.loads(result.stdout)['hookSpecificOutput']
                    self.assertEqual(report['permissionDecision'],'deny')
                    self.assertIn('未评估',report['permissionDecisionReason'])
                else:
                    self.assertFalse(result.stdout.strip(),result.stdout)

if __name__=='__main__':unittest.main()
