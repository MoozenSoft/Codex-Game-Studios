"""按文件路径选择共享领域规则；不依赖客户端自动加载路径 frontmatter。"""
import argparse
import json
from pathlib import Path
import posixpath
import re


def expand_braces(pattern):
    match=re.search(r'\{([^{}]+)\}',pattern)
    if match is None:
        return [pattern]
    return [result for choice in match.group(1).split(',')
            for result in expand_braces(pattern[:match.start()]+choice+pattern[match.end():])]


def glob_regex(pattern):
    result=''
    index=0
    while index<len(pattern):
        if pattern[index:index+3]=='**/':
            result+='(?:.*/)?'; index+=3
        elif pattern[index:index+2]=='**':
            result+='.*'; index+=2
        elif pattern[index]=='*':
            result+='[^/]*'; index+=1
        elif pattern[index]=='?':
            result+='[^/]'; index+=1
        else:
            result+=re.escape(pattern[index]); index+=1
    return re.compile('^'+result+'$')


def rules_for_paths(root, paths):
    root=Path(root).resolve()
    normalized=[]
    for path in paths:
        text=str(path).replace('\\','/')
        if Path(text).is_absolute():
            text=Path(text).resolve().relative_to(root).as_posix()
        text=posixpath.normpath(text)
        if text=='..' or text.startswith('../'):
            raise ValueError('规则路径必须位于项目内')
        normalized.append(text)
    selected=[]
    for rule in sorted((root/'.agents/rules').glob('*.md')):
        text=rule.read_text(encoding='utf-8')
        header=text.split('---',2)[1] if text.startswith('---') else ''
        patterns=re.findall(r'^\s+-\s+[\"\']([^\"\']+)[\"\']\s*$',header,re.M)
        expressions=[glob_regex(p) for pattern in patterns for p in expand_braces(pattern)]
        if any(expression.fullmatch(path) for expression in expressions for path in normalized):
            selected.append(rule.relative_to(root).as_posix())
    return selected


def main():
    parser=argparse.ArgumentParser(description='返回修改目标适用的领域规则文件，请在编辑前读取这些规则。')
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
    parser.add_argument('--json',action='store_true')
    parser.add_argument('paths',nargs='+')
    args=parser.parse_args()
    result=rules_for_paths(args.root,args.paths)
    print(json.dumps({'rules':result},ensure_ascii=False) if args.json else '\n'.join(result))


if __name__=='__main__':
    main()
