两次 `exec_command` 调用均在指定的 `workdir` 发起，`cmd` 均为 `git commit --dry-run`。两次都由项目 `PreToolUse` hook 在 Git 执行前阻断，符合预期。未发生真实提交。

1. **暂存 JSON 无效**
   `workdir` 为 `<probe>`。来源为工具返回的项目 `PreToolUse` 拒绝。

   > Command blocked by PreToolUse hook: 提交前暂存区 JSON 校验未完成：.scratch/cli-full-20261118/bad-index.json Git 暂存内容不是有效 UTF-8 JSON；工作区修复后须重新暂存. Command: git commit --dry-run

2. **外部仓库提交上下文**
   `workdir` 为 `<probe>/.scratch/cli-audit-458b4a0/external-repo`。来源为工具返回的项目 `PreToolUse` 拒绝。

   > Command blocked by PreToolUse hook: 提交前校验未评估：实际提交目标不属于当前项目，不能检查另一个仓库的索引. Command: git commit --dry-run
