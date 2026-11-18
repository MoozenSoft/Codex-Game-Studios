# Skill Test Spec: $qa-plan

> Codex 验收约定：本文件保留领域用例；配置来源为 `.agents/skills/` 与 `.codex/agents/`。提问、确认、写入及并发按实际客户端能力和 `automation-modes.md` 执行，复用已有授权；静态推理不等于真实运行通过。

## Skill Summary

`$qa-plan [sprint | feature: system-name | story: path]` generates a QA plan
before implementation. `sprint` reads the most recent file in
`production/sprints/` (or `production/sprint-status.yaml` when present) for its
story list; `feature:` globs `production/epics/*/story-*.md` by system name;
`story:` loads one file; no argument asks for the scope with `当前 Codex 可用的提问工具`.
A referenced story file that does not exist is noted as MISSING and the plan
continues; a scope with zero stories stops with `NOT ASSESSED — no stories in
scope` and a route (e.g. "No sprint plan found. Run `$sprint-plan new`.").

Story fields are collected with targeted greps. A declared `Type:` is accepted
as-is; a missing one is inferred from the acceptance criteria and flagged as a
gap. A story with no `## Acceptance Criteria` is full-read and reported as a QA
finding, never skipped. After a classification summary table, the plan
(Test Summary, Automated Tests Required, Manual QA Checklist, Smoke Test Scope,
Playtest Requirements, Definition of Done) is shown, then two independent
single-select questions ask whether to write `production/qa/qa-plan-[sprint-slug]-[date].md`
and whether to back-fill `## QA Test Cases` in the story files. All four answer
combinations are supported. Without the tool, explicit plain-text answers are
collected; an unanswered choice grants no write. `qa.level`
changes the plan's depth, but no level drops the Visual/Feel and UI screenshot
rows. No director gates apply.

---

## Static Assertions (Structural)

Checked against the SKILL.md by `$skill-test spec` — no fixture needed.

- [ ] Skill frontmatter 包含可解析的 `name`、`description`，目录名与 name 一致，不依赖旧客户端字段。
- [ ] Has ≥2 phase headings
- [ ] Contains the verdict keyword `NOT ASSESSED` for an empty scope
- [ ] Asks for approval before writing: an `当前 Codex 可用的提问工具` option naming `production/qa/qa-plan-[sprint-slug]-[date].md`, and the rule "Never write the plan without asking"
- [ ] Has a next-step handoff (`$smoke-check sprint` after implementation, `$story-done` checks for the test files)

---

## Director Gate Checks

None. `$qa-plan` is a planning utility. It spawns no agents (the workflow does not delegate) and no director gates apply.

---

## Fixture Defaults

Every case's `project.yaml` sets `modes.rigor: minimal` and
`modes.automation: collaborative`, with no `project.local.yaml`, unless its own
Fixture says otherwise. Rules: `studio-tests/AGENTS.md` §
Fixture defaults.

---

## Test Cases

### Case 1: Happy Path — Sprint With Four Typed Stories

**Fixture:**
- `production/sprints/sprint-003.md` is the most recent sprint and references 4
  story files, each with acceptance criteria and a declared Type: Logic,
  Integration, Visual/Feel, UI
- The stories reference GDDs in `design/gdd/`; `engine.name: Godot`
- `qa.level: standard`; `modes.automation: collaborative`

**Input:** `$qa-plan sprint`

**Expected behavior:**
1. Skill reads the most recent sprint file and reports "Building QA plan for 4
   stories in [scope]."
2. Story fields are collected with section greps; each declared Type is accepted
   without re-classification
3. A classification summary table is shown before the plan is generated
4. The plan's Test Summary maps Logic → unit test under `tests/unit/[system]/`,
   Integration → integration test under `tests/integration/[system]/`,
   Visual/Feel → screenshot + lead sign-off, UI → retained screenshot of each
   screen touched
5. The plan is shown, then two independent single-select questions offer the
   plan-file write and story back-fill; a plain-text pair is used if no tool is
   available. Only explicitly approved actions execute
6. After writing, next steps name `$smoke-check sprint` (after implementation)
   and `$story-done`

**Assertions:**
- [ ] All 4 stories appear in the plan, each with its declared Type unchanged
- [ ] The classification summary table appears before the plan
- [ ] Logic and Integration rows name test paths under `tests/unit/` and `tests/integration/`
- [ ] The UI row's manual verification is the retained screenshot of each screen touched, not a step-through
- [ ] Nothing is written without approval for that output, and an approved plan is written to `production/qa/qa-plan-[sprint-slug]-[date].md`
- [ ] Next steps name `$smoke-check sprint` and `$story-done`

---

### Case 2: Story Without Acceptance Criteria and a Missing Story File

**Fixture:**
- The most recent sprint file references 4 story paths
- One story has no `## Acceptance Criteria` section
- One referenced story path does not exist on disk
- The other 2 stories are complete

**Input:** `$qa-plan sprint`

