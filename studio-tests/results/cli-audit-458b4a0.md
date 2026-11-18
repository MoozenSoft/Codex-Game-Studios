# 458b4a0 的 CLI 定向验收

2026-11-17，Windows Codex CLI `0.169.0`。本轮针对提交 `458b4a0` 的变更运行真实 `codex exec --json --approve-for-me` 和同线程 `exec resume`，没有重跑共享框架全量测试。沿用用户配置的 `gpt-6.1-sol / high`，没有传入模型或推理强度覆盖。

结果：下表定向检查通过；不表示所有 Skills、角色和游戏端到端流程都已重验。[结构化汇总](runtime-evidence/cli-audit-458b4a0/summary.json)分别记录真实工作流、决策 fixture 与未评估范围。

| 检查 | 实际结果 |
| --- | --- |
| 检查点恢复 | 新 CLI 会话返回启动上下文中的随机标记；没有通过工具读取检查点或 hook 文件获取它 |
| 锁定的共享引擎 | 实际 helper 返回 Web、src、tests，并说明忽略本地 Unity 覆盖 |
| Windows 绝对路径 | Git Bash 使用反斜杠绝对 helper 路径，最终正确读取自身引擎表；首次沙箱启动失败后按正常审批重试 |
| 正常工具放行 | 原生终端输出验收标记，退出0 |
| JSON 写后提示与修复 | 原生 apply_patch 写入坏 JSON 后收到真实 hook 提示；随后修复并从落盘文件解析成功 |
| env 路径前置拒绝 | 只含无秘密测试标记的 patch 被 PreToolUse 拒绝；独立核对目标没有落盘 |
| 跨仓库提交上下文 | 原生终端将 workdir 指向临时独立仓库并调用 git commit --dry-run，被明确以实际目标不属于当前项目拒绝 |
| 异步问答待答 | 真实调用 request_user_input_async，两个问题使用 title 和字符串选项；仅返回 accepted:true 后停在 WAITING，没有写计划、回填或记录完成 |
| 明确输出选择 | 同一线程收到 write_qa_plan=yes、backfill_stories=no 后保存计划；故事423字节及哈希不变，没有再次索取同一授权 |
| 当前索引坏 JSON | 隔离索引暂存坏 JSON 后，原生 git commit --dry-run 被实际 PreToolUse hook 拒绝；没有执行真正的 commit |
| smoke 判定 fixture | 性能FAIL且有MISSING证据→FAIL；平台UNANSWERED→NOT ASSESSED；quick核心FAIL→保留FAIL及quick后缀 |
| 原项目保护 | 119个原有跟踪文件字节不变，原检查点及原Git索引已恢复 |

smoke 三项仅检验模型根据 Phase 5 规则作判断，没有运行完整 smoke Skill，也没有进行游戏性能测量或人工试玩。QA 用例是专用计数规则故事，不是游戏功能完成验收。

## 信任和隔离环境

使用此前获授权的 `<probe>` 隔离目录。最初只同步本次变更的框架文件；真实 QA 首回合发现旧目录缺少 python-run.sh 等依赖，必要检查明确保留未评估，没有把缺失伪装成通过。随后备份并同步当前提交的完整框架及验收资料1125文件，逐字节核对一致，再补齐来源清单所需的18个缺失目标；下一回合真实框架校验退出0。初次失败及后续修正均保留。

该隔离目录有独立 Git 历史，其 HEAD 仍为 f56bab3，无法解析458b4a0是预期；没有重置或创建提交来伪装同一历史。来源由同步哈希、当前提交及父会话独立核对确认。

CLI将变更的PreToolUse和PostToolUse定义标为modified。交互PTY启动两次均遭系统拒绝后，用户在CLI正常/hooks入口审阅并允许这两项；只读hooks/list随后确认七项定义均为enabled、trusted。没有使用信任绕过参数，没有脚本写全局trusted_hash。七项受信任不等于七类事件都已真实触发。

验收结束恢复临时同步的框架、检查点及索引；在隔离目录保留用户刚正常审阅的新hooks及必要运行依赖，共7个文件，避免把定义回退为待重新审阅的旧版本。再次核对七项定义仍trusted、119个既有跟踪文件无变化、索引与备份逐字节一致。保留的新适配器和生成的QA计划均仅位于隔离验收目录，不是游戏源码修改。

## 证据与实际边界

- [四次CLI执行及线程摘要](runtime-evidence/cli-audit-458b4a0/summary.json)，[启动及配置结果](runtime-evidence/cli-audit-458b4a0/baseline.md)。
- [真实hook回执](runtime-evidence/cli-audit-458b4a0/hook-receipts.json)：从本次会话的原始工具输出和hook上下文提取，包含三次前置拒绝及一次写后告警，不依赖模型自报结论。
- [异步工具调用与accepted回执](runtime-evidence/cli-audit-458b4a0/question-tool.json)，[待回答结果](runtime-evidence/cli-audit-458b4a0/qa-gate.md)，[明确回答后的结果](runtime-evidence/cli-audit-458b4a0/qa-answer.md)。
- [生成的QA计划](runtime-evidence/cli-audit-458b4a0/qa-plan-generated.md)，[父会话文件和恢复核对](runtime-evidence/cli-audit-458b4a0/parent-checks.json)，[受信任定义列表](runtime-evidence/cli-audit-458b4a0/hook-registration.json)。
- 原始CLI命令、失败重试和文件变更摘要位于同目录的四份trace.json；仅规范化测试路径，未导出账号配置、其他会话或推理内容。详细原始记录保留在本地忽略目录 `.scratch/cli-audit-458b4a0/`。

本轮模型使用原生exec_command/cmd/workdir和apply_patch，CLI在hook边界将终端事件规范化为Bash，patch事件为apply_patch。证明的是该CLI实际输入路径；不能据此将所有可能的原始命名空间和参数形状都登记成客户端实测。

模型目录刷新超时、首次Git Bash沙箱失败、非UTF-8默认读取后显式UTF-8重读等环境偏差保留。它们没有阻止最终四次CLI执行正常退出，但不能删掉后只保留成功描述。

App本轮未重验；真实PreCompact、完整游戏smoke/人工试玩、原生引擎、全部角色流程和远端CI仍未评估。该报告补充本提交的CLI证据，不扩大旧运行矩阵的通过范围。
