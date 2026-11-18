"""框架开发检查：解析 YAML 与 Skill 元数据，不执行自定义 Python 对象。"""
import argparse
import json
from pathlib import Path
import re
import sys


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args();root=args.root.resolve()
    try:import yaml
    except ImportError:
        print(json.dumps({'exit_code':2,'coverage':{'yaml_files':0,'skill_frontmatters':0},'checks':[{'id':'yaml.environment','status':'not_assessed','reason':'框架开发检查需要安装 studio-tests/requirements.txt'}]},ensure_ascii=False))
        return 2
    skip={'.git','.scratch','.superpowers','node_modules','__pycache__','fixtures','dist','build'}
    coverage={'yaml_files':0,'skill_frontmatters':0};checks=[]
    for path in sorted(root.rglob('*')):
        if not path.is_file() or any(part in skip for part in path.relative_to(root).parts):continue
        skill=path.name=='SKILL.md' and '.agents' in path.relative_to(root).parts
        if path.suffix not in ('.yaml','.yml') and not skill:continue
        relative=path.relative_to(root).as_posix()
        coverage['skill_frontmatters' if skill else 'yaml_files']+=1
        try:
            text=path.read_text(encoding='utf-8-sig')
            if skill:
                match=re.match(r'---[ \t]*\n(.*?)^---[ \t]*(?:\n|\Z)',text,re.M|re.S)
                if not match:
                    checks.append({'id':'skill.yaml_schema','status':'failed','file':relative,'reason':'缺少完整 frontmatter 区块'});continue
                documents=list(yaml.safe_load_all(match.group(1)))
                data=documents[0] if len(documents)==1 else None
                if not isinstance(data,dict) or not all(isinstance(data.get(key),str) and data[key].strip() for key in ('name','description')):
                    checks.append({'id':'skill.yaml_schema','status':'failed','file':relative,'reason':'name 和 description 必须为非空字符串'})
            else:list(yaml.safe_load_all(text))
        except yaml.YAMLError as error:
            mark=getattr(error,'problem_mark',None)
            location=f'（行{mark.line+1}，列{mark.column+1}）' if mark else ''
            checks.append({'id':'yaml.syntax','status':'failed','file':relative,'reason':'YAML 语法或标签类型无效'+location})
        except (OSError,UnicodeError):
            checks.append({'id':'yaml.read','status':'failed','file':relative,'reason':'无法读取 UTF-8 文本'})
    code=1 if checks else 0
    print(json.dumps({'exit_code':code,'coverage':coverage,'checks':checks},ensure_ascii=False))
    return code


if __name__=='__main__':sys.exit(main())
