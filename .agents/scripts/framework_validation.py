"""框架阶段校验，区分失败、未评估和可选检查，供 CLI、hook 与 CI 共用。"""
import json
from pathlib import Path
import re
import tomllib
import subprocess


def summarize(checks):
    failed=any(c['required'] and c['status']=='failed' for c in checks)
    unknown=any(c['required'] and c['status']=='not_assessed' for c in checks)
    return {'exit_code':1 if failed else 2 if unknown else 0,'checks':checks,
            'counts':{state:sum(c['status']==state for c in checks) for state in ('passed','failed','not_assessed')}}


def validate(root,stage='incremental',scope='all'):
    root=Path(root).resolve()
    checks=[]
    coverage={'json_files':0,'toml_files':0,'skills':0,'skill_resources':0,'source_total':0,'active':0,'retired':0,'pending':0,'native_components':0}
    def add(identifier,status,file='',reason='',required=True):
        checks.append({'id':identifier,'status':status,'required':required,'file':file,'reason':reason})
    skip={'.git','.scratch','.superpowers','.claude','node_modules','fixtures','__pycache__','dist','build'}
    changed=None
    if scope=='changed':
        result=subprocess.run(['git','-C',str(root),'status','--porcelain=v1','-z','--untracked-files=all'],capture_output=True,text=True,encoding='utf-8')
        top=subprocess.run(['git','-C',str(root),'rev-parse','--show-toplevel'],capture_output=True,text=True,encoding='utf-8')
        if result.returncode==0 and top.returncode==0 and Path(top.stdout.strip()).resolve()==root:
            changed=set()
            records=iter(result.stdout.split('\0'))
            for record in records:
                if not record:continue
                changed.add(record[3:].replace('\\','/'))
                if 'R' in record[:2] or 'C' in record[:2]:next(records,None)
        else:
            add('scope.fallback','passed',reason='目标不是独立 Git 根目录，改为检查目标全部文件')
    def included(path):
        return changed is None or path.relative_to(root).as_posix() in changed
    for path in root.rglob('*.json'):
        relative=path.relative_to(root)
        if any(part in skip for part in relative.parts):continue
        if not included(path):continue
        coverage['json_files']+=1
        try:json.loads(path.read_text(encoding='utf-8-sig'))
        except (ValueError,OSError) as error:add('json.syntax','failed',relative.as_posix(),str(error))
    for path in (root/'.codex').glob('**/*.toml'):
        if not included(path):continue
        coverage['toml_files']+=1
        try:
            data=tomllib.loads(path.read_text(encoding='utf-8'))
            if path.parent.name=='agents':
                if not all(data.get(key) for key in ('name','description','developer_instructions')):
                    add('agent.schema','failed',path.relative_to(root).as_posix(),'角色缺少必要字段')
        except (ValueError,OSError) as error:add('toml.syntax','failed',path.relative_to(root).as_posix(),str(error))
    for path in (root/'.agents/skills').glob('*/SKILL.md'):
        resources=list(path.parent.rglob('*.md'))
        if not any(included(resource) for resource in resources):continue
        coverage['skills']+=1
        text=path.read_text(encoding='utf-8')
        if not text.startswith('---\n') or len(text.split('---',2))<3:
            add('skill.frontmatter','failed',path.relative_to(root).as_posix(),'缺少 frontmatter');continue
        header=text.split('---',2)[1]
        fields=set(re.findall(r'^([\w-]+):',header,re.M))
        if not {'name','description'}<=fields:add('skill.schema','failed',path.relative_to(root).as_posix(),'缺少 name/description')
        if fields&{'allowed-tools','model','context','user-invocable','disable-model-invocation'}:
            add('skill.client_fields','failed',path.relative_to(root).as_posix(),'仍有旧客户端字段')
        for resource in resources:
            if not included(resource):continue
            coverage['skill_resources']+=1
            body=resource.read_text(encoding='utf-8')
            if re.search(r'(?m)^!`|\$\{?CLAUDE_|\$ARGUMENTS|\bCLAUDE_CODE_EFFORT_LEVEL\b',body):
                add('skill.client_execution','failed',resource.relative_to(root).as_posix(),'仍依赖旧注入、参数或运行设置变量')
    inventory=root/'studio-tests/migration-inventory.json'
    if inventory.is_file():
        try:
            manifest=json.loads(inventory.read_text(encoding='utf-8'))
            entries=manifest['entries']
            coverage.update(source_total=len(entries),native_components=len(manifest.get('native_components',[])))
            for status in ('active','retired','pending'):
                coverage[status]=sum(entry['status']==status for entry in entries)
            for native in manifest.get('native_components',[]):
                target=(root/native).resolve()
                if not target.is_relative_to(root) or not target.is_file():
                    add('migration.native_dependency','failed',native,'新增 Codex 必要资源不存在或越出项目')
            by_source={entry['source']:entry for entry in entries}
            for entry in entries:
                if entry['status']=='active':
                    if not entry.get('target') or not (root/entry['target']).is_file():add('migration.target','failed',entry['source'],'启用目标不存在')
                    for dep in entry['dependencies']:
                        if dep['type']=='required' and by_source.get(dep['source'],{}).get('status')!='active':
                            add('migration.dependency','failed',entry['source'],'必需依赖未启用：'+dep['source'])
            pending=sum(entry['status']=='pending' for entry in entries)
            add('migration.coverage','failed' if stage=='complete' and pending else 'passed',str(inventory.relative_to(root)),f'pending={pending}，total={len(entries)}')
        except (KeyError,ValueError) as error:add('migration.inventory','failed',str(inventory),str(error))
    elif stage=='complete':add('migration.inventory','not_assessed','','缺少迁移清单')
    if stage=='complete' and (root/'.claude').exists():add('migration.legacy_runtime','failed','.claude','旧运行目录尚未退役')
    if not checks:add('framework.observed','passed',reason='已检查所选范围，没有发现必要校验失败')
    result=summarize(checks)
    result.update({'stage':stage,'scope':scope,'coverage':coverage})
    return result
