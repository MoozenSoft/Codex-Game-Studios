# CLI 新 clone 冷启动验收

日期：2026-11-17。范围仅为当前独立 clone 的 CLI 启动与项目资源可用性。结果：部分检查通过；配置 helper 与原生角色绑定未验证成功，不能宣称完整启动验收通过。

## 边界与 Git

实际 cwd 与 `git rev-parse --show-toplevel` 均为 `<probe>/app-web-acceptance`。
分支：`app-acceptance`；HEAD：`cc1076080a16154af378fa5082a089b69169837e`；HEAD tree：`2eed3d73899155cd7a4aba4410143c57d32248f6`。
`.git` 是当前目录内的目录；absolute git dir 为当前根下 `.git`，common dir 为 `.git`，确认独立 Git 根。用户未提供预期分支或 tree 字面值，故仅核对实际身份和前后一致性。初始 `git status --porcelain` 输出为空。

实际命令（以下各命令批次退出码均为 0，另有标注除外）：

```powershell
Get-Location; git rev-parse --show-toplevel; git branch --show-current; git rev-parse HEAD; git rev-parse 'HEAD^{tree}'; git status --porcelain
Get-Content -LiteralPath .agents/skills/project-settings/SKILL.md
Get-Content -Encoding UTF8 -LiteralPath .agents/skills/project-settings/SKILL.md,.agents/docs/codex-runtime.md,.agents/docs/automation-modes.md
```

首次 Get-Content 使用终端默认编码，中文显示乱码；随后 UTF8 重读成功。Skill 加载来源仅为 `.agents/skills/project-settings/SKILL.md`，并读取其要求的两个本项目运行文档。未读取用户全局 Skills、插件、MCP、角色、私有客户端会话或旧客户端配置。

## automation

当前 `project.local.yaml` 缺失，`project.yaml` 存在且没有有效的 `modes:` 配置。按本项目 Skill 明确规定的优先级与默认值，静态判定 `modes.automation=collaborative`，来源为 default；不是旧游戏上下文或父目录配置。本地覆盖：无。helper 实际解析未成功，不能把静态判定记为 helper 成功输出。

实际逐条执行的命令如下，每条退出码均为 **1**：

```powershell
bash ".agents/skills/project-settings/../../scripts/yaml-helper.sh" resolve_setting modes.automation
bash ".agents/skills/project-settings/../../scripts/yaml-helper.sh" get_yaml_key project.yaml modes.automation
bash ".agents/skills/project-settings/../../scripts/yaml-helper.sh" is_locally_overridable modes.automation
bash ".agents/skills/project-settings/../../scripts/yaml-helper.sh" resolve_setting modes.automation_always_ask
```

四次真实错误均为（原始输出含 NUL，此处转录可读文本）：

```text
Access is denied.
Error code: Bash/E_ACCESSDENIED
```

没有安装、提权、修改 shell/账号配置或绕过限制。automation_always_ask 的运行时解析同样未评估。

后续只读核验命令，退出码 0：

```powershell
git rev-parse --absolute-git-dir; git rev-parse --git-common-dir; Get-Item -Force -LiteralPath .git | Select-Object FullName,PSIsContainer; Select-String -LiteralPath .agents/docs/effects-map.md -Pattern '^> ### RESERVED' -Context 14,0
Get-Content -Encoding UTF8 -LiteralPath project.yaml; Test-Path -LiteralPath production/qa/evidence; Test-Path -LiteralPath production/qa/evidence/cli-cold-startup.md; git status --porcelain
```

RESERVED 标题匹配无输出；报告及其 evidence 目录写入前均不存在，工作区仍为空。

## 原生 qa-tester 委派

请求任务：给定“1 个必要测试失败，其他 9 个通过”，由本项目原生 `agent_type=qa-tester` 判断故事是否可以关闭及原因，只读，保持 Sol。

实际能力阻塞：本轮提供的 `collaboration.spawn_agent` schema 仅有 `task_name`、`message`、`fork_turns`、`model`、`reasoning_effort`，没有 `agent_type` 参数，也没有另一原生角色绑定接口。因而未能发出符合要求的绑定调用；没有进程退出码，没有服务端绑定错误，也没有子代理返回或可等待的 agent ID。此为接口能力缺失，不伪造一次调用失败。

