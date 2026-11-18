# English Codex Role Adaptation Audit

Full role text is maintained only in `.codex/agents/`. Each client-specific edit has source offsets, original/replacement text, count and reason in `adaptations.json`. Tests reverse those edits and check the complete original body hash; duplicate Markdown snapshots are unnecessary.

| Role | Explicit replacements | Body reconstruction |
| --- | ---: | --- |
| accessibility-specialist | 8 | MATCH |
| ai-programmer | 11 | MATCH |
| analytics-engineer | 7 | MATCH |
| art-director | 12 | MATCH |
| audio-director | 12 | MATCH |
| community-manager | 10 | MATCH |
| creative-director | 8 | MATCH |
| devops-engineer | 15 | MATCH |
| economy-designer | 12 | MATCH |
| engine-programmer | 11 | MATCH |
| game-designer | 12 | MATCH |
| gameplay-programmer | 13 | MATCH |
| godot-csharp-specialist | 13 | MATCH |
| godot-gdextension-specialist | 13 | MATCH |
| godot-gdscript-specialist | 14 | MATCH |
| godot-shader-specialist | 13 | MATCH |
| godot-specialist | 22 | MATCH |
| lead-programmer | 11 | MATCH |
| level-designer | 13 | MATCH |
| live-ops-designer | 9 | MATCH |
| localization-lead | 8 | MATCH |
| narrative-director | 12 | MATCH |
| network-programmer | 11 | MATCH |
| performance-analyst | 8 | MATCH |
| producer | 8 | MATCH |
| prototyper | 18 | MATCH |
| qa-lead | 16 | MATCH |
| qa-tester | 19 | MATCH |
| release-manager | 10 | MATCH |
| security-engineer | 14 | MATCH |
| sound-designer | 7 | MATCH |
| systems-designer | 12 | MATCH |
| technical-artist | 11 | MATCH |
| technical-director | 8 | MATCH |
| tools-programmer | 11 | MATCH |
| ue-blueprint-specialist | 11 | MATCH |
| ue-gas-specialist | 11 | MATCH |
| ue-replication-specialist | 11 | MATCH |
| ue-umg-specialist | 11 | MATCH |
| ui-programmer | 12 | MATCH |
| unity-addressables-specialist | 11 | MATCH |
| unity-dots-specialist | 11 | MATCH |
| unity-shader-specialist | 11 | MATCH |
| unity-specialist | 17 | MATCH |
| unity-ui-specialist | 11 | MATCH |
| unreal-specialist | 17 | MATCH |
| ux-designer | 10 | MATCH |
| world-builder | 12 | MATCH |
| writer | 11 | MATCH |

An independent read-only review found two Important issues: skill-name conversion damaged resource paths, and some workflow steps still demanded unconditional confirmation. It also found an ambiguous strategic-write phrase. The fixes use bounded command matching and conditional authorization; targeted regressions were observed failing before the fixes and passing afterward.

Duplicate source snapshots have been removed. The active role directory no longer contains legacy paths, old input/delegation tool assumptions, automatic worktree claims or the old default-engine assumption.

These are content, schema and contract checks, not proof that all 49 roles have run under every client.
