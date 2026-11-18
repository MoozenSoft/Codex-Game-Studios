# skill-quick-design 场景验收与只读草稿

场景结果：passed（草稿范围）；没有达到 Skill 的“已保存、可交实施”完成状态。

输入范围：root 为 runtime-cases/skill-quick-design，显式读 project.yaml、design/gdd/combat.md、design/game-brief.md 和现有故事。实际应用当前 .agents/skills/quick-design/SKILL.md 的 Context Scan / 草稿流程及运行约定，未使用插件。
共享 yaml-helper.sh --root <本案例绝对root> resolve_config 退出 0：automation collaborative（project.yaml）、workflow minimal（rigor:minimal）。

盘点：combat GDD FOUND；systems-index ABSENT，跳过依赖层级检查；design/quick-specs ABSENT，没有 prior spec；数据文件 ABSENT。

暂按 Tweak 准备草稿。请求为基础伤害乘倍率，现有 GDD 已写 base*multiplier*crit；不能断言只是 Tuning 或默默删除 crit。分类与 crit 处理均待决定，没有代替用户作实施选择。

## Quick Design Spec 草稿：基础伤害倍率

Type: Tweak（暂定）
System: Combat
GDD Reference: design/gdd/combat.md — Detailed Design / Formulas
Date: 2026-11-16

Change Summary：已批准方向是基础伤害乘倍率；本草稿只表达基础计算步骤。
Motivation：把测试游戏的伤害方向写成可核算规则；没有玩家反馈输入，体验动机未评估。

Design Delta：原文为“伤害=base*multiplier*crit”。草稿表达“基础结算值=base*multiplier”。crit 是否为后续步骤、恒为 1 或取消尚待决定，在决定前不视为对原公式的替换。

New Rules / Values：base 为基础伤害、multiplier 为倍率；沿用 GDD 非负域。候选例子 (10,2) 的基础结算值为 20。未新设默认值、上限、舍入或非法输入策略，未指定不存在的数据文件。

Affected Systems：Combat 需在 crit 语义决定后核对 GDD；UI、生命值、存档等没有输入，影响未评估。没有新增状态或系统的证据。

候选 Acceptance Criteria（待批准）：

- (base=10,multiplier=2) 的基础计算步骤输出 20。
- 有限非负域内任一参数为零，基础计算步骤输出 0。
- 一般输入 (2.5,2) 输出 5，避免固定例子特判。
- 回归：crit=1.5 的原最终输出 30 在 crit 决策前不得擅改；最终验收必须明确两个计算步骤的关系。

GDD Update Required：若替换最终伤害规则则需要；若只澄清基础步骤则需确认表述。没有更新 GDD。

## 待决定与停止点

待决定：变更类型及旧/新规则差异；crit 处理；参数范围与数据来源；负数/非有限输入、精度、舍入和上限；影响系统与实现估算。不把缺少决定的草稿交作实施合同。

预期满足：完整草稿仅展示在获批 result.md 中，没有创建 design/quick-specs、保存设计文件或实施；未重复询问同一授权，停在 Approval and Filing 之前。

未评估：分类确认、草稿审批、文件保存、GDD 修改、story-readiness、实施及测试未执行。原生引擎运行未验证。
