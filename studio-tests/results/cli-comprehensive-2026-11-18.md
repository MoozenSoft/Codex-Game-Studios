# Codex CLI 全面验证记录

日期：2026-11-18。客户端：Windows Codex CLI `0.169.0`。对象为本轮开始时的当前工作树，HEAD 为 `458b4a0`，包含当时已有的暂存改动；不是只测试该提交的干净 tree。未传模型或推理强度覆盖。实际 turn_context 显示前段 `gpt-6.1-sol / high`，QA 续作及后段 `gpt-6.2-sol / xhigh`；按各 trace 记录，不能用一次配置快照代表全部回合。原生 qa-lead 继承测试的父子均为 `gpt-6.1-sol / high`。

**结论：CONCERNS。已执行的自动化及真实 CLI 场景均达到预期，未发现这些场景中的功能性失败；仍不能签署“所有能力全面通过”。** 75 个 Skills、49 个角色的结构检查已经覆盖；逐个完整工作流与逐个角色的实际执行没有全覆盖。交互 TUI 也受到系统限制，具体边界列在下方。

## 全量自动化与结构覆盖

| 范围 | 本轮结果 | 证据 |
| --- | --- | --- |
| 框架测试 | 105/105，无跳过 | [完整输出](runtime-evidence/cli-comprehensive-2026-11-18/unittest.txt) |
| 框架真实 Chrome 回归 | 3/3，无跳过：带/不带原生 hook 的导入绘制、grow 经典脚本绑定 | [浏览器输出](runtime-evidence/cli-comprehensive-2026-11-18/browser-tests.txt) |
| 既有 Web 游戏回归 | 18/18：6 个 Vitest、12 个 Playwright，TypeScript 与单文件构建通过 | [游戏测试输出](runtime-evidence/cli-comprehensive-2026-11-18/game-tests.txt) |
| 框架与 complete 校验 | 退出 0；743 项来源中 active=733、retired=10、pending=0，native_components=20 | [complete 结果](runtime-evidence/cli-comprehensive-2026-11-18/framework-complete.json) |
| Skills 与配置 | 75 个 Skills、206 个 Skill 资源；17 份 YAML、50 份 TOML | [YAML 结果](runtime-evidence/cli-comprehensive-2026-11-18/yaml.json)、[框架结果](runtime-evidence/cli-comprehensive-2026-11-18/framework-all.json) |
| Bash 语法 | 51/51 | [检查明细](runtime-evidence/cli-comprehensive-2026-11-18/local-checks.json) |
| 角色源与模型继承合同 | 49/49 TOML 可解析、均省略模型与推理覆盖；全量测试包括来源哈希、英文定点适配与共享合同回归 | [逐角色清单](runtime-evidence/cli-comprehensive-2026-11-18/role-inventory.json) |
| CLI Skill 发现 | 75/75 来自本 checkout、enabled，无缺失；另有专用口令探测 Skill | [真实发现结果](runtime-evidence/cli-comprehensive-2026-11-18/skills-discovery.json) |
| 兼容观察 | 255 个 Skill/角色文件扫描，FOUND_LINES=0；这是静态扫描，不是行为裁决 | [观察输出](runtime-evidence/cli-comprehensive-2026-11-18/compat-observations.txt) |
| CLI 配置与认证 | 正常登录；实际支持的严格启动配置检查退出 0 | [启动检查](runtime-evidence/cli-comprehensive-2026-11-18/strict-config-startup.txt) |

[逐项覆盖表](runtime-evidence/cli-comprehensive-2026-11-18/coverage.json)列出全部 75 个 Skills 和 49 个角色的路径、资源哈希、规格是否存在、类别及本轮实际执行范围，同时列出 105 个框架测试和 3 个浏览器测试的名称。历史类别代表证据单列，不替代本轮逐组件运行。

## 真实 CLI 场景

9 次 `codex exec` / `exec resume` 全部退出 0，涉及 6 个父线程及同一原生子代理的两回合。所有操作使用正常审批与已有 hooks 信任，没有使用信任或 sandbox 绕过参数。

