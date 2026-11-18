"""解析 Codex 实际事件输入，执行前仅阻断明确禁止的操作。"""
from pathlib import Path
import re


def patch_paths(command):
    return list(dict.fromkeys(re.findall(r'^\*\*\* (?:Add File|Update File|Delete File|Move to): (.+?)\r?$',command,re.M)))


def forbidden_path(root,path):
    root=Path(root).resolve()
    target=(root/str(path).replace('\\','/')).resolve()
    if not target.is_relative_to(root):return '目标路径位于项目之外'
    if any(part.lower()=='.env' or part.lower().startswith('.env.') for part in target.relative_to(root).parts):
        return '项目规则禁止通过工具读取或改写环境凭据文件'
    if target.suffix.lower() in ('.uasset','.umap'):
        return 'Unreal 二进制资产必须通过编辑器或受支持工具生成，不能用文本 patch 改写'
    return None


def forbidden_command(command):
    patterns=(r'\bgit\s+(?:-[Cc]\s+\S+\s+)?reset\s+[^\n;&]*--hard\b',
              r'\bgit\s+(?:-[Cc]\s+\S+\s+)?push\s+[^\n;&]*(?:--force\b|(?:^|\s)-f(?:\s|$)|(?:^|\s)\+)',
              r'\bgit\s+clean\s+[^\n;&]*(?:--force\b|-[a-zA-Z]*f)',
              r'\brm\s+(?:-[a-zA-Z]*r[a-zA-Z]*f|-[a-zA-Z]*f[a-zA-Z]*r)\b')
    return '项目规则禁止该破坏性命令' if any(re.search(pattern,command,re.I) for pattern in patterns) else None


def canonical_tool_name(name):
    return name.removeprefix('functions.') if isinstance(name,str) else ''


def normalize_tool_event(event):
    tool=canonical_tool_name(event.get('tool_name',''))
    keys={'Bash':('command','cmd'),'exec_command':('cmd','command'),'apply_patch':('command','input')}.get(tool)
    if keys is None:return event
    args=event.get('tool_input',{})
    if tool=='apply_patch' and isinstance(args,str):args={'command':args}
    if not isinstance(args,dict):raise ValueError('工具输入不是可评估的 JSON 对象')
    values=[args[key] for key in keys if key in args]
    if not values or any(not isinstance(value,str) or not value.strip() for value in values):
        raise ValueError('缺少有效命令或 patch 输入')
    if len(set(values))!=1:raise ValueError('命令输入字段互相冲突')
    normalized={key:value for key,value in args.items() if key not in keys}
    normalized['command']=values[0]
    return {**event,'tool_name':tool,'tool_input':normalized}


def pre_tool_decision(root,event):
    try:event=normalize_tool_event(event)
    except ValueError as error:return '工具守卫未评估：'+str(error)
    tool=event.get('tool_name','')
    args=event.get('tool_input',{})
    if not isinstance(args,dict):return '工具输入不是可评估的 JSON 对象'
    command=args.get('command','')
    if tool in ('Bash','exec_command'):
        return forbidden_command(command) if isinstance(command,str) else '命令字段无效'
    if tool=='apply_patch':
        if not isinstance(command,str):return 'patch 命令字段无效'
        paths=patch_paths(command)
        if not paths:return 'patch 未提供可评估的文件目标'
        for path in paths:
            reason=forbidden_path(root,path)
            if reason:return reason+': '+path
    return None
