# Codex CLI 缺口复验

后续已修复此处记录的 hook 响应协议问题，并通过七类 CLI hook 的回执验收。下文保留当时的失败和现场结果。 [CLI hooks 复验](cli-hook-acceptance.md)

2026-11-18 在 Windows 上复验 Codex CLI `0.169.0`，基线 HEAD 为 `458b4a0`。覆盖框架文件来自当前 checkout。原生交互与自动压缩使用既有受信任探针，工作流及引擎使用独立的 `.scratch/cli-gap-validation` 工程。

**验收存在一项已在真实界面复现的失败。** TUI 的 `/compact` 能完成压缩并恢复上下文，但项目的 `PreCompact` hook 输出被 CLI 拒绝。当前 `SubagentStop` 输出也与同版本协议不兼容，具体客户端回执待复验。

| 缺口 | 实测结果 | 证据 |
| --- | --- | --- |
| 交互入口与 `/compact` | VS Code 集成终端启动真正的 CLI。执行原生 slash 命令后，界面同时显示 `hook returned invalid PreCompact hook JSON output` 与 `Context compacted`。后续回合正确返回预先提供的 `TUI_GAP_80QF7`。 | [界面转录](runtime-evidence/cli-gap-validation/tui-observation.txt)、[TUI 线程证据](runtime-evidence/cli-gap-validation/tui-thread-proof.json) |
| CLI 原生问题 | 单次启用 `default_mode_request_user_input`。界面出现 Alpha 和 Beta 选项，两次提交结果均为 Alpha，CLI 均回显 `SIGNAL Alpha`，会话记录了 `verified_answer`。 | [TUI 线程证据](runtime-evidence/cli-gap-validation/tui-thread-proof.json) |
| 自动压缩 | 进程级阈值设为 6,500 token，输入 29,146 字节测试内容。恢复回合自动触发 `PreCompact` 并完成 `ContextCompaction`，无命令或文件写入，成功返回随机标识。两次 CLI 退出 0，探针检查点哈希一致。 | [运行断言](runtime-evidence/cli-gap-validation/auto-result.json)、[压缩完成事件](runtime-evidence/cli-gap-validation/auto-thread-proof.json) |
| 新 linked worktree 的 hooks | 同一受信任仓库中新建工作树，七个项目 hook 均显示 `enabled=true`、`trusted`。实际启动产生事件日志，并返回工作树专属检查点标识。测试工作树已回收。 | [注册回执](runtime-evidence/cli-gap-validation/linked-hooks-list.json)、[真实启动](runtime-evidence/cli-gap-validation/linked-run.jsonl) |
| 完整 Smoke 检查路径 | 对隔离的既有 Web 游戏运行 `$smoke-check sprint --platform pc`。6 个 Vitest 和 12 个 Playwright 通过，单文件构建成功。缺人工检查和逐故事证据，整体及 PC 裁决均为 `NOT ASSESSED`。 | [落盘报告](runtime-evidence/cli-gap-validation/smoke-report.md) |
| 从需求到可玩原型 | `$prototype` 先等待，明确模拟批准后才生成 Signal Tiles。Chrome 中 Enter 开始、三次 Space 获胜、R 重置，brief 清单 9/9。选择 `Not now` 后，grow 对未提交原型返回 guard 退出 3。 | [初轮简报](runtime-evidence/cli-gap-validation/fresh-brief.md)、[获胜截图](runtime-evidence/cli-gap-validation/fresh-play.png)、[清单](runtime-evidence/cli-gap-validation/fresh-checklist.tsv)、[grow 阻断](runtime-evidence/cli-gap-validation/fresh-grow.md) |
| grow 正常路径 | 隔离仓库提交并标记原型快照后，基准双重放、JavaScript 与 TypeScript 均匹配。实际 Vitest 2/2、Playwright 3/3、生产构建及冒烟通过，原型目录状态干净。CLI 回合在产物写出后达到 540 秒上限，保留其退出 124。 | [实际迁移产物](runtime-evidence/cli-gap-validation/fresh-grow-artifact.md)、[命令输出](runtime-evidence/cli-gap-validation/growth-observations.json)、[原型快照](runtime-evidence/cli-gap-validation/fresh-snapshot-proof.json) |
| 新 Story 创建、实现与关闭 | `create-stories` 生成一条 Ready 故事。新增 N 键用例在旧实现上先失败。实现回合随后通过 3 个 Vitest、6 个 Playwright 和 1 个冒烟测试，保持旧 R 键行为。同种子重放仍匹配原型。实现回合在产物写出后达到 540 秒上限。独立的 `story-done` 回合复跑 9 项测试，按模拟批准将故事写为 Complete。 | [Story 创建](runtime-evidence/cli-gap-validation/fresh-story.md)、[红绿测试](runtime-evidence/cli-gap-validation/story-test-observations.json)、[关闭回执](runtime-evidence/cli-gap-validation/fresh-close.md)、[最终 Story](runtime-evidence/cli-gap-validation/fresh-story-artifact.md) |
| 原生引擎 | Unity 6000.3.5f2 批处理调用 C# 验收入口，Windows Player 构建退出 0，0 错误。初次尝试加载场景后等待退出超时，增加试验专用退出入口，重新构建的 Player 成功运行并退出 0。Godot 4.7.2 自定义构建成功运行最小场景，编辑器导入两次超时。Unreal 5.7.1 加载编辑器，ResavePackages commandlet 在 210 秒内未完成。 | [首次命令与退出码](runtime-evidence/cli-gap-validation/engines-result.json)、[Unity 构建记录](runtime-evidence/cli-gap-validation/unity-build-excerpt.txt)、[Unity Player 运行](runtime-evidence/cli-gap-validation/unity-player-confirmed-excerpt.txt)、[Godot 场景日志](runtime-evidence/cli-gap-validation/godot-direct.log)、[Unreal 启动日志](runtime-evidence/cli-gap-validation/unreal-commandlet-excerpt.txt) |
| 远端 CI | GitHub Actions API 对基线提交与仓库近期运行分别返回 0 条。当前缺远端运行可供验收。 | [查询结果](runtime-evidence/cli-gap-validation/remote-ci.json) |

