# Story 001: 结果画面按 N 重试

> **Epic**: EPIC-ACCEPTANCE
> **Status**: Complete
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

- [x] AC-1：从真实游玩到达胜利结果后，Chrome 键盘 N 重试进入 play；完整 State（时间、分数、反馈、冷却、位置、判定目标、鱼位置等）等于同 seed 初始状态，事件仅为 start。
- [x] AC-2：从真实游玩到达超时失败后，Chrome 键盘 N 重试完成与 AC-1 相同的完整重置。
- [x] AC-3：标题、游玩、暂停中 N 均不重开；标题/暂停保持状态，游玩与无 N 的同 seed 同步进对照完全相同。
- [x] AC-4：胜利和失败画面的 R 与 Enter 重试继续完成整局重置；45 秒、3 鱼及原暂停、移动逻辑不变。
- [x] AC-5：主 brief 操作说明包含结果画面 N/R/Enter 重试，结果提示列出 N；构建、全套 npm test、test-run.sh web、smoke 及本轮同 seed 回放实际验证，保留并查看新截图。

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
**Status**: 本轮实际通过：新 N 3/3，全套 18/18（6 unit + 12 integration），Web smoke @boot 1/1。旧实现先红灯 1 passed / 2 failed，第一次 story-done 为 BLOCKED 且保持 Ready，详见 evidence/core-story/story-done-red.md。

## Dependencies

- Depends on: None
- Unlocks: None

## Completion Notes

**Completed**: 2026-11-17
**Verdict**: COMPLETE WITH NOTES
**Criteria**: 5/5 passing；必要自动化与视觉检查全部通过；人工试玩明确为本轮未评估后续。
**Deviations**: 无阻塞偏差；同 seed 仅提示变化经逐行轨迹、像素范围和已打开的新旧图核对；复用本轮已批准提示文案变更授权。
**Test Evidence**: tests/integration/n-retry.spec.ts；production/qa/evidence/core-story/green-build-and-suite.log、green-test-run.log、smoke-and-replay.log；无放宽或跳过必要测试。
**Reviewed by**: self, no independent review；完整 Story 为父代理自查；code-review 另有未参与实现的 lead-programmer helper，仅独立检查引擎范围，无阻塞发现。
**Review gates**: QL-TEST-COVERAGE skipped — Solo mode；LP-CODE-REVIEW skipped — Solo mode；显式 code-review 为 APPROVED WITH SUGGESTIONS（既存全局状态耦合建议，不扩大本轮范围）。
**Run result**: OBSERVED — 已查看胜利/失败前后四图；N 提示可见，重试后 45.0s、0/3 及初始位置；production/qa/evidence/story-001-n-retry/n-results-after.png。
**Same-seed run**: CHANGED, accepted — 只改结果提示，玩法行完全相同，0 errors；production/qa/evidence/grow-dusk-fish/story.png。
**Optional / NOT ASSESSED**: 人工试玩、手感、性能、乐趣难度；完整 smoke-check 人工批次 NOT ASSESSED（自动化 18/18、Web smoke 1/1 PASS），不声称人工 QA PASS 或 PROCEED。Web 参考文档缺版本探测标准字段，未在范围外补写。
**Scope**: 原型 31/31 SHA256 不变；配置仅追加 integration strict；无 Sprint/EPIC 表可更新；不安装、不提交、不发布。
**Authorization**: 沿用用户明确的保存、实施、验证及必要检查通过后关闭授权；未把 red 失败豁免，也未接受任何阻塞偏差。

## Calls beyond the design

- none beyond the design。
