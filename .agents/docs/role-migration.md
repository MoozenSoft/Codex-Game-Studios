# English Codex Role Adaptation

Active roles live in `.codex/agents/*.toml`. Their multiline developer_instructions contain English Codex guidance followed by the full role workflow with explicit client-specific edits. Historical execution instructions are not injected wholesale behind a reference marker.

## Source preservation

The source is the user's D:/Git/Claude-Code-Game-Studios/.claude/agents directory. The repository retains source hashes and the necessary adaptation deltas, without keeping a second complete Markdown copy of each role. Tests do not read that external directory.

`original-content.json` records original file provenance and normalized body hashes. `adaptations.json` records each replacement, count, reason and Unicode code point offsets before that forward edit. Tests start with the active body and undo edits in reverse order, processing the last position first. Each replacement is checked at its recorded position, so identical text that already existed elsewhere remains untouched. The recovered body's complete hash and line count must match the source record; unrecorded omissions or rewrites fail. The raw-file hash is provenance, not a claim to revalidate unavailable raw bytes.

## Active Codex behavior

- Use current `.agents/` resources, `.codex/agents/<role>.toml`, directory-appropriate AGENTS.md and actual `$skill-name` entries.
- Inspect the actual delegation schema and available depth/concurrency. Bind a canonical role when supported; otherwise explicitly load its TOML instructions into an approved bounded task. Report unavailable delegation or missing specialist input, never invented participation.
- Route user-reserved decisions through the parent and its available input tools. Do not infer tool access from historical grants or assume a fixed batch size.
- Resolve the collaboration mode and reuse existing approval for the same change set. Ask only for still-required decisions. A path alone grants no authority; new-file and skeleton confirmation follow the selected mode.
- Resolve the role's declared model family through `model-tiers.md` before delegation and pass the resulting model to the available tool. Reasoning effort and permissions follow the client.
- Isolation must actually exist or be arranged by the parent. Report checkout/branch, explicitly identify source checkout, check uncommitted/ignored inputs and LFS assets, and obtain external access only when authorized. Listing order does not identify the user's working directory.
- Resolve actual engine, pinned version, branching and CI policy. Source-template defaults and policy examples are not current project facts.
- Required tests/checks must pass before completion; unknown results remain unassessed. Preserve task scope, evidence and honest independent-review attribution.

## Metadata boundaries

Name and description remain native TOML fields. Explicit upstream model tiers become family requirements in the role instructions. The caller supplies the resolved version at dispatch. The [model routing fixture](../../studio-tests/fixtures/model-routing.json) records the upstream model declarations, revision and hashes. Historical tools/disallowedTools, maxTurns, memory, isolation and skills declarations remain provenance data rather than unsupported native fields. Declared skills become explicit local reads and project memory becomes an explicit note path; neither implies automatic loading or stronger permissions.

The compatibility inspector scans the entire active role body. Active roles do not use upstream-reference markers to reclassify old execution instructions. Reference classification in other inputs does not enforce instruction isolation.

These content, TOML and contract checks are static/script evidence. They do not establish that all 49 roles ran in every client or that all historical mechanisms have native equivalents. Per-role changes are recorded in `studio-tests/results/role-content-audit.md`.
