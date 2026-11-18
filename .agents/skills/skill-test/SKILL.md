---
name: skill-test
description: "本项目游戏工作室工作流：skill-test。Validate skill files for structural compliance and behavioral correctness. Four modes: static linter, spec, category rubric, audit."
---

**会话模型要求** 使用 `sol` 家族最新可用模型。执行前按 `.agents/docs/model-tiers.md` 解析具体型号并核对会话。

执行前读取 `.agents/docs/codex-runtime.md` 与 `.agents/docs/automation-modes.md`，按当前客户端工具执行以下领域流程。
参数从用户本次请求中读取，不依赖变量替换；用法：`static [skill-name | all] | spec [skill-or-agent-name] | category [skill-or-agent-name | all] | audit`。
正文里的逐项确认遵循已解析模式及当前会话明确授权；已批准的决定或变更集合直接沿用。



显式执行并检查结果：

```bash
bash ".agents/skills/skill-test/../../scripts/yaml-helper.sh" resolve_config --keys automation
```

**Automation mode**: Resolve `modes.automation` (`project.local.yaml` →
`project.yaml` → default `collaborative`). Every `当前 Codex 提问工具` call and
every file write follows `.agents/docs/automation-modes.md`
(collaborative asks always · guided major-only · autonomous logs and proceeds;
`automation_always_ask` categories always prompt).

# Skill Test

Validates skills (`.agents/skills/*/SKILL.md`) and agents (`.codex/agents/*.toml`)
for structural compliance and behavioral correctness. No external dependencies —
runs entirely within the existing skill/hook/template architecture.

**Four modes:**

| Mode | Command | Purpose | Token Cost |
|------|---------|---------|------------|
| `static` | `$skill-test static [name\|all]` | Structural linter — 7 compliance checks per skill, plus agent, delegation and compatibility observations | Low (~1k/skill) |
| `spec` | `$skill-test spec [name]` | Behavioral verifier — evaluates assertions in a skill's or agent's test spec | Medium (~5k each) |
| `category` | `$skill-test category [name\|all]` | Category rubric — checks a skill or agent against its category-specific metrics | Low (~2k each) |
| `audit` | `$skill-test audit` | Coverage report — skills, agent specs, last test dates | Low (~3k total) |

**What a pass proves.** Every mode reads files; none runs the skill. `static`:
the file has the structure a skill needs, not that it behaves. `spec`: read
closely, the instructions cover each case, not that Codex follows them when it
runs. `category`: the skill meets its category's rubric as written. `audit`:
which skills and agents have specs, and when each was last checked. What a skill
does shows only when it runs: a real request in a throwaway copy of the project,
on the parent session model, with and without the skill. Record static review
and runtime evidence separately.

---

## Phase 1: Parse Arguments

Determine mode from the first argument:

- `static [name]` → run 7 structural checks on one skill, or the agent observations on one agent
- `static all` → run 7 structural checks on all skills (Glob `.agents/skills/*/SKILL.md`), plus the observations for every agent
- `spec [name]` → read the skill or agent + its test spec, evaluate assertions
- `category [name]` → run category-specific rubric from `studio-tests/quality-rubric.md`
- `category all` → run category rubric for every skill and every agent that has a `category:` in catalog
- `audit` (or no argument) → read catalog, list all skills and agents, show coverage

If the argument is unrecognized, output usage and stop.

**The old spec folder.** Glob `CCGS Skill Testing Framework/catalog.yaml`. When
it exists, say so first: "`CCGS Skill Testing Framework/` was renamed
`studio-tests/` in 1.2.0, and this skill reads only `studio-tests/`. Move any
specs you wrote there; UPGRADING.md (v1.1.3 → v1.2.0, `studio-tests/`) says how."
Then go on with `studio-tests/`.

**Resolve the name before `spec` or `category`.** Look it up in
`studio-tests/catalog.yaml`: an entry under `skills:` is a skill
(`.agents/skills/[name]/SKILL.md`); an entry under `agents:` is an agent
(`.codex/agents/[name].toml`). With no catalog entry, use whichever of those two
files exists. Only when neither exists, report "'[name]' is neither a skill in
`.agents/skills/` nor an agent in `.codex/agents/`." and stop. A name that is
also an ordinary word is still a name: `$skill-test spec next-step` tests the `$next-step`
skill, never a request for this skill's usage.