未读取 `.codex/agents/qa-tester.toml` 内容，未用普通代理附带角色文本冒充原生绑定，未改变模型。原生角色验收项为未评估/阻塞。没有把父代理判断写成 qa-tester 输出。

## 本项目资源存在性

实际检查命令，退出码 0：

```powershell
$skills = @(Get-ChildItem -LiteralPath .agents/skills -Directory | Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md') }); $roles = @(Get-ChildItem -LiteralPath .codex/agents -File -Filter *.toml); 'skills_count=' + $skills.Count; $skills | ForEach-Object { '.agents/skills/' + $_.Name + '/SKILL.md' }; 'roles_count=' + $roles.Count; $roles | ForEach-Object { '.codex/agents/' + $_.Name }; '.claude=' + (Test-Path -LiteralPath .claude); 'CLAUDE.md=' + (Test-Path -LiteralPath CLAUDE.md); 'project.local.yaml=' + (Test-Path -LiteralPath project.local.yaml); 'project.yaml=' + (Test-Path -LiteralPath project.yaml)
```

结果：75 个含 SKILL.md 的正式 Skill 目录；49 个角色 TOML。仅证明资源存在，不证明每个 Skill 或角色已执行。
相对路径 `.claude`、`CLAUDE.md`、`project.local.yaml` 均缺失；`project.yaml` 存在。

资源相对路径清单：

