---
name: test-setup
description: "本项目游戏工作室工作流：test-setup。Sets up the test framework and CI: tests/ directory, engine runner, GitHub Actions workflow. Use once, before the first sprint."
---

**会话模型要求** 使用 `sol` 家族最新可用模型。执行前按 `.agents/docs/model-tiers.md` 解析具体型号并核对会话。

执行前读取 `.agents/docs/codex-runtime.md` 与 `.agents/docs/automation-modes.md`，按当前客户端工具执行以下领域流程。
参数从用户本次请求中读取，不依赖变量替换；用法：`[force]`。
正文里的逐项确认遵循已解析模式及当前会话明确授权；已批准的决定或变更集合直接沿用。



显式执行并检查结果：

```bash
bash ".agents/skills/test-setup/../../scripts/yaml-helper.sh" resolve_config --keys automation,workflow,qa.level
```

**Automation mode**: Resolve `modes.automation` (`project.local.yaml` →
`project.yaml` → default `collaborative`). Every question and
every file write follows `.agents/docs/automation-modes.md`
(collaborative asks always · guided major-only · autonomous logs and proceeds;
`automation_always_ask` categories always prompt).

# Test Setup

This skill scaffolds the automated testing infrastructure for the project.
It detects the configured engine, generates the appropriate test runner
configuration, creates the standard directory layout, and wires up CI/CD
so tests run on every push.

Run this once during the Technical Setup phase, before any implementation
begins. A test framework installed at sprint start costs 30 minutes.
A test framework installed at sprint four costs 3 sprints.

**Output:** `tests/` directory structure + `.github/workflows/tests.yml`

---

## Phase 1: Detect Engine and Existing State

**Read `references/1-detect.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 2: Present Plan

**Read `references/2-plan.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 3: Create Directory Structure

**Read `references/3-directories.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 4: Create CI/CD Workflow

**Read `references/4-ci.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 5: Create Smoke Test Seed

**Read `references/5-smoke-seed.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Phase 6: Post-Setup Summary

**Read `references/6-summary.md` now and follow it** — this phase's steps are in that file, not here. Read it again if the conversation was compacted or resumed during this phase.

## Collaborative Protocol

- **Never overwrite existing test files** — only create files that are missing.
  If a test runner file exists, leave it as-is.
- **Always ask before creating files** — Phase 2 requires explicit approval.
- **Engine detection is non-negotiable** — if the engine is not configured,
  stop and redirect to `$setup-engine`. Do not guess.
- **`force` flag skips the "already exists" early-exit but never overwrites.**
  It means "create any missing files even if the directory already exists."
- For Unity CI, note that the `UNITY_LICENSE` secret must be configured
  manually. Do not attempt to automate license management.
