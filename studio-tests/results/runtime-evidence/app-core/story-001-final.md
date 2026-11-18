# Story 001: 结果页支持 N 键重试

> **Epic**: EPIC-APP-ACCEPTANCE
> **Status**: Complete
> **Layer**: Feature
> **Type**: Integration
> **Estimate**: S
> **Last Updated**: 2026-11-17

## Context
**GDD**: design/game-brief.md
**Requirement**: Brief MVP feature 7 — 结果页 N 键也可重试，原 R/Enter 保留，非结果状态不重开。
**ADR Governing Implementation**: N/A — minimal 允许无 ADR，此功能不改变架构。
**ADR Decision Summary**: N/A — minimal，无架构变更。
**Engine**: Web 8.3.4
**Engine Notes**: N/A — 不新增引擎 API，仅扩展既有 KeyboardEvent.code 分支。
**Control Manifest Rules**: N/A — manifest not yet created。

## Acceptance Criteria
- [x] AC-1: over 和 results 状态按 N 后进入 play，计时与渔获清零。
- [x] AC-2: title、play、pause 状态按 N 不重新开始；游玩中位置不重置。
- [x] AC-3: 原 R/Enter 结果页重试继续有效；60 秒、3 条目标和暂停规则不变。

## Implementation Notes
仅对两个结果状态的重试条件增加 KeyN。保留当前 Enter / R 提示，不额外设计提示文案；N 为附加快捷键。
无性能影响预期：仅增加按键集合查询，不新增循环或分配。

## Out of Scope
- 不修改冻结原型、只读源、框架、计时参数或其它玩法；不新增 Story。

## Files
- src/main.ts
- tests/integration/n-retry.spec.ts
- tests/integration/retry.spec.ts

## QA Test Cases
- AC-1: 真实 Chrome 进入两个结果状态，按 N，固定步进后检查 scene、t 与 score。
- AC-2: 分别进入三个非结果状态，预先移动后按 N，确认场景和位置不重置。
- AC-3: 执行现有 R/Enter、计时规则及启动测试，确认回归通过。

## Test Evidence
**Story Type**: Integration
**Required evidence**: tests/integration/n-retry.spec.ts 必须真实 Chrome 通过；即使 qa.level minimal，本次用户显式要求仍为必要测试。
截图：production/qa/evidence/story-001-n-retry/。
状态与日志：production/qa/evidence/app-acceptance/commands.jsonl。

## Dependencies
- Depends on: None
- Unlocks: None

## Completion Notes
**Completed**: 2026-11-17
**Criteria**: 3/3 passing。AC-1/2：n-retry.spec.ts五种状态；AC-3：R/Enter七项、60秒超时、P暂停/继续、计时规则和启动测试。
**Deviations**: 无必要偏离。人工体验、乐趣与完整人工smoke为可选未评估项；code-review建议后续清理旧常量与拆分依赖，不扩大本次范围。
**Test Evidence**: production/qa/evidence/app-acceptance/final-suite.log，19/19（3 Vitest、16 Chrome），rule web:pass，zero_tests no，两半exit0；复用相同实现、依赖与环境的通过结果。
**Reviewed by**: lead-programmer 独立engine/code-review，APPROVED WITH SUGGESTIONS；QL-TEST-COVERAGE和LP director gate skipped — Solo mode。
**Run result**: OBSERVED — production/qa/evidence/story-001-n-retry/results.png、pause.png；真实Chrome与截图已检查。
**Same-seed run**: SAME — against accepted，match yes、errors0，production/qa/evidence/grow-app-dusk-fish/story.png。
**Authorization**: 用户已明确批准必要结果通过后关闭；首次必要失败时保留Ready并判BLOCKED，未绕过门禁。

## Calls beyond the design
- none beyond the design。
