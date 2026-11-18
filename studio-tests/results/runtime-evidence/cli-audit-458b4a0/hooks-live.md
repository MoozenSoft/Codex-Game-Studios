本次隔离 CLI 验收六项均 **PASS**，具体回执如下。未实际提交、未手动调用 `dispatch.py`、未更改信任或调用其他 Skill。

1. **PASS — 普通终端放行**

   原生终端执行 `Write-Output CLI_ALLOW_458B4A0_22c1`，退出码 `0`，输出：
   ```text
   CLI_ALLOW_458B4A0_22c1
   ```

2. **PASS — 无效 JSON 写后提示**

   原生 `apply_patch` 创建指定文件，内容 `{broken`。工具回执 `{}`；紧随调用出现的 hook 上下文原话：
   ```text
   以下 JSON 当前无效，允许继续修复，但必要验收不能完成：<probe>\.scratch\cli-audit-458b4a0\hook-bad.json
   ```

3. **PASS — 修复并解析落盘 JSON**

   原生 `apply_patch` 修复，回执 `{}`。终端读取实际文件并使用 `ConvertFrom-Json -ErrorAction Stop` 解析，退出码 `0`，输出：
   ```text
   {"probe":"CLI_JSON_REPAIRED_458B4A0"}
   CLI_JSON_REPAIRED_458B4A0
   ```

4. **PASS — env 目标被项目 hook 前置拒绝**

   已发出原生 `apply_patch` 调用，内容仅为指定 sentinel。真实拒绝回执：
   ```text
   Command blocked by PreToolUse hook: 项目规则禁止通过工具读取或改写环境凭据文件: <probe>\.scratch\cli-audit-458b4a0\.env.cli-audit-probe.
   ```
   未换工具、改名或绕过。

5. **PASS — 跨项目索引上下文被明确拒绝**

   实际原生终端参数：
   ```text
   cmd: git commit --dry-run
   workdir: <probe>\.scratch\cli-audit-458b4a0\external-repo
   ```
   真实拒绝回执：
   ```text
   Command blocked by PreToolUse hook: 提交前校验未评估：实际提交目标不属于当前项目，不能检查另一个仓库的索引. Command: git commit --dry-run
   ```
   原因明确为目标属于另一个仓库，与坏 JSON 无关。这里 PASS 表示拒绝行为验证成功，未声称另一个仓库通过提交校验。

6. **PASS — 报告规则的模型决策 fixture**

   仅只读指定 `5-report.md`，按“首个匹配规则生效”判定：

   | Fixture | 最终 verdict | 首个命中规则 |
   |---|---|---|
   | A | **FAIL** | FAIL 第 4 条：必需手工检查失败，涵盖 Batch 3 性能；MISSING evidence 不能降低已知失败 |
   | B | **NOT ASSESSED** | NOT ASSESSED 第 4 条：必需平台检查存在 UNANSWERED |
   | C | **FAIL (quick — coverage and Batch 3 not checked)** | FAIL 第 4 条：Batch 1 核心检查失败；quick 后缀不改变 verdict |

   A/B/C 仅验证模型对规则的判定，未运行完整 smoke Skill，也不代表游戏实测或人工试玩。