The 7 checks lint SKILL.md structure, so they are skills-only. Given an agent
name, `static` runs only the observations below: an agent file has no
phases or verdict keywords to lint. Never report the agent as missing.

---

## Phase 2A: Static Mode — Structural Linter

For each skill being tested, read its `SKILL.md` and every file in its `references/` folder
fully, and run all 7 checks on them as one skill — the longest skills keep each
phase in `references/`. The frontmatter checks (1, 6 and 7) read `SKILL.md`.

### Check 1 — Codex frontmatter

要求可解析的 name、description，name 与目录一致；allowed-tools、model、context、user-invocable 等旧客户端字段不能作为运行机制。缺必要字段或语法无效为 FAIL。
读取 references 里的显式执行步骤；旧 shell 注入、客户端专用环境变量和隐式参数占位符残留同样是 FAIL。

### Check 2 — 流程结构

检查步骤是否足以完成所声明任务、输入输出与结束条件是否明确。不同流程不强制相同章节数；统计脚本给出章节事实，缺必要动作时列明具体缺项。

### Check 3 — 裁决与未评估

评审或门禁需要可判断的结论，并能报告未评估及原因；生成产物或查询配置的工作流不凭空增加通过裁决。
保留对应领域的 PASS/FAIL/CONCERNS、PROCEED/PIVOT/KILL 等词汇，不以某一种英文单词作为唯一合格信号。

### Check 4 — 协作模式与已有授权

按实际 automation 检查确认与写入行为：默认 collaborative 保留草稿和必要决定，guided 区分重大选择与细节，autonomous 记录决定。
所有模式沿用已批准范围；必要问题被跳过不算同意。不能要求所有 Skill 出现同一句 May I write 或依赖已删除的 allowed-tools 判定权限。

### Check 5 — 后续交接

输出说明产物、证据、未评估项和适当的下一步；未迁移或不可用的入口只提示限制，不能假装调用成功。

### Check 6 — 显式调用与委派

检查 agents/openai.yaml 的 policy 是否符合工作流约定；dev-story、story-done 保持显式调用。
委派读取 .codex/agents 中的真实角色，受实际工具与额度约束；context: fork 已退役，不按它或固定阶段数评分。

### Check 7 — 参数与实际配置

参数从用户本次请求读取，用法在正文中明确；配置通过 yaml-helper.sh 显式执行并检查输出。空参数、无效值、缺工具应有可见结果，不猜测已经成功。

### Agent and Delegation Observations (not scored)

Run `bash .agents/scripts/agent-check.sh --skill [name]` for a skill,
`bash .agents/scripts/agent-check.sh --agent [name]` for an agent, or
`bash .agents/scripts/agent-check.sh` once for `static all`. It prints
observations, never a verdict, and nothing here changes a skill's verdict. Report
them under `Observations:`, judging each:

- **`DELEGATION:`** a part of the skill that hands work to an agent. Read it and
  say whether the brief gives an objective, an output format, the tools and
  sources, and boundaries, and whether it hands the agent a job of only a few
  tool calls or a re-check of the skill's own work. Its `markers:` are word
  counts that show where to look, not a grade.
- **`agent`**：脚本输出实际 TOML 路径、model、指令中的必读 Skill。工具权限、并发额度和可用角色绑定参数以当前客户端为准，不能从角色文字推定。
- **异常**：TOML 无法解析、角色文件或必读资源缺失。子代理无法询问用户时，将必要问题交回父代理，不默认已经同意。
- **`OVERLAP:`** two descriptions that share distinctive words: say whether each
  still singles out its agent, or which request would reach the wrong one.

If the script cannot run, write `Observations: not run (<reason>)`. Never leave
the section out: a missing section reads the same as a clean one.

### Compatibility Observations (not scored)

Run `bash .agents/scripts/compat-inventory.sh --skill [name]` for a skill,
`bash .agents/scripts/compat-inventory.sh --agent [name]` for an agent, or
`bash .agents/scripts/compat-inventory.sh` once for `static all`. Each `FOUND:`
line identifies a remaining legacy environment variable, shell injection,
or runtime path, with its file and line number. Read each match, distinguish
historical explanation from an active execution dependency, and fail an active
dependency. `FILES` and `FOUND_LINES` are coverage counts, not proof that a
client workflow ran. Report the observations under `Compatibility:`.
A `NOT FOUND` line means the name matched no file: say so. If the script cannot run, write
`Compatibility: not run (<reason>)`.

---

### Static Mode Output Format

