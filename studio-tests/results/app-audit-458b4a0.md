# 458b4a0 的 Codex App 定向验收

2026-11-17，Windows包 `OpenAI.Codex 26.1111.2228.0`，后端 `0.169.0-alpha.11.1`。客户端当前显示名为ChatGPT，用户确认操作目标；实际使用Codex模式、既有app-web-acceptance项目，原始线程来源为Codex Desktop。沿用界面选定的GPT-6.1 Sol高推理强度，没有切换模型。

同一App会话完成四回合：启动/配置只读探测、真实hooks及QA待答、通过原生问题卡片提交两个答案、坏暂存JSON及报告规则验证。[汇总](runtime-evidence/app-audit-458b4a0/summary.json)记录15项定向断言通过。所有请求和答案均在App界面操作；本地app-server协议只用于读取本轮线程及信任状态，没有用CLI发起或续作模型任务。

## 目标操作与测试断言

**被拒绝的操作没有通过业务验收。** 下表中的通过是实际行为符合测试预期。

| 场景 | 目标操作结果 | 定向断言 |
| --- | --- | --- |
| 启动检查点 | 不读取检查点文件，直接返回启动上下文的随机标记 | 通过 |
| 共享引擎解析 | Web及src/tests正确，本地Unity被忽略；真实Git Bash最终退出0 | 通过 |
| 普通原生终端 | 输出APP_ALLOW标记，退出0 | 通过 |
| 原生patch写坏JSON | JSON无效，真实PostToolUse提示必要验收不能完成 | 告警断言通过，坏内容不合格 |
| 修复JSON | 原生patch修复，实际落盘文件解析成功 | 通过 |
| env专用标记patch | PreToolUse拒绝，无文件落盘 | 阻断断言通过，操作为BLOCKED |
| 独立仓库workdir下commit --dry-run | 明确拒绝以另一个仓库索引代替当前项目检查 | 阻断断言通过，外部索引未评估 |
| 异步问题仅accepted | App可见WAITING；计划不存在、故事哈希未变 | 待答断言通过，不是输出获批 |
| 原生问题卡片yes/no | 第一题选写完整计划，第二题选不回填，再发送 | 两个独立答案实际送达 |
| QA输出 | 保存完整七项用例计划，故事未回填且仍Ready；框架静态校验退出0 | 输出选择断言通过，不代表故事用例已执行 |
| 当前项目坏暂存JSON | 实际git commit --dry-run被指定坏JSON的PreToolUse拒绝 | 阻断断言通过，目标仍BLOCKED／无提交资格 |

smoke只做三项模型决策fixture：性能FAIL且存在MISSING证据→FAIL；平台UNANSWERED→NOT ASSESSED；quick核心FAIL→保留FAIL及quick后缀。它们验证模型按Phase 5规则作判断，没有运行完整smoke Skill、游戏测试、性能测量或人工试玩。

## 原生界面和直接回执

- [原生问题调用、accepted回执及App实际答案](runtime-evidence/app-audit-458b4a0/question-interaction.json)：两题均使用title及字符串选项；投递回执后未提前写文件。答案来自App问题卡片的真实回复消息，没有以脚本伪造答案。
- [原生界面文本摘录](runtime-evidence/app-audit-458b4a0/ui-evidence.txt)：保存恢复结果、WAITING和两题卡片、下一步/发送状态、实际答案、QA输出及最终目标操作/断言结论。仅截取本次会话主区域，不导出其他项目聊天；未将无关窗口截图作为证据。
- [真实hook回执](runtime-evidence/app-audit-458b4a0/hook-receipts.json)：从本次会话原始工具输出和hook上下文提取三次拒绝、一次写后告警，包含实际cmd/workdir或patch输入，不依赖模型自报。
- [四回合命令与文件变更摘要](runtime-evidence/app-audit-458b4a0/turns.json)、[生成的QA计划](runtime-evidence/app-audit-458b4a0/qa-plan-generated.md)、[独立文件核对](runtime-evidence/app-audit-458b4a0/parent-checks.json)。原始详细记录保留在本地忽略目录 `.scratch/app-audit-458b4a0/`。

公开文本规范化测试路径和行尾留白；计划阅读副本使用等价Markdown硬换行。原始产物未修改，其SHA保存在独立核对记录中，不宣称阅读副本与原件字节一致。

界面部分更新没有立即显示，重新打开同一聊天、滚动到底部后核对到原生问题卡片及最终文本；未把后台完成状态直接当成界面显示成功。所有四回合最终均为completed。

## 来源、信任和恢复

验收前从458b4a0的Git对象同步1126份已提交框架/验收文件，运行后再次逐字节核对一致。保留隔离仓库自身的独立历史，没有重置或实际提交。项目配置解析为collaborative、workflow minimal、qa.level minimal；不表示本轮覆盖了全部模式和级别。

App目录与CLI目录不同，两项工具hooks最初为modified。用户在当前App项目的正常Review hooks入口审阅并允许PreToolUse/PostToolUse后，只读核对七项定义均enabled、trusted。未脚本写入全局信任、未使用绕过参数。七项受信任不等于七类事件都已真实触发。

结束时先恢复1006个原有跟踪文件、原检查点及原索引，哈希核对没有偏差；随后仅保留用户刚审阅的新hooks及运行依赖7文件，其中5项相对原隔离框架存在有意保留的跟踪差异。其他跟踪文件变化为0，原索引/检查点仍逐字节一致；游戏源码和既有故事未修改。明确的7文件例外列于[恢复核对](runtime-evidence/app-audit-458b4a0/parent-checks.json)，没有把这些例外写成整个隔离目录毫无变化。新生成的专用QA计划保留为验收产物。

本轮未重复共享框架全量测试；CLI与App本次变更的定向检查分别取得证据。真实PreCompact、全部角色流程、原生引擎、完整游戏smoke/试玩和远端CI仍未评估，不因本报告改成通过。