## Hook 协议复现

`hooks.json`、`run.sh` 和 `dispatch.py` 在项目与交互探针中的 SHA-256 分别一致。直接运行 dispatcher 时两个事件均退出 0，但都输出 `hookSpecificOutput.additionalContext`。Codex CLI `0.169.0` 的两种输出结构都拒绝这个字段。它们接受通用 `systemMessage` 用于显示提醒。界面上的 `PreCompact` 失败是直接观察，`SubagentStop` 的结论来自同版本结构与本地输出的对照。 [输出与哈希](runtime-evidence/cli-gap-validation/hook-payloads.json) · [Codex 0.169.0 协议源码](https://github.com/openai/codex/blob/rust-v0.169.0/codex-rs/hooks/src/schema.rs) · [PreCompact 官方文档](https://learn.chatgpt.com/docs/hooks#precompact)

工具内置 PTY 仍报 `Access denied`。自行创建的 ConPTY 启动进程后，CLI 报 `stdin is not a terminal`。交互实测通过 VS Code 集成终端完成。启动时为测试同步问题接口而启用的单次参数与共享后台特征不一致，测试选择了独立运行。

## 补跑的 Skill 场景

- 八个新模板场景实际启动 CLI 并退出 0。覆盖 [next-step](runtime-evidence/cli-gap-validation/next-step.md)、[project-stage-detect](runtime-evidence/cli-gap-validation/project-stage-detect.md)、[content-audit](runtime-evidence/cli-gap-validation/content-audit.md)、[test-flakiness](runtime-evidence/cli-gap-validation/test-flakiness.md)、[ux-review](runtime-evidence/cli-gap-validation/ux-review.md)、[create-epics](runtime-evidence/cli-gap-validation/create-epics.md)、[regression-suite](runtime-evidence/cli-gap-validation/regression-suite.md) 与 [release-checklist](runtime-evidence/cli-gap-validation/release-checklist.md)。范围为新项目路由、输入缺失或明确的前置条件分支。
- `team-narrative` 在第一道门禁前使用委派简报传入本地 writer 规范。子代理交付了隔离草稿，父回合收回并停在等待方向选择。该接口使用角色规范降级，原生 writer 绑定待测。 [门禁结果](runtime-evidence/cli-gap-validation/team-narrative.md) · [实际草稿](runtime-evidence/cli-gap-validation/narrative-draft.md) · [委派回执](runtime-evidence/cli-gap-validation/narrative-thread-proof.json)

75 个 Skills 和 49 个角色的既有结构证据继续适用，当前源文件与前轮清单逐项比较 SHA-256。逐个完整工作流、逐个原生角色、人工试玩、Godot 和 Unreal 打包、macOS 与远端 CI 仍有覆盖缺口。 [逐项对照](runtime-evidence/cli-gap-validation/component-coverage.json) · [本轮命令与结果](runtime-evidence/cli-gap-validation/cli-execution.json)
