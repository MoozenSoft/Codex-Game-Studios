# Codex 事件校验与覆盖范围

`.codex/hooks.json` 注册 SessionStart、PreToolUse、PostToolUse、PreCompact、Stop、SubagentStart、SubagentStop。
处理器为 `.codex/hooks/dispatch.py`，输入解析为 event_input.py，跨进程日志由 event_log.py 维护。项目与 hook 定义需要客户端正常审阅信任；注册存在不代表已经执行。
上游 Notification 与 statusLine 不迁移为虚构事件；完成和阻塞信息通过实际会话报告。

SessionStart 读取检查点；PreCompact 提醒保存已有任务记录，保留文件中的决定；其余生命周期事件登记最少日志，不覆盖用户检查点。
日志只记录时间、事件、工具名与调用 ID，不保存原始命令或用户消息。
`features.session_state=off` 关闭恢复注入和事件日志；工具守卫仍执行。日志以进程间锁串行追加，工具事件按 session/event/tool_use_id 去重。日志写入失败会明确提示未评估，但不会跳过禁止操作检查。

PreToolUse / PostToolUse 的 matcher 覆盖 Bash、exec_command、apply_patch 及可选的 `functions.` 命名空间；命令输入归一化接受 `command` 或 `cmd`，两者冲突或缺少必要命令时明确拒绝并报告未评估。apply_patch 输入接受 `command`、`input` 或原始补丁字符串。patch 支持新增、修改、移动和删除的多目标提取；越出项目或环境凭据路径在执行前拒绝。
命令守卫覆盖直接出现的危险 Git 与递归删除形式，属于辅助约束，不是完整 shell 解析器或权限边界；客户端 sandbox 与托管策略继续生效。
本地脚本内部、MCP 写入及未匹配工具路径不会被这些文件规则完整覆盖，交付时继续运行统一 validator。
识别到当前项目的普通 Git commit 命令时，使用归一化后的命令调用 `git-index-check.py` 检查实际暂存的 JSON 字节；坏暂存内容或必要检查无法执行会拒绝该调用。工作区文件修复后仍需重新暂存。预检先核对原生命令 workdir/cwd、事件 cwd 和 git -C 解析出的 Git 根目录；当前项目子目录可用，外部或嵌套独立仓库明确拒绝并标记未评估。命令内切换目录、自定义 Git 环境或不支持的全局配置覆盖同样不猜测索引。这个预检不替代对任意嵌套 shell、外部仓库和发布操作的完整审批。

客户端仍需正常审阅 hook 变更。PreCompact 与 SubagentStop 使用通用 `systemMessage` 呈现提醒，检查点继续由工作流落盘。CLI 0.169.0 的手动压缩、低阈值自动压缩以及原生子代理退出均返回 `completed`，提醒显示为 `warning`。SessionStart 和 PostToolUse 的上下文注入继续使用对应事件的 `hookSpecificOutput`。 [CLI hooks 复验](../../../studio-tests/results/cli-hook-acceptance.md) · [0.169.0 输出结构](https://github.com/openai/codex/blob/rust-v0.169.0/codex-rs/hooks/src/schema.rs)

PostToolUse 的 patch 输入缺失或无法提取文件目标时退出2并报告未评估；有目标时读取实际落盘 JSON，坏格式会提示修复，不能撤销已经发生的写入。工具执行前不因为普通结构未完成而拦截后续编辑。
关闭故事或阶段前调用 `.agents/scripts/validate-framework.py`；必要失败退出1，必要检查无法运行退出2，可选未评估明确列出，不冒充通过。
Stop 不自动把仓库所有未迁移项视为聊天失败；阶段完成门禁由具体工作流显式调用，避免阻止修复性工作。

SubagentStop 提醒核对父任务产物合同；事件本身不知道产物路径，不把“代理结束”当作“验收通过”。
完整角色产物、评审凭据、资产命名和注册表检查仍由对应领域 helper 与工作流负责；每项具体证据按运行矩阵登记。
