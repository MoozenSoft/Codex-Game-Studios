"""统一框架校验命令入口。"""
import argparse
import json
from pathlib import Path
import sys
from framework_validation import validate

parser=argparse.ArgumentParser(description='校验框架和必要产物，失败与未评估分别返回1和2。')
parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2])
parser.add_argument('--scope',choices=('all','changed'),default='all')
parser.add_argument('--stage',choices=('incremental','complete'),default='incremental')
parser.add_argument('--format',choices=('text','json'),default='text')
args=parser.parse_args()
result=validate(args.root,args.stage,args.scope)
if args.format=='json': print(json.dumps(result,ensure_ascii=False))
else:
    for check in result['checks']:print(f"{check['status']}\t{check['id']}\t{check['file']}\t{check['reason']}")
sys.exit(result['exit_code'])