| 检查 | 实际结果与直接证据 |
| --- | --- |
| 启动恢复、Skill 调用与配置 | 启动上下文返回随机标记；未读取检查点取得它。显式加载本地口令 Skill。真实执行 Git 与配置 helper，记录当前根和设置来源。[首回合](runtime-evidence/cli-comprehensive-2026-11-18/baseline.md) |
| 原生工具放行 | 终端输出专用验收标记，退出 0。[原生 trace](runtime-evidence/cli-comprehensive-2026-11-18/baseline.trace.json) |
| JSON 写后告警与修复 | 原生 apply_patch 写坏 JSON，真实 PostToolUse 发出告警；修复后解析落盘文件成功。没有声称告警撤销了已发生写入。[原生 trace](runtime-evidence/cli-comprehensive-2026-11-18/baseline.trace.json) |
| `.env` 写前拒绝 | 原生 apply_patch 的非秘密 fixture 被 PreToolUse 拒绝；父控制器独立确认目标未落盘。[父核对](runtime-evidence/cli-comprehensive-2026-11-18/parent-checks.json) |
| 当前暂存区拒绝 | 仅在隔离索引暂存坏 JSON，原生 `git commit --dry-run` 被真实 hook 阻断；随后逐字节恢复索引。[拒绝回执](runtime-evidence/cli-comprehensive-2026-11-18/boundaries.trace.json) |
| 跨仓库提交上下文拒绝 | 原生工具显式 workdir 指向独立 fixture 仓库，`git commit --dry-run` 被以“实际目标不属于当前项目”拒绝；没有真实提交。[原生 trace](runtime-evidence/cli-comprehensive-2026-11-18/boundaries.trace.json) |
| 异步问答等待 | qa-plan 实际提交两个独立问题，仅 accepted 时保持 WAITING；父控制器确认计划不存在、故事未改。[问题及回执](runtime-evidence/cli-comprehensive-2026-11-18/question-proof.json) |
| 明确选择后的续作 | 控制器在同一线程提供 `write_qa_plan=yes / backfill_stories=no`；实际保存完整计划，未重复提问，故事 SHA-256 不变。[生成计划](runtime-evidence/cli-comprehensive-2026-11-18/qa-plan-generated.md)、[续作结果](runtime-evidence/cli-comprehensive-2026-11-18/qa-answer.md) |
| 原生角色与失败门禁 | team-qa 按 individual 范围委派阶段门禁 qa-lead；核对当前完整角色指令在启动时实际加载，父子均为 Sol/high，调用未覆盖模型。已有 smoke FAIL 导致策略阶段 BLOCKED，未启动后续执行或关闭故事。[绑定证明](runtime-evidence/cli-comprehensive-2026-11-18/role-proof.json) |
| 同一子代理追问 | followup_task 指向同一子代理；两回合均完成。追问没有工具调用或文件重读，继续保留 FAIL，拒绝签署 APPROVED。[角色证据](runtime-evidence/cli-comprehensive-2026-11-18/role-proof.json) |
| 真实压缩及恢复 | 已安装 CLI 的原生 app-server `thread/compact/start` 压缩 CLI 创建的线程；真实 PreCompact 与完成的 ContextCompaction 均存在。之后 `codex exec resume` 无工具调用，正确恢复标记、拒绝事实及三项裁决；检查点在压缩前至 QA 待答期间哈希不变。[压缩证明](runtime-evidence/cli-comprehensive-2026-11-18/compaction-proof.json)、[恢复结果](runtime-evidence/cli-comprehensive-2026-11-18/recovery.md) |
| 七类真实生命周期事件 | 本轮增量日志实际包含 SessionStart、PreToolUse、PostToolUse、PreCompact、Stop、SubagentStart、SubagentStop，共 129 条记录。范围限原受信任隔离目录及本轮受控调用。[事件增量](runtime-evidence/cli-comprehensive-2026-11-18/events.jsonl) |
| 中文空格工作树与配置隔离 | 真实 detached linked worktree，从 src 调用自身 helper、不传 root，读到本地 guided；原 checkout 仍 collaborative。配置、检查点及 agent-memory 三项忽略规则实际匹配。[工作树结果](runtime-evidence/cli-comprehensive-2026-11-18/worktree.md)、[路径纠正补测](runtime-evidence/cli-comprehensive-2026-11-18/worktree-memory.md) |
| 浏览器实际输入 | 既有游戏 Enter 输入使 title→play，状态时间推进；实际截图 drawn、uncaught=0。18 个自动测试另覆盖移动、暂停、确定性及 R/Enter/N 重试与状态重置。[运行结果](runtime-evidence/cli-comprehensive-2026-11-18/game-regression.md)、[实际截图](runtime-evidence/cli-comprehensive-2026-11-18/game-input.png) |
| smoke 最终裁决 fixture | 性能 FAIL+缺证据→FAIL；平台 UNANSWERED→NOT ASSESSED；quick 核心失败→保留 FAIL 及 quick 后缀。仅测试裁决规则，未运行完整 smoke Skill。[首回合](runtime-evidence/cli-comprehensive-2026-11-18/baseline.md) |

