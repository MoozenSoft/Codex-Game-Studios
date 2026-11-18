# Windows Codex CLI hooks 复验

2026-11-18，使用 Windows Codex CLI `0.169.0` 复验 `PreCompact` 和 `SubagentStop`。两者现在用通用 `systemMessage` 显示提醒。修复前新增的两个回归断言均失败，修复后通过。 [Dispatcher](../../.codex/hooks/dispatch.py) · [回归测试](../automated/test_hooks.py) · [前轮失败报告](cli-gap-validation.md)

| 场景 | 客户端结果 |
| --- | --- |
| 手动压缩 | CLI app-server 返回 `PreCompact completed`，提醒作为 `warning` 呈现。随后收到 `contextCompaction` 完成事件，下一回合取回预置随机标识。 |
| 交互终端 | 在上次报错的同一受控 TUI 中再次运行 `/compact`。界面显示中文检查点提醒及 `Context compacted · 19s`。隔离日志追加一条 `PreCompact`。 |
| 自动压缩 | 单次线程阈值设为 6,500 token。自动压缩收到同样的 `PreCompact completed` 提醒及压缩完成事件，后续回复匹配预置随机标识。 |
| 原生子代理退出 | 原生绑定 `qa-lead`，父会话取回子代理标识。子线程返回 `SubagentStart completed` 和 `SubagentStop completed`，退出提醒要求核对产物路径和证据。 |
| 其余项目 hooks | 启动、工具前后与普通停止均有 `completed` 回执。三个结构化场景合计 16 条完成回执，覆盖全部七类事件。 |

验收使用已受信任的隔离探针。探针 dispatcher 在测试后恢复，检查点与索引哈希一致。手动压缩首轮在完成事件之后、回合结束之前发送恢复输入，客户端拒绝该输入。复试等待回合结束后成功。子线程最早的订阅请求收到尚无 rollout 的提示，后续仍取得归属于该子线程的项目 hook 回执。 [客户端通知和完整性证据](runtime-evidence/cli-hook-acceptance.json)

全量自动化 106 项通过，其中 hooks 22 项。CLI 运行矩阵中的 hooks 项恢复为通过。
