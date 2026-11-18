"""验证 Codex 事件适配与必要校验的失败状态。"""
import importlib.util
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor

ROOT=Path(__file__).resolve().parents[2]


def load(name,path):
    if not path.is_file():
        raise AssertionError(f'缺少实现：{path.name}')
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HookTests(unittest.TestCase):
    def test_native_exec_names_fields_and_registration_are_consistent(self):
        module=load('event_input',ROOT/'.codex/hooks/event_input.py')
        hooks=json.loads((ROOT/'.codex/hooks.json').read_text(encoding='utf-8'))['hooks']
        import re
        for name in ('Bash','exec_command','functions.exec_command'):
            with self.subTest(tool=name):
                self.assertTrue(any(re.search(item['matcher'],name) for item in hooks['PreToolUse']))
                key='cmd' if 'exec_command' in name else 'command'
                reason=module.pre_tool_decision(ROOT,{'tool_name':name,'tool_input':{key:'git reset --hard HEAD'}})
                self.assertTrue(reason)
                self.assertIsNone(module.pre_tool_decision(ROOT,{'tool_name':name,'tool_input':{key:'git status --short'}}))
        for args in ({},{'cmd':None},{'cmd':' '},{'cmd':'git status','command':'git reset --hard HEAD'}):
            with self.subTest(args=args):self.assertTrue(module.pre_tool_decision(ROOT,{'tool_name':'exec_command','tool_input':args}))

    def test_native_patch_input_forms_cannot_bypass_path_guard(self):
        module=load('event_input',ROOT/'.codex/hooks/event_input.py')
        patch='*** Begin Patch\n*** Add File: .env\n+X=1\n*** End Patch'
        for args in ({'input':patch},patch):
            self.assertTrue(module.pre_tool_decision(ROOT,{'tool_name':'functions.apply_patch','tool_input':args}))

    def test_native_patch_post_event_reports_bad_json_and_unknown_input(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);(root/'value.json').write_text('{bad',encoding='utf-8')
            patch='*** Begin Patch\n*** Update File: value.json\n@@\n-{}\n+{bad\n*** End Patch'
            result=self.dispatch(root,{'hook_event_name':'PostToolUse','tool_name':'functions.apply_patch','tool_input':{'input':patch}})
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn('value.json',json.loads(result.stdout)['hookSpecificOutput']['additionalContext'])
            for arguments in ({},{'input':'*** Begin Patch\n*** End Patch'}):
                result=self.dispatch(root,{'hook_event_name':'PostToolUse','tool_name':'functions.apply_patch','tool_input':arguments})
                self.assertEqual(result.returncode,2,result.stderr)
                self.assertIn('未评估',json.loads(result.stdout)['hookSpecificOutput']['additionalContext'])

    def dispatch(self,root,event):
        path=ROOT/'.codex/hooks/dispatch.py'
        self.assertTrue(path.is_file())
        return subprocess.run([sys.executable,str(path),'--root',str(root)],input=json.dumps(event),capture_output=True,text=True,encoding='utf-8',timeout=10)

    def test_patch_paths_include_moves_and_multiple_files(self):
        module=load('event_input',ROOT/'.codex/hooks/event_input.py')
        patch='*** Begin Patch\n*** Add File: data/items.json\n+{}\n*** Update File: src/a.ts\n*** Move to: src/b.ts\n@@\n-a\n+b\n*** Delete File: src/old.ts\n*** End Patch\n'
        self.assertEqual(module.patch_paths(patch),['data/items.json','src/a.ts','src/b.ts','src/old.ts'])

    def test_forbidden_operation_blocked_before_execution(self):
        module=load('event_input',ROOT/'.codex/hooks/event_input.py')
        self.assertTrue(module.forbidden_command('git reset --hard HEAD'))
        self.assertFalse(module.forbidden_command('git status --short'))
        with tempfile.TemporaryDirectory() as temp:
            self.assertTrue(module.forbidden_path(Path(temp),'../outside.json'))
            self.assertTrue(module.forbidden_path(Path(temp),'.env'))
            self.assertTrue(module.forbidden_path(Path(temp),'.ENV.secret'))
            self.assertTrue(module.forbidden_path(Path(temp),'Content/Maps/Level.umap'))
            self.assertFalse(module.forbidden_path(Path(temp),'data/config.json'))

    def test_incomplete_artifact_allows_repair(self):
        module=load('event_input',ROOT/'.codex/hooks/event_input.py')
        with tempfile.TemporaryDirectory() as temp:
            result=module.pre_tool_decision(Path(temp),{'tool_name':'apply_patch','tool_input':{'command':'*** Begin Patch\n*** Add File: data/x.json\n+not-json\n*** End Patch'}})
            self.assertIsNone(result,'普通未完成内容应允许后续修复')

    def test_required_failure_blocks_completion(self):
        module=load('framework_validation',ROOT/'.agents/scripts/framework_validation.py')
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); (root/'data').mkdir(); (root/'data/bad.json').write_text('{bad',encoding='utf-8')
            result=module.validate(root,stage='incremental')
            self.assertEqual(result['exit_code'],1)
            self.assertTrue(any(item['status']=='failed' and item['required'] for item in result['checks']))

    def test_optional_unassessed_is_reported(self):
        module=load('framework_validation',ROOT/'.agents/scripts/framework_validation.py')
        result=module.summarize([{'id':'visual','required':False,'status':'not_assessed','reason':'没有浏览器'}])
        self.assertEqual(result['exit_code'],0)
        self.assertEqual(result['checks'][0]['status'],'not_assessed')
        result=module.summarize([{'id':'logic','required':True,'status':'not_assessed','reason':'缺少测试工具'}])
        self.assertEqual(result['exit_code'],2)

    def test_dispatch_returns_deny_without_running_command(self):
        with tempfile.TemporaryDirectory() as temp:
            result=self.dispatch(temp,{'hook_event_name':'PreToolUse','tool_name':'Bash','tool_input':{'command':'git reset --hard HEAD'}})
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(result.stdout)['hookSpecificOutput']['permissionDecision'],'deny')
            log=(Path(temp)/'production/session-logs/codex-events.jsonl').read_text(encoding='utf-8')
            self.assertNotIn('git reset',log,'事件日志不保存原始命令')

    def test_session_start_restores_checkpoint(self):
        with tempfile.TemporaryDirectory() as temp:
            state=Path(temp)/'production/session-state/active.md';state.parent.mkdir(parents=True)
            state.write_text('恢复任务：STORY-42',encoding='utf-8')
            result=self.dispatch(temp,{'hook_event_name':'SessionStart'})
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn('STORY-42',json.loads(result.stdout)['hookSpecificOutput']['additionalContext'])

    def test_lifecycle_reminders_use_supported_output(self):
        # Codex CLI 0.169.0 的这两个事件接受通用提醒字段。
        for event, reminder in (
            ('PreCompact', 'production/session-state/active.md'),
            ('SubagentStop', '产物路径和证据'),
        ):
            with self.subTest(event=event), tempfile.TemporaryDirectory() as temp:
                state = Path(temp) / 'production/session-state/active.md'
                state.parent.mkdir(parents=True)
                state.write_bytes(b'<!-- CHECKPOINT -->\nSTORY-42\n<!-- /CHECKPOINT -->\n')
                checkpoint = state.read_bytes()
                result = self.dispatch(temp, {'hook_event_name': event})
                self.assertEqual(result.returncode, 0, result.stderr)
                output = json.loads(result.stdout)
                self.assertEqual(set(output), {'systemMessage'})
                self.assertIn(reminder, output['systemMessage'])
                self.assertEqual(state.read_bytes(), checkpoint)
                log = Path(temp) / 'production/session-logs/codex-events.jsonl'
                self.assertEqual(json.loads(log.read_text(encoding='utf-8'))['event'], event)

    def test_post_tool_warns_without_claiming_rollback(self):
        with tempfile.TemporaryDirectory() as temp:
            file=Path(temp)/'data.json';file.write_text('{bad',encoding='utf-8')
            result=self.dispatch(temp,{'hook_event_name':'PostToolUse','tool_name':'apply_patch','tool_input':{'command':'*** Begin Patch\n*** Add File: data.json\n+{bad\n*** End Patch'}})
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn('data.json',json.loads(result.stdout)['hookSpecificOutput']['additionalContext'])
            self.assertEqual(file.read_text(encoding='utf-8'),'{bad')

    def test_validator_checks_executable_skill_references(self):
        module=load('framework_validation',ROOT/'.agents/scripts/framework_validation.py')
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); skill=root/'.agents/skills/sample';(skill/'references').mkdir(parents=True)
            (skill/'SKILL.md').write_text('---\nname: sample\ndescription: sample\n---\n读取 references/run.md',encoding='utf-8')
            (skill/'references/run.md').write_text('!`echo ${CLAUDE_SKILL_DIR}`',encoding='utf-8')
            self.assertEqual(module.validate(root)['exit_code'],1)

    def test_changed_scope_checks_reference_when_skill_entry_is_unchanged(self):
        module=load('framework_validation',ROOT/'.agents/scripts/framework_validation.py')
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); skill=root/'.agents/skills/sample';(skill/'references').mkdir(parents=True)
            (skill/'SKILL.md').write_text('---\nname: sample\ndescription: sample\n---\n读取 references/run.md',encoding='utf-8')
            reference=skill/'references/run.md'
            reference.write_text('使用显式命令读取配置。',encoding='utf-8')
            subprocess.run(['git','init','--quiet',str(root)],check=True,capture_output=True)
            subprocess.run(['git','-C',str(root),'add','.'],check=True,capture_output=True)
            subprocess.run(['git','-C',str(root),'-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','--quiet','-m','初始测试文件'],check=True,capture_output=True)
            reference.write_text('!`echo ${CLAUDE_SKILL_DIR}`',encoding='utf-8')
            result=module.validate(root,scope='changed')
            self.assertEqual(result['exit_code'],1)
            self.assertTrue(any(check['id']=='skill.client_execution' and check['file'].endswith('references/run.md') for check in result['checks']))

    def test_long_checkpoint_keeps_current_task_not_only_tail(self):
        with tempfile.TemporaryDirectory() as temp:
            state=Path(temp)/'production/session-state/active.md';state.parent.mkdir(parents=True)
            state.write_text('<!-- CHECKPOINT -->\n任务 CURRENT_STORY_9\n<!-- /CHECKPOINT -->\n'+'旧记录\n'*6000,encoding='utf-8')
            result=self.dispatch(temp,{'hook_event_name':'SessionStart'})
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertTrue('CURRENT_STORY_9' in json.loads(result.stdout)['hookSpecificOutput']['additionalContext'],'长记录恢复应保留当前检查点')

    def test_duplicate_tool_event_has_one_log_record(self):
        with tempfile.TemporaryDirectory() as temp:
            event={'hook_event_name':'PreToolUse','tool_name':'Bash','tool_use_id':'same-tool-7','tool_input':{'command':'git status'}}
            self.dispatch(temp,event);self.dispatch(temp,event)
            rows=(Path(temp)/'production/session-logs/codex-events.jsonl').read_text(encoding='utf-8').splitlines()
            self.assertEqual(len(rows),1)

    def test_commit_guard_rejects_invalid_staged_json(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            subprocess.run(['git','init','--quiet',str(root)],check=True,capture_output=True)
            (root/'data.json').write_text('{broken',encoding='utf-8')
            subprocess.run(['git','-C',str(root),'add','--','data.json'],check=True,capture_output=True)
            result=self.dispatch(root,{'hook_event_name':'PreToolUse','tool_name':'Bash','tool_input':{'command':'git commit -m "提交"'}})
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertTrue(result.stdout.strip(),'提交前必须返回拒绝结果')
            self.assertEqual(json.loads(result.stdout)['hookSpecificOutput']['permissionDecision'],'deny')

    def test_unknown_or_malformed_event_is_unassessed(self):
        with tempfile.TemporaryDirectory() as temp:
            for payload in ('','{bad','[]','{"hook_event_name":"Unknown"}','{"hook_event_name":[]}'):
                with self.subTest(payload=payload):
                    result=subprocess.run([sys.executable,str(ROOT/'.codex/hooks/dispatch.py'),'--root',temp],input=payload,capture_output=True,text=True,encoding='utf-8',timeout=10)
                    self.assertEqual(result.returncode,2,result.stderr)
                    self.assertIn('未评估',result.stderr)

    def test_concurrent_tool_logs_remain_complete_and_unique(self):
        with tempfile.TemporaryDirectory() as temp:
            events=[{'hook_event_name':'PostToolUse','session_id':'concurrent','tool_name':'Bash','tool_use_id':f'tool-{index}'} for index in range(8)]
            with ThreadPoolExecutor(max_workers=8) as pool:
                results=list(pool.map(lambda event:self.dispatch(temp,event),events+events))
            self.assertTrue(all(result.returncode==0 for result in results))
            rows=[json.loads(line) for line in (Path(temp)/'production/session-logs/codex-events.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual({row['tool_use_id'] for row in rows},{f'tool-{index}' for index in range(8)})
            self.assertEqual(len(rows),8)

    def test_logging_failure_does_not_disable_tool_guard(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'production').mkdir()
            (root/'production/session-logs').write_text('占用日志路径',encoding='utf-8')
            result=self.dispatch(root,{'hook_event_name':'PreToolUse','tool_name':'apply_patch','tool_input':{'command':'*** Begin Patch\n*** Add File: .env\n+X=1\n*** End Patch'}})
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(result.stdout)['hookSpecificOutput']['permissionDecision'],'deny')
            self.assertIn('未评估',result.stderr)

    def test_registered_events_accept_sanitized_protocol_examples(self):
        fixture=json.loads((ROOT/'studio-tests/fixtures/hooks/event-examples.json').read_text(encoding='utf-8'))
        registered=set(json.loads((ROOT/'.codex/hooks.json').read_text(encoding='utf-8'))['hooks'])
        self.assertEqual({event['hook_event_name'] for event in fixture['events']},registered)
        with tempfile.TemporaryDirectory() as temp:
            for event in fixture['events']:
                result=self.dispatch(temp,event)
                self.assertEqual(result.returncode,0,result.stderr)
            rows=[json.loads(line) for line in (Path(temp)/'production/session-logs/codex-events.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual({row['event'] for row in rows},registered)

    def test_complete_validation_checks_new_native_dependencies(self):
        module=load('framework_validation',ROOT/'.agents/scripts/framework_validation.py')
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'studio-tests').mkdir()
            (root/'studio-tests/migration-inventory.json').write_text(json.dumps({'entries':[],'native_components':['.codex/hooks/event_log.py']}),encoding='utf-8')
            result=module.validate(root,stage='complete')
            self.assertEqual(result['exit_code'],1)
            self.assertTrue(any(check['id']=='migration.native_dependency' for check in result['checks']))


if __name__=='__main__': unittest.main()
