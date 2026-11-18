1. **恢复标记：PASS**
   `CLI_RESTORE_7c1f0d9a`，直接来自启动上下文，未通过文件或日志获取。

2. **项目 Skill：PASS**
   显式读取本 checkout 的 [codex-studio-probe/SKILL.md](<probe>/.agents/skills/codex-studio-probe/SKILL.md)，返回 `STUDIO_SKILL_OK_6f19`。未使用同名插件。

3. **终端与配置：PASS（经重试）**
   `git rev-parse --show-toplevel` 实际返回当前隔离 checkout。指定 Git Bash 首次退出 1、无输出；正常自动审批重试退出 0。配置结果：
   - `automation: collaborative`
   - `rigor: minimal`
   - `review_mode: solo`
   - `workflow: minimal`
   - `team.size: individual`
   - `engine: unset`
   - `engine_values: name=unset version=unset language=unset`
   - `engine_row: engine=unset code_root=src(detected) test_root=unset asset_root=- run=- build=- test=- smoke=-`

4. **原生终端输出：PASS**
   实际输出 `CLI_ALLOW_FULL_20261118`。

5. **PostToolUse 与 JSON 修复：PASS**
   原生 `apply_patch` 创建 `{broken` 后，客户端实际回执：
   > 以下 JSON 当前无效，允许继续修复，但必要验收不能完成：<probe>/.scratch/cli-full-20261118/hook-invalid.json

   随后通过 `apply_patch` 修复。终端首次解析因参数引号失败，改用标准输入调用已有 `CGS_PYTHON` 后退出 0，解析并断言落盘值为 `{"probe":"CLI_FULL_REPAIRED_20261118"}`。

6. **PreToolUse 阻断：PASS**
   已实际发出原生 `apply_patch` 调用，创建 `.env.nonsecret-probe` 的请求被客户端拒绝：
   > Command blocked by PreToolUse hook: 项目规则禁止通过工具读取或改写环境凭据文件: <probe>/.scratch/cli-full-20261118/.env.nonsecret-probe.

   未换工具绕过。

7. **三个决策 fixture：PASS**
   已只读核对当前源 `smoke-check/references/5-report.md`：

   | Fixture | Verdict | 依据 |
   |---|---|---|
   | a：自动与核心 PASS、性能 FAIL、Logic 证据 MISSING | **FAIL** | 已知性能失败优先于证据警告 |
   | b：其他检查 PASS、请求平台一项 UNANSWERED | **NOT ASSESSED** | 必需平台检查缺少回答 |
   | c：quick 模式核心 FAIL | **FAIL (quick — coverage and Batch 3 not checked)** | quick 后缀不改变失败判定 |

以上是 CLI 验证与决策 fixture，未执行游戏运行测试或完整 smoke-check Skill。无剩余无法执行项；未 commit、安装、修改全局设置或运行手动 hook handler。
