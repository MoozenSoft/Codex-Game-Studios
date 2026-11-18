"""Codex 生命周期入口：最少事件日志、检查点恢复和工具边界检查。"""
import argparse
import json
from pathlib import Path
import sys
import os
import re
import importlib.util
from event_input import pre_tool_decision,patch_paths,normalize_tool_event,canonical_tool_name
from event_log import append_event

parser=argparse.ArgumentParser()
parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
args=parser.parse_args()
root=args.root.resolve()
try:
    event=json.loads(sys.stdin.readline())
    if not isinstance(event,dict):raise ValueError('事件必须是 JSON 对象')
except (ValueError,TypeError) as error:
    print('Codex hook 未评估：'+str(error),file=sys.stderr);sys.exit(2)
name=event.get('hook_event_name','')
if not isinstance(name,str) or name not in {'SessionStart','PreToolUse','PostToolUse','PreCompact','Stop','SubagentStart','SubagentStop'}:
    print('Codex hook 未评估：未知生命周期事件',file=sys.stderr);sys.exit(2)
tracking=os.environ.get('CGS_SESSION_STATE','on')!='off'
if not tracking and name not in ('PreToolUse','PostToolUse'):
    sys.exit(0)
if tracking:
    try:append_event(root,event)
    except OSError as error:
        # 日志故障不能跳过后面的工具守卫；生命周期本身则明确报告未评估。
        print('Codex 事件日志未评估：'+str(error),file=sys.stderr)
        if name not in ('PreToolUse','PostToolUse'):sys.exit(2)

def context(message):
    print(json.dumps({'hookSpecificOutput':{'hookEventName':name,'additionalContext':message}},ensure_ascii=False))

def system_message(message):
    # 这两个生命周期事件只通过通用字段显示提醒，不能注入额外上下文。
    print(json.dumps({'systemMessage': message}))

if name=='PreToolUse':
    reason=pre_tool_decision(root,event)
    if not reason:event=normalize_tool_event(event)
    if not reason and event.get('tool_name') in ('Bash','exec_command'):
        # 实现来自当前框架 checkout；--root 仅改变被检查的项目。
        checker=Path(__file__).resolve().parents[2]/'.agents/scripts/git-index-check.py'
        if checker.is_file():
            spec=importlib.util.spec_from_file_location('git_index_check',checker)
            module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            if module.is_commit(event.get('tool_input',{}).get('command','')):
                reason=module.commit_context_reason(root,event['tool_input']['command'],event['tool_input'],event.get('cwd'))
                if not reason:
                    report=module.check_index(root)
                    if report['exit_code']:
                        reason='提交前暂存区 JSON 校验未完成：'+'；'.join(check['file']+' '+check['reason'] for check in report['checks'][:4])
        elif re.search(r'\bgit\b[^\n]*\bcommit\b',event.get('tool_input',{}).get('command','')):
            reason='提交前校验未评估：缺少 git-index-check.py'
    if reason:print(json.dumps({'hookSpecificOutput':{'hookEventName':name,'permissionDecision':'deny','permissionDecisionReason':reason}},ensure_ascii=False))
elif name=='SessionStart':
    state=root/'production/session-state/active.md'
    if state.is_file():
        text=state.read_text(encoding='utf-8')
        blocks=[]
        for marker in ('STATUS','CHECKPOINT'):
            match=re.search(r'(?ms)^\s*<!-- '+marker+r' -->\s*$.*?^\s*<!-- /'+marker+r' -->\s*$',text)
            if match:blocks.append(match.group())
        context('工作室检查点：\n'+('\n'.join(blocks) if blocks else text)[:12000])
    else:context('工作室：尚无会话检查点，按当前请求建立任务记录。')
elif name=='PreCompact':
    system_message('压缩前保留已授权任务的检查点；production/session-state/active.md 是恢复依据，事件日志不替代任务内容。')
elif name=='PostToolUse' and canonical_tool_name(event.get('tool_name'))=='apply_patch':
    try:event=normalize_tool_event(event)
    except ValueError as error:
        context('写后JSON校验未评估：'+str(error))
        sys.exit(2)
    paths=patch_paths(event['tool_input']['command'])
    if not paths:
        context('写后JSON校验未评估：patch 未提供可评估的文件目标')
        sys.exit(2)
    bad=[]
    for path in paths:
        file=(root/path).resolve()
        if file.is_relative_to(root) and file.is_file() and file.suffix=='.json':
            try:json.loads(file.read_text(encoding='utf-8-sig'))
            except ValueError:bad.append(path)
    if bad:context('以下 JSON 当前无效，允许继续修复，但必要验收不能完成：'+', '.join(bad))
elif name=='SubagentStop':
    system_message('核对该子代理简报中约定的产物路径和证据；仅有完成事件不代表产物验收通过。')
