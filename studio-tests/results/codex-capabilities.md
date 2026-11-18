# Codex 客户端能力基线

本文保留任务 1 的历史探测结果；当前迁移进度和完整运行范围见[验收状态](codex-adaptation-status.md)及[运行矩阵](../runtime-matrix.json)。下文的“待验证”和 pending 指当时状态。

记录日期：2026-11-16。迁移分支：`codex/codex-adaptation`；来源基线：`7655fef`。

任务 1 的来源盘点与双端最小能力基线已完成：Windows CLI 与 App 均取得 Skill 读取、项目角色委派及正常受信任的 SessionStart hook 的真实运行证据。App 中的完整最终答案现已直接核验，三个口令与运行记录一致，此前停留 Thinking 的显示问题已关闭。独立的公共配置迁移已开始，正式 Skills、完整事件校验和游戏工作流仍待后续任务。

## 环境与真实探测

| 项目 | 观察结果 | 判定范围 |
| --- | --- | --- |
| Windows Codex CLI | `0.169.0`；Sol 只读探测完成 | 仅代表下列已实际运行的能力 |
| CLI Skill | 无探测 Skill 时返回 `PROBE_UNAVAILABLE`；添加后返回文件内的 `STUDIO_SKILL_OK_6f19` | 显式调用、定位与读取最小项目 Skill 通过 |
| CLI 项目角色 | `.codex/agents/studio-probe.toml` 的角色在持久会话中被真实委派，返回 `STUDIO_ROLE_OK_e94a` | 最小角色绑定与结果回收通过；追问续作等完整场景仍待测 |
| CLI 临时会话 | 同一探测在 `--ephemeral` 会话中委派失败：`no rollout found for thread id` | 本机此调用组合不可作为角色验收方式，不能泛化为所有版本不支持 |
| CLI hooks | 最初 `hooks/list` 为 `untrusted`；用户授权后在 App 的 Review hooks 仅选中唯一测试定义并 Allow selected，接口变为 `trusted`。随后真实 CLI 新会话收到 `STUDIO_HOOK_OK_b57c`，目录内生成标记 | 最小 SessionStart 执行通过；未使用绕过信任参数，其他事件仍待验证 |
| 项目信任 | 用户明确批准信任 `.scratch/codex-capability-probe` 与已检查的唯一测试 hook，未扩大到整个仓库 | 目录信任与 hook 信任为两个独立步骤；配置能被发现不表示已经允许运行 |
| 交互终端 | 当前工具创建交互 PTY 时返回 `CreateProcessW ... Access is denied` | 未能通过 CLI `/hooks` 检查和审阅 hook |
| 桌面 App | 包版本 `26.1111.2228.0`；`Local`、迁移分支与 `6.1 Sol Light`；请求实际读取 Skill 并返回 `STUDIO_SKILL_OK_6f19`，项目子代理返回 `STUDIO_ROLE_OK_e94a`，启动上下文返回 `STUDIO_HOOK_OK_b57c` | 最小 Skill、项目角色与 SessionStart 执行通过；原始运行记录见 [App 探测证据](codex-app-probe-trace.json) |
| App 工作区 | 此前工作区设置加载错误导致 Send 禁用；本次重试错误消失，正常发送请求并取得 completed 运行记录 | 发送恢复；没有据此假定账号或网络问题的具体原因 |
| App 最终结果显示 | 直接查看当前窗口截图及可访问性树，三个正确口令、完整最终答案和完成后的操作控件均已显示，Thinking 与 Stop 消失 | 最小探测结果显示通过，见 [界面验证记录](codex-app-visible-result.json)；此前显示问题已关闭 |
| Git Bash | `5.2.37`；沙箱内进程以 `0xC0000142` 退出，授权的沙箱外同命令成功 | 不能把 PATH 中的 WSL `bash.exe` 当成 Git Bash；测试必须记录执行环境 |
| Python | 实际解释器 `3.14.3` 可执行测试；PATH 的 Python Install Manager 在沙箱身份下找不到宿主运行时 | 测试使用已存在解释器，避免管理器自动安装；未增加项目依赖 |
| Node.js | `24.14.0` | 只检查版本，尚未做游戏浏览器运行测试 |
| 浏览器 | 本机 Chrome `157.0.8103.78`、Edge `157.0.4341.60` 可执行文件存在 | 只核对安装与文件版本；实际游戏运行在任务 5 验证 |

