# Story 001: 结果画面按 N 重试

> **Epic**: EPIC-ACCEPTANCE
> **Status**: Ready
> **Layer**: Core
> **Type**: Integration
> **Estimate**: S
> **Build step**: deepen — 倒计时、胜负、暂停和重试
> **Manifest Version**: N/A — manifest not yet created
> **Last Updated**: 2026-11-17

## Context

**GDD**: `design/game-brief.md`（minimal 下以已批准 brief 代替 GDD）
**Requirement**: Brief Features 第 7 项“胜利或失败画面重试”的已批准增量：增加 N；原 R/Enter 保留，非结果状态 N 不重开。

**ADR Governing Implementation**: N/A — minimal 允许本次输入增量不引用 ADR，无新增架构决定。
**ADR Decision Summary**: N/A — 复用结果状态现有 begin/reset 路径。
**ADR Version**: N/A

**Engine**: Web 8.3.4 | **Risk**: LOW
**Engine Notes**: N/A — 不涉及新引擎 API；真实 Chrome KeyboardEvent 输入与现有固定步进钩子验证。

**Control Manifest Rules (this layer)**:
- N/A — manifest not yet created。
- no performance impact expected — 只扩展结果场景的按键条件，不改变 gameplay loop 的计算或数值。

## Acceptance Criteria

- [ ] AC-1：从真实游玩到达胜利结果后，Chrome 键盘 N 重试进入 play；完整 State（时间、分数、反馈、冷却、位置、判定目标、鱼位置等）等于同 seed 初始状态，事件仅为 start。
- [ ] AC-2：从真实游玩到达超时失败后，Chrome 键盘 N 重试完成与 AC-1 相同的完整重置。
- [ ] AC-3：标题、游玩、暂停中 N 均不重开；标题/暂停保持状态，游玩与无 N 的同 seed 同步进对照完全相同。
- [ ] AC-4：胜利和失败画面的 R 与 Enter 重试继续完成整局重置；45 秒、3 鱼及原暂停、移动逻辑不变。
- [ ] AC-5：主 brief 操作说明包含结果画面 N/R/Enter 重试，结果提示列出 N；构建、全套 npm test、test-run.sh web、smoke 及本轮同 seed 回放实际验证，保留并查看新截图。

## Implementation Notes

在 src/main.ts 的 over/results 输入条件加入 KeyN，复用 begin()，更新两处结果提示。不得改变 reset、时长、目标、随机数和其它场景。所有决定来自本轮明确授权。

## Out of Scope

- 冻结的整个 prototypes/dusk-fish（31 文件）；不重做 grow。
- .agents、.codex、AGENTS、其它工作流、外层仓库及全局设置；不安装、不提交、不发布。
- 仅允许 project.yaml 追加 testing.strict.integration: true，不改变 rigor、automation、engine。
- 人工试玩、乐趣难度判断及 PROCEED 结论未评估。

## Files

- src/main.ts
- tests/integration/n-retry.spec.ts
- design/game-brief.md（只更新操作说明及第 7 项说明）

## QA Test Cases

无 qa-lead 独立规格（minimal/solo）。以下由本轮用户验收输入给定，不冒充 qa-lead：

- AC-1/2：Given 固定 seed 到达胜利/失败且有本局状态；When page.keyboard.press('n') 后执行一固定步；Then 场景 play，完整 State 等于初始状态，events 等于 ['start']。继续同输入验证 RNG 序列重置。
- AC-3：Given 标题、移动一秒的 play、pause；When 真实 N 输入；Then 前后状态或与不按 N 的对照一致。
- AC-4：Given 胜利/失败；When 真实 R/Enter；Then 完整 State 和 events 重置；复用现有回归用例。
- AC-5：检查真实构建/测试输出、同 seed 比较及打开截图，提示不得遮挡；未做人工试玩按未评估记录。

## Test Evidence

**Story Type**: Integration
**Required evidence**: `tests/integration/n-retry.spec.ts` 必须实际通过；本轮显式要求优先于 qa.level minimal 的默认豁免，testing.strict.integration 为 true。旧实现必须先红灯，必要失败时 story-done 必须 BLOCKED，不能凭文件存在关闭。
**Logs**: `production/qa/evidence/core-story/`
**Screenshots**: `production/qa/evidence/story-001-n-retry/`（本轮生成）
**Report**: `production/qa/evidence/core-story-result.md`
**Status**: 尚未运行；不声明通过。

## Dependencies

- Depends on: None
- Unlocks: None
