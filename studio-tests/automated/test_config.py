"""运行真实配置解析器，验证模式、来源与 checkout 定位约定。"""

import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class ConfigTests(unittest.TestCase):
    def setUp(self):
        helper = ROOT / '.agents/scripts/yaml-helper.sh'
        self.assertTrue(helper.is_file(), '尚未迁移可执行配置解析器')
        self.temp = tempfile.TemporaryDirectory(prefix='游戏 配置-')
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        for path in ('.agents/scripts/yaml-helper.sh', '.agents/scripts/engine-row.awk', '.agents/engines/engines.tsv'):
            target = self.project / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, target)
        self.helper = self.project / '.agents/scripts/yaml-helper.sh'
        self.bash = os.environ.get('CGS_TEST_BASH') or shutil.which('bash')
        self.assertTrue(self.bash, '配置测试需要 Git Bash 或 Bash')
        self.env = dict(os.environ)
        self.env['PATH'] = str(Path(sys.executable).parent) + os.pathsep + self.env['PATH']

    def resolve(self, shared='', local=None, cwd=None, args=()):
        (self.project / 'project.yaml').write_text(shared, encoding='utf-8')
        if local is not None:
            (self.project / 'project.local.yaml').write_text(local, encoding='utf-8')
        command = [self.bash, str(self.helper), *args, 'resolve_config', '--keys', 'automation,workflow,qa.level,review_mode,team.size,docs.density,story_granularity']
        result = subprocess.run(command, cwd=cwd or self.project, env=self.env, capture_output=True, text=True, encoding='utf-8', timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_default_automation_is_collaborative(self):
        output = self.resolve('schema_version: 1\n')
        self.assertIn('automation: collaborative (default)', output)
        self.assertIn('workflow: minimal (rigor:minimal)', output)

    def test_automation_independent_of_rigor(self):
        for rigor, qa, review in (('minimal', 'minimal', 'solo'), ('standard', 'standard', 'lean'), ('full', 'full', 'full')):
            with self.subTest(rigor=rigor):
                output = self.resolve(f'modes:\n  rigor: {rigor}\n')
                self.assertIn('automation: collaborative (default)', output)
                self.assertIn(f'qa.level: {qa} (rigor:{rigor})', output)
                self.assertIn(f'review_mode: {review} (rigor:{rigor})', output)

    def test_local_automation_override(self):
        output = self.resolve('modes:\n  automation: collaborative\n', 'modes:\n  automation: autonomous\n')
        self.assertIn('automation: autonomous (project.local.yaml)', output)

    def test_invalid_local_enum_falls_back_with_warning(self):
        output = self.resolve('modes:\n  automation: guided\n', 'modes:\n  automation: typo\n')
        self.assertIn('automation: guided (project.yaml)', output)
        self.assertIn('typo', output)
        self.assertIn('notes:', output)

    def test_subdirectory_uses_helpers_checkout(self):
        nested = self.project / 'src/ui'
        nested.mkdir(parents=True)
        self.env['CLAUDE_PROJECT_DIR'] = str(ROOT)
        output = self.resolve('modes:\n  automation: guided\n', cwd=nested)
        self.assertIn('automation: guided (project.yaml)', output)

    def test_explicit_root_wins_over_callers_project(self):
        other = self.project / 'other'
        other.mkdir()
        (other / 'project.yaml').write_text('modes:\n  automation: autonomous\n', encoding='utf-8')
        output = self.resolve('modes:\n  automation: guided\n', cwd=other, args=('--root', str(self.project)))
        self.assertIn('automation: guided (project.yaml)', output)

    def test_unknown_command_fails(self):
        result = subprocess.run([self.bash, str(self.helper), 'unknown-command'], cwd=self.project, env=self.env, capture_output=True, text=True, encoding='utf-8', timeout=10)
        self.assertEqual(result.returncode, 2)

    def test_invalid_explicit_interpreter_does_not_fall_back_to_launcher(self):
        self.env['CGS_PYTHON']=str(self.project/'missing-python.exe')
        (self.project/'project.yaml').write_text('schema_version: 1\n',encoding='utf-8')
        result=subprocess.run([self.bash,str(self.helper),'resolve_config','--keys','automation'],cwd=self.project,env=self.env,capture_output=True,text=True,encoding='utf-8',timeout=10)
        self.assertEqual(result.returncode,2)
        self.assertNotIn('automation: collaborative',result.stdout)

    def test_framework_folders_are_not_game_test_roots(self):
        for folder in ('.agents', '.codex'):
            with self.subTest(folder=folder):
                (self.project / folder).mkdir(exist_ok=True)
                (self.project / 'project.yaml').write_text(f'engine:\n  name: Web\n  test_root: {folder}\n', encoding='utf-8')
                result = subprocess.run([self.bash, '-c', 'source "$1"; resolve_test_root', 'probe', str(self.helper)], cwd=self.project, env=self.env, capture_output=True, text=True, encoding='utf-8', timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn('\tinvalid\t', result.stdout)

    def test_locked_local_engine_cannot_change_derived_roots(self):
        (self.project/'project.yaml').write_text('engine:\n  name: Web\n',encoding='utf-8')
        (self.project/'project.local.yaml').write_text('engine:\n  name: Unity\n',encoding='utf-8')
        for name in ('src','tests','Assets/Tests'):(self.project/name).mkdir(parents=True)
        result=subprocess.run([self.bash,self.helper.as_posix(),'resolve_config','--keys','engine,engine_values,engine_row'],cwd=self.project,env=self.env,capture_output=True,text=True,encoding='utf-8',timeout=30)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('engine: Web (project.yaml)',result.stdout)
        self.assertIn('engine_row: engine=Web(project.yaml)',result.stdout)
        self.assertIn('code_root=src(engine.name)',result.stdout)
        self.assertIn('test_root=tests(engine.name)',result.stdout)
        self.assertIn('not locally overridable',result.stdout)
        self.assertNotIn('Unity(project.local.yaml)',result.stdout)

    @unittest.skipUnless(os.name=='nt','Windows反斜杠脚本路径')
    def test_windows_absolute_script_path_reads_its_own_engine_table(self):
        (self.project/'project.yaml').write_text('engine:\n  name: Web\n',encoding='utf-8')
        result=subprocess.run([self.bash,str(self.helper),'resolve_config','--keys','engine_row'],cwd=self.project,env=self.env,capture_output=True,text=True,encoding='utf-8',timeout=30)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('engine_row: engine=Web(project.yaml)',result.stdout)
        self.assertIn('code_root=src(engine.name)',result.stdout)


if __name__ == '__main__':
    unittest.main()
