# Story 001: 胜利后按 N 立即重开

> **Epic**: Signal Tiles
> **Status**: Complete
> **Layer**: Feature
> **Type**: Logic
> **Estimate**: S
> **Manifest Version**: N/A (minimal — no control manifest)
> **Last Updated**: 2026-11-18

## Context

**GDD**: `design/game-brief.md`
**Requirement**: `Brief MVP feature 5`

**ADR Governing Implementation**: N/A (minimal — no ADRs)
**ADR Decision Summary**: N/A (minimal — no ADRs)
**ADR Version**: N/A (minimal — no ADRs)

**Engine**: Web 8.3.4 | **Risk**: HIGH
**Engine Notes**: none (no ADR engine-compatibility analysis at minimal)

**Control Manifest Rules (this layer)**: N/A (minimal — no control manifest)

## Acceptance Criteria

依据简报的 Features 第 5 项、Core loop 和 Goal & fail state。

- [ ] **AC-1**　打开游戏，按 `Enter`，再单独按三次 `Space`，第三格亮起时立即显示「胜利」，分数为 `3`。在胜利画面发送一次浏览器键盘 `N` 按键，游戏直接进入进行中（`play`）。
- [ ] **AC-2**　`N` 触发重开的当步，三格全暗、分数为 `0`、胜利标记清空。
- [ ] **AC-3**　重开后直接单独按 `Space` 三次，按原顺序每次亮一格并加 `1` 分，第三次再次显示「胜利」，分数为 `3`。
- [ ] **AC-4**　在待机、已亮一格的进行中和纯展示页（`scene=figures`）各发送一次 `N` 按键，当前场景、已亮格数、分数和胜利标记均不因该键改变。
- [ ] **AC-5**　在待机、已亮一格的进行中、初次胜利和经 `N` 重开后再次胜利时分别按 `R`，均回到待机、三格全暗、分数为 `0`。随后按 `Enter` 仍能开始。纯展示页仍忽略 `R`。

## Implementation Notes

- 沿用 `src/input.ts` 的真实键盘入口，在 `src/game/rules.ts` 中处理 `results` 到 `play` 的转换，并复用现有的清零状态。
- 用浏览器键盘事件验证 AC-1，以覆盖键盘入口和场景规则。其余条件可通过界面或现有重放钩子观察。

## Out of Scope

- 胜利画面的文案与布局、额外关卡、排行榜及发布。

## Files

- `src/input.ts`
- `src/game/rules.ts`
- `tests/unit/rules.test.ts`
- `tests/integration/boot.spec.ts`

## QA Test Cases

*N/A — no qa-lead specs at this tier; implement against the Acceptance Criteria above*

## Test Evidence

**Story Type**: Logic
**Required evidence**: 本次明确要求先验证新用例失败，再执行完整测试和 R 键回归。

**Status**: [x] Passed — 新用例在旧代码上按预期失败，实施后完整测试通过。

- [本条故事验收记录](../../qa/evidence/story-001-restart-from-victory/verification.md)记录实际测试、截图和同种子重放。
- [grow 迁移证据](../../qa/evidence/grow-signal-tiles/grow.md)为变更前基线。人工试玩未评估。

## Dependencies

- Depends on: None。已有 grow Web 构建、重放钩子和测试。
- Unlocks: None。

## Completion Notes

**Completed**: 2026-11-18
**Criteria**: 5/5。Playwright 使用真实浏览器键盘覆盖胜利后重开、当步清零、再次胜利、其他场景忽略 N，以及 R 的待机重置与展示页行为。
**Deviations**: 无设计偏差。人工试玩未评估。
**Test Evidence**: [上一轮红灯及截图](../../qa/evidence/story-001-restart-from-victory/verification.md)。本轮通过 `test-run.sh web` 重跑完整测试，Vitest 3/3、Playwright 6/6，包含 `@boot` 和 R 键回归，失败 0，`zero_tests=no`，`web:pass`。[Vitest 日志](../../qa/evidence/story-001-restart-from-victory/story-done-test-run.log.unit) · [Playwright 日志](../../qa/evidence/story-001-restart-from-victory/story-done-test-run.log.e2e)
**Run result**: OBSERVED — [初次胜利，三格亮、3 分](../../qa/evidence/story-001-restart-from-victory/01-victory.png)；[按 N 后正在点亮，三格暗、0 分](../../qa/evidence/story-001-restart-from-victory/02-restarted.png)。本轮核对两张截图及四个对应文件的内容戳。
**Reviewed by**: self, no independent review（Solo 跳过 QL-TEST-COVERAGE 与 LP-CODE-REVIEW）
**Same-seed run**: SAME — 对照 grow reference，match yes、errors 0，截图哈希一致。[重放画面](../../qa/evidence/grow-signal-tiles/story.png)

## Calls beyond the design

- none beyond the design
