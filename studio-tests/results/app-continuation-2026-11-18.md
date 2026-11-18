# Codex App 压缩与角色续验

2026-11-18，继续验证458b4a0。沿用既有App隔离项目；模型保持用户选定的gpt-6.1-sol/high。App父子线程的来源及后端版本见[结构化汇总](runtime-evidence/app-continuation-2026-11-18/summary.json)。本轮补足手动压缩与单个QA角色路径，不重跑此前15项或共享框架全量。

## 实际结果

| 场景 | 证据与结论 |
| --- | --- |
| App原生手动压缩 | 在原生斜杠菜单选择“压缩”；界面当时显示上下文使用约10%。真实PreCompact于00:04:53 UTC触发；00:06:13记录compacted、完成的ContextCompaction及task_complete |
| 检查点保留 | 压缩前后专用active.md的SHA一致，没有自动覆盖既有授权边界 |
| 压缩后恢复 | 下一次App请求实际读取active.md，正确返回新的Marker、Stage、Pending和只读授权范围；界面核对到“上下文已压缩”及恢复回复 |
| 本次SessionStart | 恢复请求记录SessionStart，并在本线程实际收到带新检查点的开发者上下文；随后又按要求读文件复核。两种证据分别保存，不把读文件等同于自动注入，也不保证每次压缩都有相同启动事件 |
| 原生角色绑定 | 新App会话实际调用spawn_agent，agent_type为qa-tester，无降级；子线程agentRole为qa-tester，父子关系匹配。子代理首次工具调用前的指令上下文包含当前TOML完整developer_instructions，源正文SHA另存 |
| 模型与推理继承 | 委派未传model或推理强度覆盖；实际父子线程元数据均为gpt-6.1-sol/high，不靠代理自报 |
| 同代理追问 | followup_task指向原规范任务名，子线程ID不变且两回合均完成。第二回合无命令/文件工具调用，仍正确返回首轮标记及计数3 |
| 只读与恢复 | 运行后1126份已提交框架文件逐字节未变；结束恢复1006份原有跟踪文件、原检查点和原索引，无偏差 |

角色探针只生成三个QA用例草案，再回答一个基于保留上下文的规则问题；没有执行这些功能用例或游戏实现。当前接口没有正常关闭代理操作，任务已完成且没有继续调用，保留结束态记录。

## 七类真实事件

本轮仅统计准备时保存的日志字节偏移之后的真实事件：

| 事件 | 数量 |
| --- | ---: |
| PreCompact | 1 |
| SessionStart | 2 |
| PreToolUse | 16 |
| PostToolUse | 16 |
| Stop | 3 |
| SubagentStart | 1 |
| SubagentStop | 2 |

这次七类均有实际日志，PreCompact另有原生压缩记录佐证，角色事件有父子活动及返回结果对应。它证明本App版本、该受信任目录和受控路径，不代表所有输入形状或每个事件处理分支都已验证。没有手动调用dispatch.py制造客户端事件，也没有通过CLI发起模型或压缩任务。

## 证据

- [压缩及恢复证据](runtime-evidence/app-continuation-2026-11-18/compaction-proof.json)、[恢复回复](runtime-evidence/app-continuation-2026-11-18/recovery.md)、[真实事件增量](runtime-evidence/app-continuation-2026-11-18/events.jsonl)。不导出压缩摘要或隐藏推理，仅记录完成事件与本次受控检查点上下文。
- [角色绑定及源正文指纹](runtime-evidence/app-continuation-2026-11-18/role-binding.json)、[父子元数据](runtime-evidence/app-continuation-2026-11-18/role-thread-metadata.json)、[委派及追问参数](runtime-evidence/app-continuation-2026-11-18/role-calls.json)。委派正文在协议中是不透明数据，公开记录省略正文，不尝试解密。
- [首轮角色答复](runtime-evidence/app-continuation-2026-11-18/qa-role-first.md)、[追问答复](runtime-evidence/app-continuation-2026-11-18/qa-role-followup.md)、[同代理及无重读核对](runtime-evidence/app-continuation-2026-11-18/role-followup-proof.json)、[专用输入](runtime-evidence/app-continuation-2026-11-18/role-input.md)。
- [App界面摘录](runtime-evidence/app-continuation-2026-11-18/ui-evidence.txt)、[来源与恢复核对](runtime-evidence/app-continuation-2026-11-18/restoration.json)。窗口转场后曾遇无障碍树缓存旧页，重建连接并核对当前截图后才继续；没有使用旧页索引替代新会话状态。只公开本次主区域文本，规范化测试路径及行尾留白。

运行文件临时从458b4a0的Git对象同步，保留隔离仓库原历史。结束后全部恢复本轮准备时的原件；上一轮已审阅的七文件适配器原本就在该基线中，本轮不增加新的恢复例外。旧报告的“PreCompact未评估”保留当时状态，当前登记以本次追加证据为准。

CLI真实PreCompact、自动压缩路径、全部49个角色及其完整工作流、原生引擎、完整游戏试玩和远端CI仍未评估。本轮只更新验证登记和说明，没有新增运行规则或实现补丁。


## 登记校验

更新当前hooks说明、PreCompact/qa-tester运行证据和App矩阵链接后，共享Codex合同8项、迁移清单8项定向检查通过；项目要求的complete校验退出0。源清单仍为743项、733 active、10 retired、pending=0，native_components=20。仅补必要定向校验，未重复共享全量；没有更改hooks实现、角色正文或模型配置。
