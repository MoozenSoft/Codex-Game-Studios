# Codex 事件输入边界

真实事件 fixture 和客户端证据优先于上游协议说明。入口从 stdin 读取一个 JSON 对象，包含 `hook_event_name`、`session_id`，工具事件另外提供 `tool_name`、`tool_use_id` 与 `tool_input`。

已观察到的 shell 工具名为 `Bash`，命令从 `tool_input.command` 读取。apply_patch 同样读取 `command` 中的 patch，支持多文件新增、更新、移动和删除。不能把旧客户端的 `file_path/content/old_string/new_string` 当成当前工具协议。

PreToolUse 拒绝结果采用 `hookSpecificOutput`，包含实际事件名与 `permissionDecision: deny`、`permissionDecisionReason`。上下文告警采用对应事件的 `additionalContext`；处理器不伪造工具执行成功或回滚。

日志仅保留最少事件元数据，不保存原始命令、消息或凭据。同一 session/event/tool_use_id 重复事件只记一条日志；不同工具事件仍独立处理。

未知工具或无法解析的输入不作为检查通过。实际支持范围、不可覆盖的 MCP/脚本内部写入和必要完成检查见 `codex-events.md`。
