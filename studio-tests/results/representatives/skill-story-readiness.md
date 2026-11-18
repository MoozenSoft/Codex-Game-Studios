# skill-story-readiness 场景验收

场景结果：passed（正确拒绝开始并保留状态未知）；Story Verdict: NEEDS WORK，ADR status item: NOT ASSESSED，不能 READY。

## 输入范围与实际执行

root 为 runtime-cases/skill-story-readiness。Checking 1 story files：production/epics/EPIC-001-S01-damage.md。
实际读取当前 .agents/skills/story-readiness/SKILL.md、QA gate 参考、runtime / automation / director-gates 文档，显式读取本案例 project.yaml、故事与引用 ADR，未用插件。
共享 yaml-helper.sh 显式 --root 本案例绝对路径，退出 0：workflow/full、review/full、qa/full、story_granularity/fine、team/studio（rigor:full），automation/collaborative（project.yaml），QL skill-gates=run。

实际 story-facts.sh --root <本案例root> --lint --granularity fine <故事> 退出 0：stories 1；type_missing、no_tr_id、TODO line 3；原始 Status 为 TODO（helper 分 OTHER）。
helper ac=0 仅因原 AC 用普通列表而非 checkbox；人工实读有一条“伤害计算结果为30。”，没有伪称文字不存在。该句不提供输入、调用对象或条件，依然不构成自足测试合同。

实际 adr-status.sh --root <本案例root> 退出 0：
    adrs 1
    no_status 1
    ADR adr-0001 docs/architecture/adr-0001-damage.md - ... unversioned

人工复读 ADR：只有行内 Status: Proposed，没有正式 ## Status。故事也标注 (Proposed)。因此没有 Accepted 证据；遵循 Skill 将正式状态读取记 NOT ASSESSED，而不是把 no_status 伪称 helper 已识别 Proposed 或 Accepted。需先修复/正式决定 ADR，再重查；本次不接受或修改 ADR。

## Passing Checks / Gaps

| 必须报告的组 | 已能核对的项目 | 缺项与处理 |
| --- | --- | --- |
| Design Completeness | 有一条可读取 AC | 无设计文件/具体规则追踪；AC 缺输入、接口及条件，非自足，需补可测试合同 |
| Architecture Completeness | 引用路径确实存在；TR registry/manifest 不存在 | 正式 ADR 状态未评估，无 Accepted；无 engine notes；没有 manifest 时相关版本比较 N/A，不假报过期 |
| Scope Clarity | none — see Gaps | 无估算、Out of Scope、明确依赖列表或 None |
| Open Questions | 没有已声明依赖路径可核对 | helper 标记 TODO（状态行），不是有 owner 的设计决定；依赖未声明，不能推断为无依赖 |
| Asset References | No asset references | 不对不存在的资源要求额外检查 |
| Definition of Done | fine 最低1条的原文数量存在 | Type 缺失，性能预算/无影响理由缺失；无 Test Evidence 地点，且 full 未提供测试合同 |

TR registry 与 control-manifest 经实际 Test-Path 确认缺失；按照 Skill，无 TR registry 时 TR-ID 校验通过（不把 helper no_tr_id 单独列为阻塞）。未声明 Type 不能直接认定正式 Logic 分类；内容像计算逻辑仅作为建议。既有 NEEDS WORK 优先于未评估项，故总体不是 READY 或假称所有检查均评估完毕。

## 真实 QA 门禁与结论

实际绑定 qa-lead（Sol），已回收；先读 ql-story-ready 定义，分别核对本案例配置，helper --root 退出 0，全程只读。
QL-STORY-READY: INADEQUATE。
理由：唯一 AC“伤害计算结果为30。”可被常量30满足，不能唯一确定伤害算法；没有输入/调用接口；Type、TR 需求和依赖上下文缺失。候选改写为“输入10、2、1.5，调用伤害计算接口返回30”，接口及精度仍待作者确定。这只是建议，未当成批准条件。

预期满足：确实检查引用 ADR，报告其未正式 Accepted / 状态格式不可判定，不允许开始；未修改故事、ADR、sprint 或阶段，仅写本报告。没有把 YAML 同ID的 Done 当作 readiness 通过依据。

未评估：正式 ADR 状态、需求引用、未知依赖、极值/非法输入合同及实现测试；原生引擎运行未验证。没有主动实施或生成缺失产物。
Review: QL-STORY-READY: INADEQUATE
Next ready stories: no sprint file found
Next step: 先补齐故事合同并澄清 ADR 状态，再 story-readiness
Files changed: 仅获批 result.md，故事/ADR 未改
