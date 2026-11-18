"""只读检查 Git 暂存的 JSON 字节；与工作区文件状态分开判断。"""
import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys


def is_commit(command):
    try:
        lexer=shlex.shlex(command,posix=True,punctuation_chars=';&|()\n')
        lexer.escape='';lexer.whitespace_split=True;lexer.commenters=''
        tokens=list(lexer)
    except ValueError:
        return False
    for index,token in enumerate(tokens):
        if token.replace('\\','/').rsplit('/',1)[-1].lower() not in ('git','git.exe'):
            continue
        cursor=index+1
        while cursor<len(tokens):
            token=tokens[cursor]
            if token in ('-C','-c','--git-dir','--work-tree','--namespace','--config-env'):
                cursor+=2
            elif token.startswith('-'):
                cursor+=1
            else:
                if token=='commit':return True
                break
    return False


def commit_context_reason(root,command,tool_input,event_cwd=None):
    """只核实可确定的当前项目上下文，不执行命令或猜测 shell 状态。"""
    root=Path(root).resolve()
    try:
        lexer=shlex.shlex(command,posix=True,punctuation_chars=';&|()\r\n')
        lexer.whitespace=' \t'
        lexer.escape='';lexer.whitespace_split=True;lexer.commenters=''
        tokens=list(lexer)
        directory_commands={'cd','chdir','pushd','popd','set-location','sl'}
        for index,token in enumerate(tokens):
            if token.lower() in directory_commands and (index==0 or set(tokens[index-1])<=set(';&|()\r\n')):
                return '提交前校验未评估：命令内切换目录，无法确定实际 Git 索引'
        context_keys={'git_dir','git_work_tree','git_index_file','git_common_dir'}
        if any(key.lower() in context_keys for key in os.environ) or any(
            token.lower().removeprefix('$env:').split('=',1)[0] in context_keys for token in tokens
        ):
            return '提交前校验未评估：自定义 Git 环境可能改变索引'
        base=Path(event_cwd) if event_cwd else root
        if not base.is_absolute():base=root/base
        directories=[]
        for key in ('workdir','cwd'):
            if key in tool_input:
                value=tool_input[key]
                if not isinstance(value,str) or not value.strip():
                    return '提交前校验未评估：无效的命令工作目录'
                path=Path(value)
                directories.append((path if path.is_absolute() else base/path).resolve())
        if len(set(directories))>1:
            return '提交前校验未评估：命令工作目录字段冲突'
        working=directories[0] if directories else base.resolve()
        for index,token in enumerate(tokens):
            if token.replace('\\','/').rsplit('/',1)[-1].lower() not in ('git','git.exe'):continue
            cursor=index+1;directory=working;unsupported=False
            while cursor<len(tokens):
                option=tokens[cursor]
                if option=='-C':
                    cursor+=1
                    if cursor>=len(tokens):return '提交前校验未评估：缺少 git -C 目录'
                    path=Path(tokens[cursor]);directory=(path if path.is_absolute() else directory/path).resolve()
                elif option.startswith('-C'):
                    path=Path(option[2:]);directory=(path if path.is_absolute() else directory/path).resolve()
                elif option in ('-c','--git-dir','--work-tree','--namespace','--config-env'):
                    unsupported=True;cursor+=1
                elif option.startswith('-'):
                    if option not in ('--no-pager','--paginate','--no-optional-locks'):unsupported=True
                else:
                    if option=='commit':
                        if unsupported:return '提交前校验未评估：Git 全局配置或索引覆盖不在支持范围内'
                        top=subprocess.run(['git','-C',str(directory),'rev-parse','--show-toplevel'],capture_output=True,timeout=8)
                        if top.returncode or Path(top.stdout.decode('utf-8').strip()).resolve()!=root:
                            return '提交前校验未评估：实际提交目标不属于当前项目，不能检查另一个仓库的索引'
                    break
                cursor+=1
    except (OSError,ValueError,TypeError,subprocess.TimeoutExpired,UnicodeError):
        return '提交前校验未评估：无法确认实际 Git 工作目录'
    return None


def check_index(root):
    checks=[]
    def result(code,status,file='',reason=''):
        if status:checks.append({'id':'git.index.json','status':status,'required':True,'file':file,'reason':reason})
        return {'exit_code':code,'checks':checks}
    try:
        top=subprocess.run(['git','-C',str(root),'rev-parse','--show-toplevel'],capture_output=True,timeout=8)
        if top.returncode or Path(top.stdout.decode('utf-8').strip()).resolve()!=Path(root).resolve():
            return result(2,'not_assessed',reason='目标不是独立 Git 根目录，不能用外层仓库的暂存区代替项目检查')
        listed=subprocess.run(['git','-C',str(root),'diff','--cached','--name-only','--diff-filter=ACMR','-z','--','*.json'],capture_output=True,timeout=8)
        if listed.returncode:
            return result(2,'not_assessed',reason='无法读取 Git 暂存区，提交前 JSON 检查未执行')
        for raw in filter(None,listed.stdout.split(b'\0')):
            name=raw.decode('utf-8')
            blob=subprocess.run(['git','-C',str(root),'show',':'+name],capture_output=True,timeout=8)
            if blob.returncode:
                return result(2,'not_assessed',name,'无法读取已暂存内容')
            try:
                json.loads(blob.stdout.decode('utf-8-sig'))
            except (ValueError,UnicodeError):
                checks.append({'id':'git.index.json','status':'failed','required':True,'file':name,'reason':'Git 暂存内容不是有效 UTF-8 JSON；工作区修复后须重新暂存'})
    except (OSError,subprocess.TimeoutExpired,UnicodeError):
        return result(2,'not_assessed',reason='Git 或暂存内容不可读取，提交前检查未完成')
    return result(1 if checks else 0,None) if checks else result(0,'passed',reason='已检查当前项目的暂存 JSON')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,default=Path.cwd())
    args=parser.parse_args()
    report=check_index(args.root)
    print(json.dumps(report,ensure_ascii=False))
    return report['exit_code']


if __name__=='__main__':sys.exit(main())