For a single skill:
```
=== Skill Static Check: /[name] ===

Check 1 — Frontmatter Fields:    PASS
Check 2 — 流程结构:              PASS (输入、输出与结束条件明确)
Check 3 — Verdict Keywords:      PASS (PASS, FAIL, CONCERNS)
Check 4 — 协作模式与已有授权:     PASS (沿用已批准的变更范围)
Check 5 — Next-Step Handoff:     WARN (no follow-up section found)
Check 6 — 显式调用与委派:         PASS (真实角色及任务边界明确)
Check 7 — 参数与实际配置:         PASS

Observations (not scored):
  Delegation, "Phase 3: Implementation" (line 202): ux-designer, ui-programmer.
    The brief names the output file and limits but no sources to read.

Compatibility (not scored):
  FILES: N · FOUND_LINES: 0
  仅为静态扫描结果，客户端运行尚未评估。

Verdict: WARNINGS (1 warning, 0 failures)
Recommended: Add a "Follow-Up Actions" section at the end of the skill.
```

For a single agent there is no verdict, only observations:
```
=== Agent Static Check: qa-lead ===

Model: [actual session model] · Effort: [actual session effort, or NOT ASSESSED]
工具权限和并发额度由当前客户端提供。
Observations (not scored):
  asks-user (lines 31, 52): tells the agent to get approval before writing.
  overlap with qa-tester (creation, regression, test): each still singled out.
Compatibility (not scored):
  TOML 已解析；必读资源路径均存在。原生角色绑定仍需实际运行。
```

A WARN or FAIL line names its cause in parentheses, and any verdict other than
COMPLIANT ends with a `Recommended:` line naming the fix.

The single-skill `Verdict:` is one of four values, the same as the `static all`
Result column: **COMPLIANT** (no warnings, no failures), **WARNINGS** (warnings,
no failures), **NON-COMPLIANT** (any FAIL), or **NOT ASSESSED** (the file could
not be read or parsed, or its checks could not run — name the reason).

For `static all`, produce a summary table then list any non-compliant skills:
```
=== Skill Static Check: All 75 Skills ===

Skill                  | Result       | Issues
-----------------------|--------------|-------
gate-check             | COMPLIANT    |
design-review          | COMPLIANT    |
story-readiness        | WARNINGS     | Check 5: no handoff
...

Summary: 48 COMPLIANT, 3 WARNINGS, 1 NON-COMPLIANT, 1 NOT ASSESSED
Aggregate Verdict: N WARNINGS / N FAILURES / N NOT ASSESSED

Agents (observations, not scored): 49 read
  TOML 可读: N agents · 必读资源缺失: N
  Overlap pairs: [each pair, with whether both are still singled out]
  Delegation blocks: N in N skills; [the ones whose brief lacks a part]

Compatibility (not scored): N FOUND lines in N of N files read
  [legacy dependency]: N files, N hits; ...
```

**`NOT ASSESSED` is a per-skill result here, not only an aggregate line.** A skill
whose file is missing or otherwise unreadable (permissions, not found), so no
check could even start, is reported as `NOT ASSESSED` with the reason — never
omitted from the table and never counted as COMPLIANT. Ranked **above
COMPLIANT**, **below WARNINGS and NON-COMPLIANT**. A file that *was* read but
whose frontmatter does not parse is a different case: Check 1 fails on it (see
above), so it is reported **NON-COMPLIANT**, not NOT ASSESSED — the defect is in
the skill, not in the linter's access to it.

**And state the denominator.** `All 75 Skills` in the header must be the number
actually examined, not the number that exist: report `[N] of [M] skills checked`
whenever they differ. A summary whose counts silently sum to less than its own
title is the failure this skill is supposed to catch in others.

No file writes in static mode.

---

## Phase 2B: Spec Mode — Behavioral Verifier

### Step 1 — Locate Files

Use the skill or agent file resolved in Phase 1.
Look up the spec path from `studio-tests/catalog.yaml` — use the
`spec:` field on the matching `skills:` or `agents:` entry.

If either is missing:
- Missing skill or agent: the Phase 1 message.
- Missing spec path in catalog: "No spec path set for '[name]' in catalog.yaml."
- Spec file not found at path: "Spec file missing at [path]. Run `$skill-test audit`
  to see coverage gaps."

### Step 2 — Read Both Files

Read the skill — its `SKILL.md` and every file in its `references/` folder — or
the agent file, and the test spec file, completely.

### Step 3 — Evaluate Assertions