```text
.agents/skills/adopt/SKILL.md
.agents/skills/architecture-decision/SKILL.md
.agents/skills/architecture-review/SKILL.md
.agents/skills/art-bible/SKILL.md
.agents/skills/asset-audit/SKILL.md
.agents/skills/asset-spec/SKILL.md
.agents/skills/balance-check/SKILL.md
.agents/skills/brainstorm/SKILL.md
.agents/skills/bug-report/SKILL.md
.agents/skills/bug-triage/SKILL.md
.agents/skills/code-review/SKILL.md
.agents/skills/consistency-check/SKILL.md
.agents/skills/content-audit/SKILL.md
.agents/skills/create-architecture/SKILL.md
.agents/skills/create-control-manifest/SKILL.md
.agents/skills/create-epics/SKILL.md
.agents/skills/create-stories/SKILL.md
.agents/skills/cut/SKILL.md
.agents/skills/day-one-patch/SKILL.md
.agents/skills/design-review/SKILL.md
.agents/skills/design-system/SKILL.md
.agents/skills/dev-story/SKILL.md
.agents/skills/estimate/SKILL.md
.agents/skills/gate-check/SKILL.md
.agents/skills/hotfix/SKILL.md
.agents/skills/launch-checklist/SKILL.md
.agents/skills/localize/SKILL.md
.agents/skills/map-systems/SKILL.md
.agents/skills/milestone-review/SKILL.md
.agents/skills/next-step/SKILL.md
.agents/skills/onboard/SKILL.md
.agents/skills/patch-notes/SKILL.md
.agents/skills/perf-profile/SKILL.md
.agents/skills/playtest-report/SKILL.md
.agents/skills/project-settings/SKILL.md
.agents/skills/project-stage-detect/SKILL.md
.agents/skills/propagate-design-change/SKILL.md
.agents/skills/prototype/SKILL.md
.agents/skills/qa-plan/SKILL.md
.agents/skills/quick-design/SKILL.md
.agents/skills/regression-suite/SKILL.md
.agents/skills/release-checklist/SKILL.md
.agents/skills/retrospective/SKILL.md
.agents/skills/reverse-document/SKILL.md
.agents/skills/review-all-gdds/SKILL.md
.agents/skills/scope-check/SKILL.md
.agents/skills/security-audit/SKILL.md
.agents/skills/setup-engine/SKILL.md
.agents/skills/skill-improve/SKILL.md
.agents/skills/skill-test/SKILL.md
.agents/skills/smoke-check/SKILL.md
.agents/skills/soak-test/SKILL.md
.agents/skills/sprint-plan/SKILL.md
.agents/skills/sprint-status/SKILL.md
.agents/skills/start/SKILL.md
.agents/skills/story-done/SKILL.md
.agents/skills/story-readiness/SKILL.md
.agents/skills/team-audio/SKILL.md
.agents/skills/team-combat/SKILL.md
.agents/skills/team-level/SKILL.md
.agents/skills/team-live-ops/SKILL.md
.agents/skills/team-narrative/SKILL.md
.agents/skills/team-polish/SKILL.md
.agents/skills/team-qa/SKILL.md
.agents/skills/team-release/SKILL.md
.agents/skills/team-ui/SKILL.md
.agents/skills/tech-debt/SKILL.md
.agents/skills/test-evidence-review/SKILL.md
.agents/skills/test-flakiness/SKILL.md
.agents/skills/test-helpers/SKILL.md
.agents/skills/test-setup/SKILL.md
.agents/skills/ux-design/SKILL.md
.agents/skills/ux-review/SKILL.md
.agents/skills/vertical-slice/SKILL.md
.agents/skills/write-changelog/SKILL.md
.codex/agents/accessibility-specialist.toml
.codex/agents/ai-programmer.toml
.codex/agents/analytics-engineer.toml
.codex/agents/art-director.toml
.codex/agents/audio-director.toml
.codex/agents/community-manager.toml
.codex/agents/creative-director.toml
.codex/agents/devops-engineer.toml
.codex/agents/economy-designer.toml
.codex/agents/engine-programmer.toml
.codex/agents/game-designer.toml
.codex/agents/gameplay-programmer.toml
.codex/agents/godot-csharp-specialist.toml
.codex/agents/godot-gdextension-specialist.toml
.codex/agents/godot-gdscript-specialist.toml
.codex/agents/godot-shader-specialist.toml
.codex/agents/godot-specialist.toml
.codex/agents/lead-programmer.toml
.codex/agents/level-designer.toml
.codex/agents/live-ops-designer.toml
.codex/agents/localization-lead.toml
.codex/agents/narrative-director.toml
.codex/agents/network-programmer.toml
.codex/agents/performance-analyst.toml
.codex/agents/producer.toml
.codex/agents/prototyper.toml
.codex/agents/qa-lead.toml
.codex/agents/qa-tester.toml
.codex/agents/release-manager.toml
.codex/agents/security-engineer.toml
.codex/agents/sound-designer.toml
.codex/agents/systems-designer.toml
.codex/agents/technical-artist.toml
.codex/agents/technical-director.toml
.codex/agents/tools-programmer.toml
.codex/agents/ue-blueprint-specialist.toml
.codex/agents/ue-gas-specialist.toml
.codex/agents/ue-replication-specialist.toml
.codex/agents/ue-umg-specialist.toml
.codex/agents/ui-programmer.toml
.codex/agents/unity-addressables-specialist.toml
.codex/agents/unity-dots-specialist.toml
.codex/agents/unity-shader-specialist.toml
.codex/agents/unity-specialist.toml
.codex/agents/unity-ui-specialist.toml
.codex/agents/unreal-specialist.toml
.codex/agents/ux-designer.toml
.codex/agents/world-builder.toml
.codex/agents/writer.toml
```

## 未评估项与写入约束

hooks 的信任与触发没有本轮实际事件证据，明确未评估；未手工调用 hooks 绕过信任。App 运行、整个 Web 流程、游戏运行、全部框架验证及其他工作流均未评估。没有联网发布、安装、提交、改变分支/index/HEAD、修改框架/配置/游戏/账号设置。
唯一新增文件为本报告 `production/qa/evidence/cli-cold-startup.md`（仅为容纳报告创建父目录）。未生成 session-state 或其他日志。

写入方式：PowerShell 在内存构造本报告与当前目录枚举清单，`New-Item -ItemType Directory -Force -Path production/qa/evidence`，随后 `Set-Content -Encoding UTF8 -LiteralPath production/qa/evidence/cli-cold-startup.md -Value $report`。
最终只读复核命令：`git branch --show-current; git rev-parse HEAD; git rev-parse 'HEAD^{tree}'; git status --porcelain --untracked-files=all`；实际结果在交付时核对。
`n最终复核及报告写入命令批次退出码：0。分支、HEAD、HEAD tree 与初始值完全一致；status 唯一输出为 `?? production/qa/evidence/cli-cold-startup.md`。
