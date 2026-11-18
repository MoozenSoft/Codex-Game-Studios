# Codex hooks 与显式校验

实际事件协议与覆盖范围见 [codex-events.md](hooks-reference/codex-events.md)。`.codex/hooks.json` 注册七类事件，运行入口为 `.codex/hooks/run.sh`。注册、触发、协议回执与压缩完成分别记证。CLI 0.169.0 已通过七类项目 hook 的回执验收。TUI `/compact` 和自动压缩分别确认 PreCompact 提醒，原生 qa-lead 退出时确认 SubagentStop 提醒。其他客户端的修复后状态仍未评估。 [CLI hooks 复验](../../studio-tests/results/cli-hook-acceptance.md)

| 上游职责 | Codex 处理方式 |
| --- | --- |
| 会话启动与压缩 | SessionStart 恢复检查点；PreCompact 提醒保存；工作流负责落盘 |
| 工具前检查 | PreToolUse 对实际 Bash / exec_command / apply_patch 输入检查明确禁止的操作 |
| 工具后检查 | PostToolUse 检查实际落盘内容；普通问题允许继续修复 |
| 子代理开始、结束和 Stop | 最少事件日志；父代理按委派合同核对产物，不读取旧客户端私有会话日志 |
| write / read guard | `.agents/scripts/write-guard.sh`、`read-guard.sh` 保留领域算法，由调用工作流显式执行；不假定存在旧 Write/Edit/Read 工具事件 |
| 注册表追加与状态 | `.agents/scripts/registry.sh validate/compare`；写前保留旧版本进行 compare，不从 patch 臆造完整新文件 |
| 资产、设计与评审检查 | 对应领域工作流和 helper，结果由阶段门禁检查；完整流程不能仅凭 hook 注册宣称通过 |
| Notification、statusLine、上游版本通知 | 旧客户端入口退役；完成、阻塞与升级说明由当前会话和发布文档报告 |

所有 helper 输出观察结果而非自动授权。必要失败或必要检查无法执行时，故事或阶段不能关闭；普通编辑仍可修复。统一入口为 `validate-framework.py`，领域门禁与评审凭据仍由其所属工作流负责。

运行矩阵中的 App 与 CLI 证据分开维护；静态配置、脚本测试和真实客户端调用是三种不同证据。