**按实际上下文评估。** 读取适用的 `AGENTS.md`、Skill、角色的 `developer_instructions` 及其中要求显式读取的资源。Codex 不执行旧客户端的隐式导入语法；不能假定引用文件已进入子代理上下文。记录规范所在文件和实际读取证据；冲突按当前会话的指令优先级处理。

**For an agent**, evaluate the TOML role definition and the Skills explicitly
required by its developer instructions. Reading those dependencies is a visible
step; no legacy frontmatter preload is implied:

- **Static Assertions** — check each against the agent's TOML and instructions.
  Compare literal values exactly, including the Codex model family in the
  role instructions. Check the resolver and caller when the spec requires
  dynamic selection. A near match fails the assertion.
- **Test Cases** — evaluate each case's expected behavior against the agent's
  written instructions, the same way a skill's are evaluated below. A case
  that names a gate ID (`LP-FEASIBILITY`, `CD-PILLARS`, …) is that gate's
  invocation: the spawning skill has the agent read
  `.agents/docs/director-gates/[gate-id].md` first, so that file's Prompt and
  Verdicts are the agent's instructions for the case — read it too.
- **Redirect and escalation cases** — the agent is asked for work another role
  owns, or meets a conflict it cannot settle. The case is met when the loaded
  `coordination-rules.md` covers the step — rule 2 (no binding decisions
  outside its domain), rule 3 (escalate a conflict to the shared parent) or
  rule 5 (no files outside its directories without delegation) — **and** the
  agent's own file names the owning role in its collaborator, delegation,
  escalation or "must not" lists. Cite both; do not require the agent to
  restate the redirect in its own words. It is a FAIL when the agent's file
  claims that work for itself, or when no loaded file names who owns it.
- **Protocol Compliance** — use the spec's own `## Protocol Compliance` list in
  place of the four skill checks below.

**For a skill**, check each of the spec's **Static Assertions** against the
skill's frontmatter and body (`SKILL.md` and its `references/` files) the same
way; a literal value is an exact
comparison. `$skill-test static` runs only its 7 fixed checks, so a spec's own
static lines — a verdict keyword, a phase, "May I write" before a named file —
are evaluated here or nowhere.

The rest of this step applies to skills and agents alike.

For each **Test Case** in the spec:

1. Read the **Fixture** description (assumed state of project files)
2. Read the **Expected behavior** steps
3. Read each **Assertion** checkbox

A case with no **Fixture** reads its **Input** as the fixture; a case with no
**Assertions** list treats each **Expected behavior** bullet as an assertion —
most agent specs are written this way, and a case verdict is not left undefined
just because it has no separate checklist.

For each assertion, evaluate whether the skill's written instructions, if
followed correctly given the fixture state, would satisfy it. This is a
Codex 对文档的静态推理检查，不是代码执行。

Mark each assertion:
- **PASS** — skill instructions clearly satisfy this assertion
- **PARTIAL** — skill instructions partially address it, but with ambiguity
- **FAIL** — skill instructions would NOT satisfy this assertion given the fixture
- **NOT ASSESSED** — the assertion could not be evaluated at all: it names a
  fixture state the spec never defines, depends on runtime behavior no static
  read can settle, or references a file or section that does not exist (a file
  that is merely silent on the behaviour is FAIL or PARTIAL, not this). Rank it
  **above PASS** (an assertion nobody could evaluate has not been satisfied) and
  **below PARTIAL and FAIL** (an ambiguity somebody identified is more actionable
  than one nobody could reach). Do not resolve an unevaluable assertion to PASS
  because the skill "probably" handles it — that judgement is what the spec exists
  to replace.

For a skill's **Protocol Compliance** section (always present), evaluate each line
of the spec's own list against the skill's files exactly as you evaluate a case
assertion — PASS, PARTIAL, FAIL or NOT ASSESSED. Specs put rules there that no
case repeats ("covered by the protocol compliance assertions above"), so a
list that is not evaluated is a set of rules nobody checks. These four checks are
the floor, added when the list does not already cover them:
- 检查写入是否遵守当前协作模式及会话已有授权
- Check whether the skill presents findings before requesting approval
- Check whether the skill ends with a recommended next step
- 检查必要问题没有被跳过；已批准的范围不重复索取确认

### Step 4 — Build Report