CLI 在探测中还报告模型目录刷新超时，但随后 Sol 请求与上述最小场景完成；这是环境观察，不作为正式工作流失败或通过的替代证据。

本轮冻结的验收基线为 CLI `0.169.0`、App `26.1111.2228.0`，模型 `gpt-6.1-sol`；迁移首版暂以这些已测版本为最低验收起点，较低版本不作支持承诺。它们已通过最小机制探测，App 最终结果显示也已核验；完整支持声明仍取决于后续核心流程和其余客户端交互验证。

## 来源覆盖与基线检查

- [迁移清单](../migration-inventory.json) 登记 743 条文件/事件记录，含全部 78 个 Skill 入口、49 个角色、14 份规则、54 个脚本、18 个 hook 辅助文件与 8 类事件。
- 正式迁移集合为 75 个 Skills；3 个旧名入口显式登记退役及替代项。
- 上游只读 `compat-inventory.sh` 报告：读取 426 个相关文件，其中 268 个文件有 Claude 专用依赖，命中 2,500 行。这是兼容性盘点，不能视作测试通过。
- [运行验收矩阵](../runtime-matrix.json) 登记 27 个必测场景：App/CLI 各 6 项、9 个 Skill 类别和 6 个角色类别。矩阵中的完整场景与最小能力探测分开记录。
- [清单测试](../automated/test_inventory.py) 先在缺清单时观察到 6 项失败；建立清单后通过。增加矩阵覆盖测试后观察到缺矩阵导致的失败，建立矩阵后 7 项全部通过。
- 迁移前的 68 个已跟踪 Bash 脚本通过 `bash -n`；`one-shot-driver.js` 通过 `node --check`。这是脚本语法基线，不代表脚本行为或浏览器游戏运行通过。
- 全部迁移组件仍为 `pending`，没有把来源盘点或最小客户端探测标记为正式组件运行通过。

## 已开始的公共配置迁移

`.agents/scripts/yaml-helper.sh`、`engine-row.awk`、`.agents/engines/engines.tsv` 及中文配置说明已建立。保留上游解析算法、取值来源与 TSV；新增显式 `--root`、当前 checkout 定位和未知命令的失败退出，去除 Claude 专属环境变量依赖。

8 项真实配置测试覆盖默认 `collaborative`、rigor 独立性、本地覆盖、无效枚举、中文空格路径、子目录启动、显式根目录和 `.agents/.codex` 测试根拒绝。与原 7 项清单测试合计 15 项通过，原始结果见 [配置测试记录](config-tests-2026-11-16.txt)。配置行为先经历缺少迁移入口导致的 RED；目录拒绝用例另复现失败后修复为 GREEN。

任务 2 的其余公共文档、脚本、路径规则、scaffold 和调用者仍待迁移，不能将这组测试推广为任务 2 完成。

验证命令（使用实际可用的 Python 解释器）：

```text
python -m unittest discover -s studio-tests/automated -p test_inventory.py -v
```

## 后续验收前提

1. App 项目“Codex Studio 验收”的最小 Skill、角色、SessionStart 和最终结果显示已验证；继续核验恢复会话及后续交互。源目录为 `.scratch/codex-capability-probe`，项目、目录及测试 hook 信任均已取得明确用户授权。
2. App 的正常 Review hooks → Details → 选中唯一测试项 → Allow selected 已完成；后续变更 hook 定义时重新正常审阅，不将当前信任泛化为其他 hook 的授权。
3. 补齐角色追问续作、提问授权、工作树和核心流程等矩阵场景，随后才能决定相应支持声明。

任务 1 完成的是来源清单、运行矩阵和双端最小机制基线。完整 App/CLI 适配仍需后续任务和矩阵中的必要场景通过；目前不宣布整套框架适配完成。