## 环境失败、纠正与覆盖边界

- PowerShell 默认选中 `codex.ps1`，被执行策略拒绝；改用已有 `codex.cmd`，未改变全局执行策略。
- 首轮默认 Python 缺少 PyYAML，103/105 通过、2 项返回环境未评估；确认仓库已有虚拟环境含要求的 PyYAML 6.0.3，指定 `CGS_PYTHON` 后重跑 105/105。[首轮日志](runtime-evidence/cli-comprehensive-2026-11-18/unittest-initial.txt)保留。
- `features` 子命令不支持 `--strict-config`，这是测试命令选择错误；改用 CLI 明确支持的 app-server 严格启动检查后退出 0。
- 多次 Git Bash/Git 沙箱启动失败，经正常自动审批重试成功；若干 CLI 启动刷新模型目录超时，9 次执行最终均正常退出。Python `-c` 引号错误、默认编码初读及纠正亦保留在 trace 中。
- 有效模型选择按实际回合记证；`config/read` 首末快照分别为 6.1-sol/high、6.1-sol/low，与后段实际 6.2-sol/xhigh 不同。不推断变化原因，不把读取配置的快照当作执行模型证明。[逐回合汇总](runtime-evidence/cli-comprehensive-2026-11-18/summary.json)保留两种证据。
- 首次工作树测试错误使用 `agent-notes` 路径；它不属于项目合同。补测真实 `agent-memory` 路径后三项均命中，未把错误 fixture 当作框架缺陷。
- **交互 TUI 未评估**：PTY 连 `codex.cmd --version` 的进程创建都被系统 `Access denied` 拒绝。没有测试 TUI `/compact` 或人工点击原生问题卡片；上述压缩证据严格属于原生 backend 接口和 CLI 恢复路径，自动触发压缩也未评估。
- **未逐个执行所有工作流或角色**：75 Skills/49 角色均有全量结构/来源/合同检查，但本轮原生角色实测为 qa-lead；Skill 实测为 qa-plan、team-qa 失败策略门禁及 smoke 裁决 fixture。这不等于其他完整流程都失败，也不能将它们计为本轮逐项运行通过。
- 本轮重跑已有游戏的构建、全套自动测试及真实输入；从零需求→brief→prototype→grow→Story 的完整创建链仅保留[既有 CLI 证据](codex-adaptation-status.md)，未重新生成游戏。
- 新工作树 hooks 的独立信任未测；七类事件不能扩大到该工作树。原生引擎编辑器/构建、人工试玩与乐趣、macOS、远端 CI 未评估。App 不在本轮范围。

## 隔离、恢复和交付

原受信任 fixture 同步当前工作树 1,190 个来源文件，逐文件哈希一致；其独立 Git HEAD 仍为 `f56bab3`，不伪装成来源提交。来源清单见 [prepared.json](runtime-evidence/cli-comprehensive-2026-11-18/prepared.json)。

归档前父控制器核对：QA 故事未回填、受控失败故事未改、`.env` 目标未落盘；全部 119 个原有跟踪文件、临时同步文件、原检查点和 fixture 索引已恢复。主仓库原有跟踪文件及索引在归档前逐字节不变。专用未来日期 smoke、epic fixture、生成 QA 计划均先归档再移除；中文空格工作树核对绝对路径后移除，避免污染后续流程。只有本轮 `.scratch` 原始证据及事件增量保留。[恢复证明](runtime-evidence/cli-comprehensive-2026-11-18/restored.json)、[清理证明](runtime-evidence/cli-comprehensive-2026-11-18/fixture-cleanup.json)。

归档不含推理、账号配置或不透明委派正文；文本路径归一化为 `<repo>`、`<probe>`，统一 LF 并移除行末留白，不冒充逐字节原始日志。该目录的四类文本在 `.gitattributes` 固定 LF，PNG 保持二进制检测，并核对 Git clean 过滤不改变代表文件字节。[文件哈希清单](runtime-evidence/cli-comprehensive-2026-11-18/archive-manifest.json)用于核对归档字节。详细原始记录与本轮验证驱动位于忽略目录 `.scratch/cli-comprehensive-2026-11-18/`。本轮只新增验证产物、同步覆盖说明并固定归档换行，不修改游戏或框架实现，不提交、不暂存主仓库改动。