```
=== Skill Spec Test: /[name] ===
Date: [date]
Spec: studio-tests/skills/[category]/[name].md

Static Assertions:
  [PASS] [assertion text]
  [NOT ASSESSED] [assertion text]
     Reason: [why it could not be evaluated]

Case 1: [Happy Path — name]
  Fixture: [summary]
  Assertions:
    [PASS] [assertion text]
    [FAIL] [assertion text]
       Reason: The skill's Phase 3 says "..." but the fixture state means "..."
  Case Verdict: FAIL

Case 2: [Edge Case — name]
  ...
  Case Verdict: PASS

Protocol Compliance:
  [PASS] 写入遵循当前模式及已有授权
  [PASS] Presents findings before asking approval
  [PARTIAL] No explicit next-step handoff at end

Overall Verdict: FAIL (1 case failed, 1 protocol line partial)
```

A Case Verdict is the worst result among its assertions, and the Overall
Verdict the worst across the static assertions, the cases and Protocol
Compliance, in this order:
FAIL, PARTIAL, NOT ASSESSED, PASS. An assertion nobody could evaluate keeps the
overall result from reading PASS.

For an agent, the header is `=== Agent Spec Test: [name] ===`, `Spec:` is its
path under `studio-tests/agents/`, and a `Static Assertions:`
block comes before Case 1.

### Step 5 — Offer to Write Results

"May I write these results to `studio-tests/results/skill-test-spec-[name]-[date].md`
and update `studio-tests/catalog.yaml`?"

If yes:
- Write results file to `studio-tests/results/`
- Update the skill's or agent's entry in `studio-tests/catalog.yaml`:
  - `last_spec: [date]`
  - `last_spec_result: PASS|PARTIAL|FAIL|NOT ASSESSED` — the Overall Verdict

---

## Phase 2D: Category Mode — Rubric Evaluation

### Step 1 — Locate Skill and Category

Use the skill or agent file resolved in Phase 1.
Look up the `category:` field on its `skills:` or `agents:` entry in
`studio-tests/catalog.yaml`.

If neither file exists: the Phase 1 message.
If no `category:` field: "No category assigned for '[name]' in catalog.yaml.
Add `category: [name]` to its entry first."

