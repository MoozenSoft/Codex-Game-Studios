1. 检查点标记：`CLI_RESTORE_7c1f0d9a`。
2. 无效 JSON 触发真实 PostToolUse 回执，允许继续修复但不能完成必要验收；随后用原生 apply_patch 修复为 `{"probe":"CLI_FULL_REPAIRED_20261118"}`，并用已有 CGS_PYTHON 解析落盘文件成功。
3. `.env.nonsecret-probe` 被真实 PreToolUse 拒绝；未获准换工具绕过，也未绕过。
4. smoke 决策 fixture：a **FAIL**；b **NOT ASSESSED**；c **FAIL（quick — coverage and Batch 3 not checked）**。仅为决策验证，非游戏运行测试或完整 Skill 执行。
