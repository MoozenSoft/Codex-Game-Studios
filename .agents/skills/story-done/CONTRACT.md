# $story-done — Handoff Contract

## Role in Pipeline
Closes the implementation loop for a single story by verifying every acceptance criterion, checking test evidence, detecting GDD/ADR deviations, and — after user approval — updating the story file to `Status: Complete` with a `## Completion Notes` section.

## Inputs Required

### Files That Must Exist
| File | Required Fields / Sections | Read-Only? |
|------|---------------------------|-----------|
| `production/epics/**/*.md` (the story file) | `Status:` (expected: `In Progress`, or `Ready` if `$dev-story` was skipped — `$dev-story` sets `In Progress`, and `$story-done` is the only skill that closes a story it verified — `$dev-story`'s dependency option `[C]` also sets `Complete`, on a dependency the user says is done, after an ask), `Type:`, `Manifest Version`, TR-ID(s), ADR reference(s), `## Acceptance Criteria`, list of files to create/modify, `## Test Evidence` path | No — status and completion notes written after approval |
| `docs/architecture/tr-registry.yaml` | Entry per TR-ID with current `requirement` text | Yes |
| GDD section referenced by each TR-ID | Acceptance criteria and key rules for cross-check | Yes |
| `docs/architecture/adr-NNNN-[slug].md` (referenced ADR) | `## Decision`, `## Consequences` | Yes |
| `docs/architecture/control-manifest.md` | `Manifest Version:` header date, forbidden patterns | Yes (existence checked; absent = skip staleness check) |
| `production/session-state/active.md` | Active story path (used when no argument given) | No — `<!-- CHECKPOINT -->` block overwritten |

> **Tier.** The TR registry, GDD-section and ADR rows are `standard`/`full` inputs.
> At `workflow: minimal` the story traces to the brief, and Phase 5 runs no GDD
> or ADR check; the manifest, hardcoded-value and scope checks still run. At
> `qa.level: minimal` no test evidence is required (SKILL.md Phase 4) — but the
> Visual/UI run-and-observe screenshot is not waived.

### Test Evidence Files (presence checked, not pre-required to exist — absence triggers gate)
| Story Type | Expected Location |
|------------|------------------|
| Logic | `tests/unit/[system]/[story-slug]_test.[ext]` |
| Integration | `tests/integration/[system]/[story-slug]_test.[ext]` OR `production/qa/playtests/` playtest record |
| Visual/Feel | `production/qa/evidence/[story-slug]-evidence.md` + a retained screenshot |
| UI | A retained screenshot of each screen touched, under `production/qa/evidence/` — no evidence doc or sign-off required |
| Config/Data | `production/qa/smoke-*.md` |

### Preconditions
- The story file must be findable either by argument path, in `production/session-state/active.md`, or in the current sprint file as `IN PROGRESS`
- Implementation must have been attempted (the files the story's `## Files` section lists should exist) — this skill does not implement; it verifies
- At `qa.level: full`, a Config/Data story's smoke report is BLOCKING by default (an explicit `testing.strict.config: false` keeps it advisory), and any UNTESTED acceptance criterion blocks; at `standard` only more than half untested blocks
- For Logic and Integration stories, the test file at the `## Test Evidence` path must **exist** before a COMPLETE verdict is possible — unless `testing.strict` in `project.yaml` sets that type to advisory (`testing.strict.logic`/`.integration: false`), in which case a missing test is recorded as a warning but does not block
- For Visual/Feel and UI stories, a retained screenshot must exist under `production/qa/evidence/` before a COMPLETE verdict is possible, and for Visual/Feel an evidence doc with every sign-off `[x] Approved` too (UI needs the screenshot only, as `coding-standards.md` says) — unless `testing.strict.visual`/`.ui` is set to `false`, in which case the gap is recorded as a warning but does not block
- 必要测试必须具有当前 tree、依赖及环境一致的通过证据；没有可复用结果时运行相关测试。文件存在不代表通过；必要失败为 BLOCKED，必要未评估为 NOT ASSESSED，均不得 COMPLETE。可选缺项依当前严格度明确记录。见 SKILL.md Phase 4。

## Verdicts Emitted
`COMPLETE` / `COMPLETE WITH NOTES` / `NOT ASSESSED` / `BLOCKED`.

`NOT ASSESSED` outranks `COMPLETE` — one or more acceptance criteria could not
be evaluated at all, which is not the same as evaluating them and finding them
met. Precedence is `BLOCKED`, then `NOT ASSESSED`, then `COMPLETE WITH NOTES`,
then `COMPLETE`; see the verdict section of `SKILL.md`.

## 关闭资格

此表适用于所有关闭写入与协作模式，必须先于 Phase 7 的关闭选项执行。必要项失败、未知或缺环境时，关闭授权不能替代实际通过，也不能直接写 Story、sprint 或 Epic 为完成。真实需求变更须先更新要求，再重新评估。

| Verdict | Close eligibility |
| --- | --- |
| `COMPLETE` | `ALLOW` |
| `COMPLETE WITH NOTES` | `ALLOW` |
| `NOT ASSESSED` | `DENY` |
| `BLOCKED` | `DENY` |

## Outputs Produced

### Files Written
| File | Guaranteed Fields / Sections | Notes |
|------|------------------------------|-------|
| `production/epics/**/*.md` (the story file) | `Status: Complete`, `## Completion Notes` block (date, criteria count, deviations, test evidence path, code review status, Reviewed by) | updated after explicit user approval |
| `production/sprint-status.yaml` | `status: done`, `completed: [date]`, top-level `updated` field | updated silently alongside story file if file exists |
| `docs/tech-debt-register.md` | Advisory deviation entries (if user confirms) | appended if advisory deviations exist and user agrees |
| `production/session-state/active.md` | `<!-- CHECKPOINT -->` block: current task (story path, verdict, closed or left open), next step (the next story, or the fix the verdict named), blocker, tech debt count | written on every verdict, closed or not, by `session-state.sh checkpoint`: the block is replaced, never appended (the file is created from `.agents/docs/templates/session-state.md` if absent) |

### Output Guarantees
- `Status: Complete` 仅在关闭资格为 ALLOW 且有明确授权时写入；复用会话中同一范围的“必要结果通过后关闭”授权，不重复要求同一批准。BLOCKED / NOT ASSESSED 不得关闭。
- `## Completion Notes` always contains: completion date, criteria pass count, deviation summary, test evidence path (or "None required"), code review status, and a Reviewed by line: `lead-programmer`, `$code-review (you said you ran it; not verified here)`, or `self, no independent review` when nobody else reviewed the work
- Session state always records the final verdict and the next recommended story path

## Immutability Rules
- READS but does NOT modify: `docs/architecture/tr-registry.yaml`, referenced ADRs/GDDs, `docs/architecture/control-manifest.md`, source files and test files. 必要测试可执行，但本 Skill 不改实现或测试来修复失败。
- MODIFIES: the story `.md` file (status + completion notes), `production/sprint-status.yaml` (if exists), `production/session-state/active.md` (the `<!-- CHECKPOINT -->` block, overwritten), `docs/tech-debt-register.md` (append a row, and update its `Last updated:` and `Total items:` lines, only with user approval)
- Does NOT write to the code root or the test root under any circumstances

## Hard Constraints (Never Violate)
- Never sets `Status: Complete` without close eligibility ALLOW and explicit approval covering the same scope.
- Never marks a Logic story Complete on a missing unit test when its resolved gate level is BLOCKING — the level is BLOCKING by default and whenever `testing.strict.logic` is `true`; it is ADVISORY only when `testing.strict.logic` is explicitly `false`
- Never marks an Integration story Complete on missing evidence (integration test file or playtest session log) when its resolved gate level is BLOCKING — BLOCKING by default and under `testing.strict.integration: true`; ADVISORY only under an explicit `false`
- Never marks a Visual/Feel or UI story Complete on a missing retained screenshot in `production/qa/evidence/` when its resolved gate level is BLOCKING — BLOCKING by default and under `testing.strict.visual`/`.ui: true`; ADVISORY only under an explicit `false`. A written description of a visual check is not a substitute for the image
- Never auto-fixes failing acceptance criteria — report failures and ask the user what to do
- Never enters the close-writing branch on BLOCKED or NOT ASSESSED, including when the user asks to accept the risk; keep completion states unchanged and record blockers in the report/checkpoint.
- Never reclassifies a necessary condition as optional merely to close; after an actual scope change, update requirements and assess them again.

## Downstream Skill Expects
**Next skill:** `$gate-check` (Production → Polish gate, or end-of-sprint review)
- It will read: story files in `production/epics/` checking `Status: Complete` and presence of `## Completion Notes`
- It will read: `tests/unit/` and `tests/integration/` for test file presence and will run the test suite via Bash
- It assumes: every Complete Logic story whose `testing.strict.logic` gate resolved to BLOCKING (the default) has a corresponding test file that **exists**; under an explicit `testing.strict.logic: false` a Logic story may be Complete with the test gap documented in `## Completion Notes`
  > 完成状态与具体运行证据分开核对。story-done 已核对必要测试结果；gate-check 仍按自己的范围核对是否有当前可复用证据或需要运行更广的套件。没有运行器时为 NOT ASSESSED，不能从状态文字推定通过。
- It assumes: Visual/Feel and UI stories that are Complete have a retained screenshot in `production/qa/evidence/`, and Visual/Feel ones a signed-off evidence doc as well — that gate is BLOCKING by default; only under an explicit `testing.strict.visual`/`.ui: false` may such a story be Complete with the deviation documented in `## Completion Notes`
- It will read: `production/sprint-status.yaml` for `status: done` entries if that file exists

## Known Fragile Points
- The story's `## Test Evidence` path is checked first; when it does not match, Phase 4 searches `tests/unit/[system]/` (or `tests/integration/[system]/`) before flagging the test missing, so a file under a slightly different name is still found — one outside that folder is not
- The scope check reads the story's `## Files` list (filled by `$create-stories`, replaced by `$dev-story`). A story written before the section existed falls back to the checkpoint's **Files in progress** when it names this story, else reports scope NOT ASSESSED; changes already committed are not seen, since it compares uncommitted files only
- If `Type:` is absent from the story header, test evidence gate enforcement is ADVISORY only — stories can slip through without tests
- Manifest version staleness check is skipped if `docs/architecture/control-manifest.md` does not exist; the check being skipped is noted in the report but is non-blocking
- `production/sprint-status.yaml` update is silent (no separate approval); if that file uses a different key structure than expected, the update silently fails and sprint tracking becomes stale
- The traceability table escalation rule (>50% UNTESTED = BLOCKING at `qa.level: standard`, any UNTESTED at `full`) can be triggered by deferred Visual/Feel criteria that are legitimately not automatable — ensure deferred criteria are explicitly marked `DEFERRED` (not left as unchecked) to avoid false escalation