For `category all`: collect every skill and every agent with a `category:` field
and process each, reporting skills and agents in separate tables.
`category: utility` skills are evaluated against U1 (static checks pass) and U2
(gate mode correct if applicable) only — skip to the static mode for U1.
Cross-check against `.agents/skills/*/SKILL.md` and `.codex/agents/*.toml`
(Audit mode's Step 2 glob): list any skill or agent missing from the catalog, or
catalogued with no `category:`, by name as **NOT ASSESSED** — never silently
excluded from the run.

### Step 2 — Read Rubric Section

Read `studio-tests/quality-rubric.md`.
Extract the section matching the category (e.g., `### gate`, `### team`; an
agent's category is under `## Agent Categories`, e.g. `### director`).
If the rubric has no section for the category, the result is **NOT ASSESSED**:
name the missing section, and never borrow another category's metrics.

### Step 3 — Read Skill

Read the skill's `SKILL.md` and every file in its `references/` folder, or the
agent's `.codex/agents/[name].toml`, fully,
and the project context Phase 2B Step 3 describes — a metric met by a rule in
`AGENTS.md` or an explicitly read resource is met, citing that file. Its rule for
redirect and escalation cases decides the domain, deferral and escalation
metrics too (D2, D3, L2, S1–S3, O2).

### Step 4 — Evaluate Rubric Metrics

For each metric in the category's rubric table:
1. Check whether the skill's or agent's written instructions clearly satisfy the criterion
2. Mark PASS, FAIL, WARN, or NOT ASSESSED (the metric could not be evaluated — name why)
3. For FAIL/WARN/NOT ASSESSED, identify the exact gap in the text (quote the
   relevant section, note its absence, or name what could not be evaluated)

### Step 5 — Output Report

For an agent, the header is `=== Agent Category Check: [name] ([category]) ===`.

```
=== Skill Category Check: /[name] ([category]) ===

Metric G1 — Review mode read:      PASS
Metric G2 — Director panel width:  FAIL
  Gap: Phase 3 spawns only CD-PHASE-GATE at `workflow: full`; TD-PHASE-GATE, PR-PHASE-GATE, AD-PHASE-GATE absent
Metric G3 — Lean mode: PHASE-GATE only: PASS
Metric G4 — Solo mode: no directors:    PASS
Metric G5 — No auto-advance:       PASS

Verdict: FAIL (1 failure, 0 warnings)
Fix: Size the Phase 3 panel from `modes.workflow` — PR at `minimal`, TD + PR at
     `standard`, all four at `full` — and name any perspective a narrower panel leaves out.
```

The category verdict, first match wins: **FAIL** when any metric fails; else
**WARNINGS** when any metric warns; else **NOT ASSESSED** when any metric could
not be evaluated (a rubric section missing, a file unreadable); else **PASS**
when every metric passes — the same ranking as static and spec mode. It is
`last_category_result` in the catalog.

### Step 6 — Offer to Update Catalog

"May I update `studio-tests/catalog.yaml` to record this category check
(`last_category`, `last_category_result`) for [name]?"

---

## Phase 2C: Audit Mode — Coverage Report

### Step 1 — Read Catalog

Read `studio-tests/catalog.yaml`. If missing, note that catalog doesn't exist
yet (first-run state).

### Step 2 — Enumerate All Skills and Agents

Glob `.agents/skills/*/SKILL.md` to get the complete list of skills.
Extract skill name from each path (directory name).

Glob `.codex/agents/*.toml` for the complete list of agents — the repo itself,
not the catalog, is the covered set (`.agents/rules/skill-authoring.md` §5:
gates derive their covered set, they do not enumerate it). Compare both globs
against the catalog's `skills:`/`agents:` entries and report any skill or agent
missing from the catalog by name, so an uncatalogued one cannot drop out silently.
Skip the old-name aliases (`changelog`, `help`, `settings`, each described as
"Old name of …"): they are not in the catalog and are not gaps.

### Step 3 — Build Skill Coverage Table

For each skill:
- Check if a spec file exists (use the `spec:` path from catalog, or glob `studio-tests/skills/*/[name].md`)
- Look up `last_static`, `last_static_result`, `last_spec`, `last_spec_result`,
  `last_category`, `last_category_result`, `category` from catalog (or mark as
  "never" / "—" if not in catalog)
- Priority comes from catalog `priority:` field (critical/high/medium/low)

### Step 3b — Build Agent Coverage Table

For each agent in catalog's `agents:` section:
- Check if a spec file exists (use the `spec:` path from catalog, or glob `studio-tests/agents/*/[name].md`)
- Look up `last_spec`, `last_spec_result`, `last_category`,
  `last_category_result`, `category` from catalog

### Step 4 — Output Report

```
=== Skill Test Coverage Audit ===
Date: [date]

SKILLS (75 total)
Specs written: 75 (100%) | Never static tested: 75 | Never category tested: 75

Skill                  | Cat      | Has Spec | Last Static | S.Result | Last Cat | C.Result | Priority
-----------------------|----------|----------|-------------|----------|----------|----------|----------
gate-check             | gate     | YES      | never       | —        | never    | —        | critical
design-review          | review   | YES      | never       | —        | never    | —        | critical
...

AGENTS (49 total)
Agent specs written: 49 (100%)

Agent                  | Category   | Has Spec | Last Spec   | Result | Last Cat | C.Result
-----------------------|------------|----------|-------------|--------|----------|----------
creative-director      | director   | YES      | never       | —      | never    | —
technical-director     | director   | YES      | never       | —      | never    | —
...

Top 5 Priority Gaps (skills with no spec, critical/high priority):
(none if all specs are written)

Skill coverage:  75/75 specs (100%)
Agent coverage:  49/49 specs (100%)
```

No file writes in audit mode.

Offer: "Would you like to run `$skill-test static all` to check structural
compliance across all skills? `$skill-test category all` to run category rubric
checks? Or `$skill-test spec [name]` to run a specific behavioral test?"

---

## Phase 3: Recommended Next Steps

After any mode completes, offer contextual follow-up:

- After `static [name]`: "Run `$skill-test spec [name]` to validate behavioral
  correctness if a test spec exists."
- After `static all` with failures: "Address NON-COMPLIANT skills first. Run
  `$skill-test static [name]` individually for detailed remediation guidance."
- After `spec [name]` PASS: "Update `studio-tests/catalog.yaml` to record this
  pass date. Consider running `$skill-test audit` to find the next spec gap."
- After `spec [name]` FAIL: "Review the failing assertions and update the skill
  or agent, or the test spec, to resolve the mismatch."
- After `audit`: "Start with the critical-priority gaps. Use the spec template
  at `studio-tests/templates/skill-test-spec.md` (agents:
  `agent-test-spec.md`) to create new specs."
