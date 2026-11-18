# Agent Test Spec: [agent-name]

> Codex 验收约定：本文件保留领域用例；配置来源为 `.agents/skills/` 与 `.codex/agents/`。提问、确认、写入及并发按实际客户端能力和 `automation-modes.md` 执行，复用已有授权；静态推理不等于真实运行通过。

## Agent Summary

[One paragraph describing this agent's domain, what decisions it owns, and what it
delegates vs. handles directly. Include which gates it triggers (if any).]

**Domain**: [files/directories this agent owns]
**Escalates to**: [parent agent — e.g., creative-director for design conflicts]
**Delegates to**: [sub-agents this agent typically spawns]

---

## Static Assertions (Structural)

- [ ] Agent file exists at `.codex/agents/[name].toml`
- [ ] Native TOML has `name`, `description`, `developer_instructions` fields
- [ ] The role declares the correct model family when required. The caller resolves it and passes the model at dispatch. `model_reasoning_effort` follows client settings unless explicitly configured. Tool access follows actual capabilities and permissions (see `.agents/docs/model-tiers.md`)
- [ ] Domain clearly stated
- [ ] Escalation path documented
- [ ] Does not make decisions outside its domain

---

## Test Cases

### Case 1: In-Domain Request — [brief name]

**Scenario**: A request that is clearly within this agent's domain.

**Fixture**:
- [relevant project state]
- [input provided to agent]

**Expected behavior**:
1. Agent accepts the request
2. Agent produces [specific output type]
3. Agent applies the configured automation mode and reuses existing authorization for file writes

**Assertions**:
- [ ] Agent handles request within its domain without escalating
- [ ] Output format matches expected structure
- [ ] Configured automation mode followed; necessary unresolved decisions are asked, and existing authorization is reused

**Case Verdict**: PASS / FAIL / PARTIAL / NOT ASSESSED

---

### Case 2: Out-of-Domain Redirect — [brief name]

**Scenario**: A request that falls outside this agent's domain.

**Fixture**:
- [request that belongs to a different agent]

**Expected behavior**:
1. Agent identifies the request is out of domain
2. Agent redirects to the correct agent
3. Agent does NOT attempt to handle it

**Assertions**:
- [ ] Agent declines and redirects (does not silently handle cross-domain work)
- [ ] Correct agent named in redirect

**Case Verdict**: PASS / FAIL / PARTIAL / NOT ASSESSED

---

### Case 3: Gate Verdict — [brief name]

**Scenario**: Agent is invoked as part of a director gate check.

**Fixture**:
- [project state presented for review]
- [gate ID: e.g., CD-PHASE-GATE]

**Expected behavior**:
1. Agent reads the gate's definition file, then the documents it names
2. Agent opens with `[GATE-ID]: [word]`, the word taken from that gate's **Verdicts** line
3. Agent returns the verdict to the calling skill and does not act on it itself

**Assertions**:
- [ ] First line is `[GATE-ID]: [word]` with a word from the invoked gate's Verdicts line — or `NOT ASSESSED`, naming the input, when an input the gate names was not given
- [ ] Reasoning provided for verdict
- [ ] Agent does not carry on with the reviewed work past its own verdict — the calling skill, not the agent, blocks on the gate's failure word (CONCERNS is not blocking; the skill takes it to the user)

**Case Verdict**: PASS / FAIL / PARTIAL / NOT ASSESSED

---

### Case 4: Conflict Escalation — [brief name]

**Scenario**: This agent's domain conflicts with another agent's decision.

**Fixture**:
- [conflicting decisions from two agents at same tier]

**Expected behavior**:
1. Agent identifies the conflict
2. Agent escalates to the shared parent (or creative-director / technical-director)
3. Agent does NOT unilaterally resolve cross-domain conflicts

**Assertions**:
- [ ] Conflict surfaced explicitly
- [ ] Correct escalation path followed
- [ ] No unilateral cross-domain changes made

**Case Verdict**: PASS / FAIL / PARTIAL / NOT ASSESSED

---

### Case 5: Context Pass-Through — [brief name]

**Scenario**: Agent receives a task with full context from a parent agent.

**Fixture**:
- [context block passed from parent]
- [specific sub-task to execute]

**Expected behavior**:
1. Agent reads and uses the provided context
2. Agent completes the sub-task
3. Agent returns result to parent (does not prompt user unnecessarily)

**Assertions**:
- [ ] Agent uses provided context rather than re-asking for it
- [ ] Result is scoped to the sub-task, not expanded beyond it
- [ ] Output format suitable for parent agent consumption

**Case Verdict**: PASS / FAIL / PARTIAL / NOT ASSESSED

---

## Protocol Compliance

- [ ] Stays within declared domain — no unilateral cross-domain changes
- [ ] Escalates conflicts to correct parent
- [ ] Applies the configured automation mode and existing authorization before file writes (or is read-only)
- [ ] Presents findings before requesting approval
- [ ] Does not skip tiers in the delegation hierarchy

---

## Coverage Notes

[Any gaps in coverage, known edge cases not tested, or behaviors that require
a live agent invocation to verify.]