**Expected behavior:**
1. The missing path is noted as MISSING and the plan continues
2. The story whose AC grep matched nothing is full-read, and the plan says it
   has no testable criteria — a QA finding, not a skipped story
3. The 2 complete stories are classified and planned normally
4. Approval is asked before writing

**Assertions:**
- [ ] The missing file is reported as MISSING without failing the whole plan
- [ ] The story with no acceptance criteria is full-read and reported as a QA finding
- [ ] That story is not silently dropped from the plan
- [ ] The two complete stories receive normal test assignments

---

### Case 3: Mode Variant — qa.level minimal

**Fixture:**
- Same 4-story sprint as Case 1
- `qa.level: minimal`

**Input:** `$qa-plan sprint`

**Expected behavior:**
1. Skill produces only a minimal smoke plan
2. The "Automated Tests Required" section is omitted and the Test Summary's
   "Automated Test Required" column is blanked
3. The Definition of Done drops the test-file and smoke rows only; it still
   requires a retained screenshot of each screen touched for the Visual/Feel
   and UI stories, and a signed-off evidence doc for the Visual/Feel story —
   `qa.level` waives tests, never the screenshot
4. Approval is asked before writing

**Assertions:**
- [ ] No "Automated Tests Required" section appears
- [ ] The Test Summary's automated-test column is blank
- [ ] The Definition of Done has no test-file or smoke-check rows
- [ ] The Definition of Done still requires the retained screenshot for the Visual/Feel and UI stories, and the signed-off evidence doc for the Visual/Feel story
- [ ] Approval is still asked before the plan is written

---

### Case 4: No Sprint Plan — NOT ASSESSED

**Fixture:**
- `production/sprints/` contains no files
- No `production/sprint-status.yaml`
- `modes.rigor: standard` (so sprints are expected)

**Input:** `$qa-plan sprint`

**Expected behavior:**
1. The resolved scope contains zero stories
2. Skill stops before Phase 2 and reports `NOT ASSESSED — no stories in scope`,
   naming the scope searched and the empty path
3. Skill routes: "No sprint plan found. Run `$sprint-plan new`."
4. No plan is generated and no write approval is asked

**Assertions:**
- [ ] Verdict is `NOT ASSESSED — no stories in scope`
- [ ] The empty path `production/sprints/` is named
- [ ] `$sprint-plan new` is suggested
- [ ] No plan document with empty tables is produced, and nothing is written

---

### Case 5: Director Gate Check — None

**Fixture:**
- A sprint with typed stories and acceptance criteria
- Any review mode

**Input:** `$qa-plan sprint`

**Expected behavior:**
1. Skill classifies stories and generates the plan
2. No director or other agent is spawned; no gate IDs appear
3. The only interactive step after scope resolution is the single write approval

**Assertions:**
- [ ] No director gate is invoked and no gate skip message appears
- [ ] No subagent is spawned
- [ ] Phases 2–4 run without asking the user anything
- [ ] Exactly one approval prompt precedes the write

---

### Case 8: Independent output choices and unanswered choice

**Fixture:**
- A valid story has generated QA test cases and the plan has been shown.
- The current question tool supports single selection only.
- Existing session authorization does not cover either output write.

**Input:** `$qa-plan story: production/stories/story-001.md`

**Expected behavior:**
1. Ask independent plan-file and story-backfill questions.
2. Exercise all four explicit yes/no pairs: both outputs, only the plan, only
   story back-fill, or neither. Write exactly the approved outputs.
3. Variant: dismiss one question. Wait or report its output choice unanswered;
   do not call the dismissal a decline or claim that output was written.
4. With no tool, collect the explicit pair in plain text and wait.

**Assertions:**
- [ ] Either output can be selected independently and both can be declined.
- [ ] A missing response authorizes no write and produces no false completion claim.
- [ ] The summary and checkpoint name only files actually written.
- [ ] Async submission is WAITING, not an approval: no answer-dependent write
      or completion occurs until the later user response. Sync is called only in
      modes where it is available; schemas are selected from the actual tools.

---

## Protocol Compliance

- [ ] Stops with `NOT ASSESSED — no stories in scope` when the scope is empty, and routes to the producing skill
- [ ] Notes missing story files as MISSING and continues
- [ ] Accepts declared `Type:` values; infers and flags a missing Type
- [ ] Never skips a story because its acceptance-criteria section is absent
- [ ] Shows the classification table and the plan before asking to write
- [ ] Writes only after the `当前 Codex 可用的提问工具` approval; back-fills story files only when that option is selected

---

## Coverage Notes

- `feature: [system-name]` and `story: [path]` scopes, and the no-argument
  scope question, are not separately tested.
- A story with no `Type:` field (inferred from acceptance criteria and flagged
  as a gap) is covered only by protocol compliance.
- The back-fill option (editing `## QA Test Cases` in each story file) is not
  tested in detail.
- At `rigor: minimal`, the empty-sprint route points to `$qa-plan feature:` or
  `$qa-plan story:` instead of `$sprint-plan new`; not separately tested.
