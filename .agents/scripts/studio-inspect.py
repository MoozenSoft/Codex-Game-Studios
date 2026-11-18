"""读取原生角色和 Skills 的结构事实，裁决由工作流和统一校验入口负责。"""
import argparse
import json
from pathlib import Path
import re
import sys
import tomllib


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('kind',choices=('agents','skills','compat'))
    parser.add_argument('name',nargs='?',default='all')
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--agent')
    parser.add_argument('--skill')
    args=parser.parse_args();root=args.root.resolve()
    if args.kind=='agents':
        paths=sorted((root/'.codex/agents').glob('*.toml'))
        if args.agent:paths=[p for p in paths if p.stem==args.agent]
        if not paths:print('NOT FOUND\t角色不存在');return 3
        print(f'agents\t{len(paths)}\t.codex/agents')
        for path in paths:
            data=tomllib.loads(path.read_text(encoding='utf-8'))
            body=data.get('developer_instructions','')
            if args.skill and f'.agents/skills/{args.skill}/SKILL.md' not in body:continue
            print(f"agent\t{data.get('name','-')}\tpath={path.relative_to(root).as_posix()}\tmodel={data.get('model','inherit')}\tpreloads={','.join(sorted(set(re.findall(r'.agents/skills/([\w-]+)/SKILL.md',body)))) or '-'}")
    elif args.kind=='skills':
        paths=sorted((root/'.agents/skills').glob('*/SKILL.md'))
        target=args.skill or args.name
        if target!='all':paths=[p for p in paths if p.parent.name==target]
        if not paths:print('NOT FOUND\tSkill不存在');return 3
        print(f'skills\t{len(paths)}\t.agents/skills')
        for path in paths:
            text=path.read_text(encoding='utf-8');name=path.parent.name
            header=text.split('---',2)[1] if text.startswith('---\n') else ''
            fields=set(re.findall(r'^([\w-]+):',header,re.M))
            missing=','.join(sorted({'name','description'}-fields)) or '-'
            policy=path.parent/'agents/openai.yaml'
            implicit=not(policy.is_file() and re.search(r'allow_implicit_invocation:\s*false',policy.read_text(encoding='utf-8')))
            print(f'skill\t{name}\tpath={path.relative_to(root).as_posix()}')
            print(f'check1\t{name}\tfrontmatter={"ok" if header else "missing"}\tmissing={missing}')
            phases=len(re.findall(r'^## Phase [0-9]+',text,re.M))
            headings=len(re.findall(r'^## ',text,re.M))
            verdicts=','.join(sorted(set(re.findall(r'\b(?:PASS|FAIL|BLOCKED|COMPLETE|NOT ASSESSED)\b',text)))) or '-'
            print(f'check2\t{name}\tphases={phases}\th2={headings}')
            print(f'check3\t{name}\tverdicts={verdicts}')
            print(f'check4\t{name}\tconfirmation_policy=.agents/docs/automation-modes.md')
            print(f'check5\t{name}\tresources={sum(p.is_file() for p in path.parent.rglob("*"))}')
            print(f'check6\t{name}\tdelegation=codex-runtime\tcontext_fork=not_applicable')
            print(f'check7\t{name}\tallow_implicit_invocation={str(implicit).lower()}\targuments=request_text')
    else:
        patterns={'legacy_env':r'\bCLAUDE_(?:PROJECT_DIR|SKILL_DIR|CODE_SESSION_ID|CODE_EFFORT_LEVEL)\b','shell_injection':r'^!`','legacy_runtime_path':r'\.claude/'}
        paths=list((root/'.agents/skills').rglob('*.md'))+list((root/'.codex/agents').glob('*.toml'))
        if args.skill:paths=[p for p in paths if f'/skills/{args.skill}/' in p.as_posix()]
        if args.agent:paths=[p for p in paths if p.stem==args.agent]
        hits=0;references=0
        for path in paths:
            reference=False
            for number,line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
                if path.suffix=='.toml' and line=='<!-- BEGIN UPSTREAM ROLE -->':reference=True;continue
                if path.suffix=='.toml' and line=='<!-- END UPSTREAM ROLE -->':reference=False;continue
                for name,pattern in patterns.items():
                    if re.search(pattern,line):
                        label='REFERENCE' if reference else 'FOUND'
                        print(f'{label}\t{name}\t{path.relative_to(root).as_posix()}:{number}')
                        if reference:references+=1
                        else:hits+=1
        print(f'FILES\t{len(paths)}\tFOUND_LINES\t{hits}\tREFERENCE_LINES\t{references}')
    return 0


if __name__=='__main__':sys.exit(main())
