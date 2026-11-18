"""用隔离项目执行迁移后的公共脚本，检查路径定位与用户内容保留。"""
import os
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class SharedScriptTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='工作室 路径-')
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.bash = os.environ.get('CGS_TEST_BASH') or shutil.which('bash')
        self.env = dict(os.environ)
        self.env['PATH'] = str(Path(sys.executable).parent) + os.pathsep + self.env['PATH']

    def run_script(self, name, *args, input=None):
        script = ROOT / '.agents/scripts' / name
        self.assertTrue(script.is_file(), f'缺少迁移脚本：{name}')
        return subprocess.run([self.bash, str(script), *args, '--root', str(self.project)], cwd=self.project, env=self.env, input=input, text=True, encoding='utf-8', capture_output=True, timeout=40)

    def test_web_scaffold_escapes_title_and_preserves_existing_files(self):
        (self.project/'AGENTS.md').write_text('用户规则\n', encoding='utf-8')
        (self.project/'src').mkdir()
        (self.project/'src/main.ts').write_text('// 用户代码\n', encoding='utf-8')
        result = self.run_script('web-scaffold.sh', '--title', '钓鱼 <A>&')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('钓鱼 &lt;A&gt;&amp;', (self.project/'index.html').read_text(encoding='utf-8'))
        self.assertEqual((self.project/'src/main.ts').read_text(encoding='utf-8'), '// 用户代码\n')
        self.assertEqual((self.project/'AGENTS.md').read_text(encoding='utf-8'), '用户规则\n')
        self.assertFalse((self.project/'CLAUDE.md').exists())

    def test_web_scaffold_refuses_existing_package(self):
        (self.project/'package.json').write_text('{"name":"existing"}', encoding='utf-8')
        result = self.run_script('web-scaffold.sh')
        self.assertEqual(result.returncode, 3)
        self.assertFalse((self.project/'index.html').exists())

    def test_config_set_rejects_unshared_local_engine(self):
        (self.project/'project.yaml').write_text('schema_version: 1\n', encoding='utf-8')
        result = self.run_script('config-set.sh', '--local', 'engine.name', 'Godot')
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.project/'project.local.yaml').exists())
        result = self.run_script('config-set.sh', '--local', 'modes.automation', 'guided')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('guided', (self.project/'project.local.yaml').read_text(encoding='utf-8'))

    def test_grow_record_writes_engine_without_touching_agents(self):
        policy = '# 用户规则\n<!-- ENGINE-REFERENCE-IMPORT -->\n- **Engine**: [CHOOSE]\n'
        (self.project/'AGENTS.md').write_text(policy, encoding='utf-8')
        (self.project/'project.yaml').write_text('schema_version: 1\n', encoding='utf-8')
        (self.project/'package.json').write_text('{\n  "devDependencies": {\n    "vite": "8.0.5"\n  }\n}\n', encoding='utf-8')
        result = self.run_script('one-shot-grow.sh', 'record', 'fish')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.project/'AGENTS.md').read_text(encoding='utf-8'), policy)
        self.assertIn('Web', (self.project/'project.yaml').read_text(encoding='utf-8'))
        self.assertTrue((self.project/'docs/engine-reference/web/VERSION.md').is_file())
        self.assertFalse((self.project/'CLAUDE.md').exists())

    def test_grow_guard_treats_src_agents_as_metadata(self):
        (self.project/'src').mkdir()
        (self.project/'src/AGENTS.md').write_text('代码规则', encoding='utf-8')
        game = self.project/'prototypes/fish'
        game.mkdir(parents=True)
        (game/'index.html').write_text('<html></html>', encoding='utf-8')
        result = self.run_script('one-shot-grow.sh', 'guard', 'fish')
        self.assertIn('guard\troot\tpass\tnot grown', result.stdout)

    def test_grow_copy_preserves_extra_config_globals_and_functions(self):
        game=self.project/'prototypes/fish';game.mkdir(parents=True)
        source='window.CONFIG={duration:{value:30,min:10,max:90,step:5},seed:721};\nwindow.ART={color:"purple"};\nwindow.nextDuration=()=>CONFIG.duration.value+1;\n'
        (game/'config.js').write_text(source,encoding='utf-8')
        (game/'index.html').write_text('<!doctype html>\n<title>fish</title>\n<script src="config.js"></script>\n<script>\nwindow.growObservation={color:ART.color,duration:CONFIG.duration.value,extra:nextDuration()};\n</script>\n',encoding='utf-8')
        copied=self.run_script('one-shot-grow.sh','copy','fish')
        self.assertEqual(copied.returncode,0,copied.stderr)
        config=self.project/'data/config.json'
        values=json.loads(config.read_text(encoding='utf-8'));values['duration']['value']=45
        config.write_text(json.dumps(values),encoding='utf-8')
        node=subprocess.run(['node','--experimental-vm-modules',str(ROOT/'studio-tests/fixtures/grow/evaluate-module.mjs'),str(self.project/'src/main.js')],cwd=self.project,capture_output=True,text=True,encoding='utf-8',timeout=20)
        self.assertEqual(node.returncode,0,node.stderr)
        self.assertEqual(json.loads(node.stdout),{'color':'purple','duration':45,'extra':46})
        self.assertEqual((game/'config.js').read_text(encoding='utf-8'),source)

    def test_grow_copy_preserves_classic_top_level_bindings(self):
        game=self.project/'prototypes/fish';game.mkdir(parents=True)
        source='window.CONFIG={duration:{value:30,min:10,max:90,step:5}};\nvar ART={color:"purple"};\nlet BONUS=2;\nconst OFFSET=3;\nfunction nextDuration(){return CONFIG.duration.value+BONUS+OFFSET;}\n'
        (game/'config.js').write_text(source,encoding='utf-8')
        (game/'index.html').write_text('<!doctype html>\n<title>fish</title>\n<script src="config.js"></script>\n<script>\nwindow.growObservation={color:ART.color,bonus:BONUS,offset:OFFSET,duration:CONFIG.duration.value,extra:nextDuration()};\n</script>\n',encoding='utf-8')
        copied=self.run_script('one-shot-grow.sh','copy','fish')
        self.assertEqual(copied.returncode,0,copied.stderr)
        config=self.project/'data/config.json'
        values=json.loads(config.read_text(encoding='utf-8'));values['duration']['value']=45
        config.write_text(json.dumps(values),encoding='utf-8')
        node=subprocess.run(['node','--experimental-vm-modules',str(ROOT/'studio-tests/fixtures/grow/evaluate-module.mjs'),str(self.project/'src/main.js')],cwd=self.project,capture_output=True,text=True,encoding='utf-8',timeout=20)
        self.assertEqual(node.returncode,0,node.stderr)
        self.assertEqual(json.loads(node.stdout),{'color':'purple','bonus':2,'offset':3,'duration':45,'extra':50})
        self.assertEqual((game/'config.js').read_text(encoding='utf-8'),source)

    def test_session_checkpoint_is_repeatable_and_preserves_notes(self):
        result = self.run_script('session-state.sh', 'checkpoint', input='任务：移动\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.run_script('session-state.sh', 'append', input='保留用户笔记\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.run_script('session-state.sh', 'checkpoint', input='任务：战斗\n')
        self.assertEqual(result.returncode, 0, result.stderr)
        state = (self.project/'production/session-state/active.md').read_text(encoding='utf-8')
        self.assertIn('任务：战斗', state)
        self.assertIn('保留用户笔记', state)
        self.assertNotIn('任务：移动', state)

    def test_reference_files_are_saved_and_deduplicated(self):
        source=self.project/'参考.png'
        source.write_bytes(b'\x89PNG\r\n\x1a\nimage-data')
        result=self.run_script('references-save.sh','--file',str(source))
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('saved\treferences/pasted-1.png',result.stdout)
        result=self.run_script('references-save.sh','--file',str(source))
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('kept\treferences/pasted-1.png',result.stdout)
        self.assertEqual(list((self.project/'references').iterdir()),[self.project/'references/pasted-1.png'])

    def test_stage_writer_creates_consistent_config_and_mirror(self):
        result=self.run_script('set-stage.sh','Technical Setup')
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('stage: Technical Setup',(self.project/'project.yaml').read_text(encoding='utf-8'))
        self.assertEqual((self.project/'production/stage.txt').read_text(encoding='utf-8'),'Technical Setup')

    def test_artifact_check_uses_shared_catalog_for_external_project(self):
        script=ROOT/'.agents/scripts/artifact-check.sh'
        result=subprocess.run([self.bash,str(script),'--phase','concept',str(self.project)],env=self.env,cwd=self.project,capture_output=True,text=True,encoding='utf-8',timeout=30)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertIn('STEP:',result.stdout)
        self.assertIn('ABSENT',result.stdout)

    def test_disabled_session_tracking_keeps_tool_guard_active(self):
        (self.project/'project.yaml').write_text('features:\n  session_state: on\n',encoding='utf-8')
        (self.project/'project.local.yaml').write_text('features:\n  session_state: off\n',encoding='utf-8')
        script=ROOT/'.codex/hooks/run.sh'
        def run(event):
            return subprocess.run([self.bash,str(script),'--root',str(self.project)],input=json.dumps(event),cwd=self.project,env=self.env,capture_output=True,text=True,encoding='utf-8',timeout=20)
        started=run({'hook_event_name':'SessionStart'})
        self.assertEqual(started.returncode,0,started.stderr)
        self.assertFalse(started.stdout.strip(),'关闭跟踪时不注入检查点')
        guarded=run({'hook_event_name':'PreToolUse','tool_name':'apply_patch','tool_input':{'command':'*** Begin Patch\n*** Add File: .env\n+X=1\n*** End Patch'}})
        self.assertEqual(guarded.returncode,0,guarded.stderr)
        self.assertEqual(json.loads(guarded.stdout)['hookSpecificOutput']['permissionDecision'],'deny')
        self.assertFalse((self.project/'production/session-logs').exists(),'个人关闭跟踪后不保存事件日志')

    def test_registry_reports_invalid_status_and_removed_entry(self):
        registry=self.project/'design/registry/entities.yaml';registry.parent.mkdir(parents=True)
        before=self.project/'before.yaml';after=self.project/'after.yaml'
        before.write_text('entities:\n  - name: goblin\n    status: active\nitems: []\n',encoding='utf-8')
        registry.write_text('entities:\n  - name: goblin\n    status: invalid\nitems: []\n',encoding='utf-8')
        checked=self.run_script('registry.sh','validate')
        self.assertEqual(checked.returncode,0,checked.stderr)
        self.assertRegex(checked.stdout,r'(?m)^STATUS\tentities\tgoblin\tinvalid\t')
        after.write_text('entities: []\nitems: []\n',encoding='utf-8')
        compared=self.run_script('registry.sh','compare','entities',str(before),str(after))
        self.assertEqual(compared.returncode,0,compared.stderr)
        self.assertRegex(compared.stdout,r'(?m)^REMOVED\tentities\t.*goblin')

    def test_review_receipt_detects_content_change_with_same_mtime(self):
        source=self.project/'design.md';receipt=self.project/'review.md'
        source.write_text('# 设计\n数值：3\n',encoding='utf-8')
        script=ROOT/'.agents/scripts/review-receipts.sh'
        def run(*args):
            return subprocess.run([self.bash,str(script),*args],cwd=self.project,env=self.env,capture_output=True,text=True,encoding='utf-8',timeout=20)
        stamp=run('hash',source.name)
        self.assertEqual(stamp.returncode,0,stamp.stderr)
        receipt.write_text(stamp.stdout,encoding='utf-8')
        unchanged=run('check',receipt.name,source.name)
        self.assertIn('UNCHANGED: design.md',unchanged.stdout)
        original=source.stat()
        source.write_text('# 设计\n数值：4\n',encoding='utf-8')
        os.utime(source,ns=(original.st_atime_ns,original.st_mtime_ns))
        changed=run('check',receipt.name,source.name)
        self.assertEqual(changed.returncode,0,changed.stderr)
        self.assertIn('CHANGED: design.md',changed.stdout)

    def test_python_entry_uses_explicit_runtime_and_preserves_arguments(self):
        script=ROOT/'.agents/scripts/python-run.sh'
        self.assertTrue(script.is_file(),'缺少真实Python解释器入口')
        probe=self.project/'参数 验收.py'
        probe.write_text('import json,sys\nprint(json.dumps(sys.argv[1:],ensure_ascii=False))\n',encoding='utf-8')
        env=dict(self.env,CGS_PYTHON=sys.executable)
        result=subprocess.run([self.bash,str(script),str(probe),'中文 参数'],cwd=self.project,env=env,capture_output=True,text=True,encoding='utf-8',timeout=20)
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual(json.loads(result.stdout),['中文 参数'])

    def test_python_entry_does_not_fallback_from_invalid_explicit_runtime(self):
        script=ROOT/'.agents/scripts/python-run.sh'
        self.assertTrue(script.is_file(),'缺少真实Python解释器入口')
        env=dict(self.env,CGS_PYTHON=str(self.project/'missing-runtime.exe'))
        result=subprocess.run([self.bash,str(script),'-c','print("must not run")'],cwd=self.project,env=env,capture_output=True,text=True,encoding='utf-8',timeout=20)
        self.assertEqual(result.returncode,2,result.stderr)
        self.assertIn('未评估',result.stderr)
        self.assertNotIn('must not run',result.stdout)


if __name__ == '__main__':
    unittest.main()
