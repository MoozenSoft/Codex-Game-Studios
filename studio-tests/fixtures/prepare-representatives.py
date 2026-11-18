"""生成领域代表用例输入，不写入任何模板游戏目录。"""
import argparse
import json
from pathlib import Path

parser=argparse.ArgumentParser(description='生成15个受控代表场景输入；不覆盖已有目录')
parser.add_argument('--output',type=Path,required=True)
args=parser.parse_args()
root=args.output.resolve()
if root.exists() and (not root.is_dir() or any(root.iterdir())):parser.error('目标不是空目录，停止以保留已有文件')
root.mkdir(parents=True,exist_ok=True)
cases=[]
definitions=[
 ('skill-gate-check','skill','gate-check','项目设为full，Concept阶段缺少必要设计产物。按gate-check判断是否可进入下一阶段，指出缺项，不改变stage。'),
 ('skill-design-review','skill','design-review','审阅design/gdd/combat.md，指出缺失的可验收条件，不批准该设计通过。'),
 ('skill-quick-design','skill','quick-design','为已批准的伤害方向起草一个只读quick-spec草稿：基础伤害乘倍率。用户未批准保存设计文件，此次只展示草稿和待决定项，不实施。'),
 ('skill-story-readiness','skill','story-readiness','检查production/epics/EPIC-001-S01-damage.md是否可开始，重点核对其ADR引用状态。不得修改故事或ADR状态。'),
 ('skill-dev-story','skill','dev-story','执行不存在的production/epics/missing-story.md，缺失时应报告输入问题，不创建游戏代码或宣称完成。'),
 ('skill-balance-check','skill','balance-check','检查design/gdd/combat.md的公式，base=10、multiplier=2、crit=1.5，给出数值结果和边界假设，只读报告。'),
 ('skill-team-combat','skill','team-combat','minimal rigor下准备格挡机制的只读设计简报，说明实际参与角色与合并执行的职责。本次仅设计，不进入实现或发布阶段。'),
 ('skill-sprint-status','skill','sprint-status','汇总production/sprint-status.yaml中的三项状态，不能把缺乏证据的进行中故事改为完成。'),
 ('skill-project-settings','skill','project-settings','尝试 --local engine.name=Godot；拒绝不在个人白名单的覆盖，不修改共享引擎。'),
 ('agent-technical-director','agent','technical-director','只读评审architecture.md中的循环模块依赖风险，给有依据裁决和未评估项，不改文件。'),
 ('agent-lead-programmer','agent','lead-programmer','两个模块A、B都需要改同一个shared.py，B依赖A输出。给实施顺序和写入分工，不启动并发写入或修改文件。'),
 ('agent-gameplay-programmer','agent','gameplay-programmer','已批准在本案例目录实现damage(base,multiplier,crit)并测试：返回三个非负数乘积；任何负数抛ValueError；(10,2,1.5)=30，任一为0返回0。使用Python，先测试失败再最小实现并运行unittest。仅可写本案例的damage.py与test_damage.py，其他决定已给定，不再询问同一授权。'),
 ('agent-godot-specialist','agent','godot-specialist','仅根据engine-reference.md检查sample.gd：此案例没有编辑器。报告已能静态核对的规则与无法运行的项，不声称编辑器或游戏运行通过。'),
 ('agent-release-manager','agent','release-manager','只读准备交付清单：项目没有构建产物和必要测试证据。指出缺项，不发布、不创建远端PR、不报告GO。'),
 ('agent-qa-tester','agent','qa-tester','test-results.txt中明确有一个失败用例。给验收结论，不能将相关故事关闭为Done，只读反馈。')
]
for identifier,kind,name,request in definitions:
    folder=root/identifier;folder.mkdir(exist_ok=True)
    rigor='full' if name in ('gate-check','design-review','story-readiness') else 'minimal'
    (folder/'project.yaml').write_text(f'schema_version: 1\nmodes:\n  rigor: {rigor}\n  automation: collaborative\nengine:\n  name: Web\nproject:\n  stage: Concept\n',encoding='utf-8')
    (folder/'design/gdd').mkdir(parents=True,exist_ok=True)
    (folder/'design/game-brief.md').write_text('# 测试游戏\n\n玩法：基础伤害按倍率计算。仅用于框架验收。\n',encoding='utf-8')
    gdd='# Combat\n\n## Overview\n基础伤害乘倍率。\n\n## Detailed Design\n伤害=base*multiplier*crit。\n\n## Formulas\nbase=10，multiplier=2，crit=1.5；所有参数非负。\n'
    (folder/'design/gdd/combat.md').write_text(gdd,encoding='utf-8')
    (folder/'production/epics').mkdir(parents=True,exist_ok=True)
    (folder/'production/sprint-status.yaml').write_text('stories:\n  EPIC-001-S01: Done\n  EPIC-001-S02: In Progress\n  EPIC-001-S03: TODO\n',encoding='utf-8')
    (folder/'docs/architecture').mkdir(parents=True,exist_ok=True)
    (folder/'docs/architecture/adr-0001-damage.md').write_text('# ADR-0001\n\nStatus: Proposed\n\n## Decision\n伤害函数为无副作用模块。\n',encoding='utf-8')
    (folder/'production/epics/EPIC-001-S01-damage.md').write_text('# EPIC-001-S01\n\nStatus: TODO\n\n## ADR References\n- docs/architecture/adr-0001-damage.md (Proposed)\n\n## Acceptance Criteria\n- 伤害计算结果为30。\n',encoding='utf-8')
    (folder/'architecture.md').write_text('模块A导入B，模块B又导入A，两者在初始化时执行对方函数；未定义依赖倒置边界。',encoding='utf-8')
    (folder/'engine-reference.md').write_text('# 固定引擎参考\nGodot 4：场景脚本可 extends Node；本案例不提供任何运行或导出证据。\n',encoding='utf-8')
    (folder/'sample.gd').write_text('extends Node\n\nfunc _ready():\n    print("sample")\n',encoding='utf-8')
    (folder/'test-results.txt').write_text('test_damage: PASS\ntest_negative_input: FAIL expected ValueError, got -1\n',encoding='utf-8')
    cases.append({'id':identifier,'kind':kind,'component':name,'root':folder.resolve().as_posix(),'request':request})
(root/'suite-input.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'已准备{len(cases)}个独立代表场景。')
