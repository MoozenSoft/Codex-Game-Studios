# Codex 实际运行证据

此目录仅保存报告、命令输出、哈希、回放和截图，不包含生成游戏代码。`<probe>` 表示本任务创建的隔离 Git 项目，`%LOCALAPPDATA%` 表示当时使用的已安装运行时位置；仅规范化路径，不改变报告的结论或游戏文件哈希。

App 正常放行、写前拒绝、坏 JSON 后置提示、修复及原生角色追问见 app-fresh-result.md。追加日志修复后又执行了 App 只读复测，工具事件由 parent-audit.json 独立核对。

CLI 原型、首轮 grow 的真实失败和第二轮成功分别见三个 core 报告。首轮 ART 缺失已经由框架回归复现后修复；旧失败报告继续保留。第二轮对 hooks 哈希变化的 CONCERNS 由主会话同步日志实现解释，详见 parent-audit.json。

七类事件均有协议 fixture 测试；2026-11-18 追加的 App 与 CLI 证据也分别包含七类真实事件。PreCompact 的已测路径为 App 原生手动压缩，以及已安装 CLI 的原生 app-server 接口压缩 CLI 创建线程并用 exec resume 恢复。CLI 交互 TUI 与自动触发压缩仍未评估；历史报告保留其原时点结论。人工试玩、原生引擎编辑器及远端 Linux CI 不由这些证据证明通过。


提交458b4a0的CLI定向复验见 [运行报告](../cli-audit-458b4a0.md)及 `cli-audit-458b4a0/`。包含真实异步工具accepted后等待、明确QA输出组合、原生hooks拒绝及写后提示、独立文件/索引核对；smoke判定仅为模型决策fixture，未重验App或真实PreCompact。


提交458b4a0的App定向复验见 [运行报告](../app-audit-458b4a0.md)及 `app-audit-458b4a0/`。四回合均由App界面发起/回答；包括原生问题卡片、accepted后等待、明确输出组合和三种真实前置拒绝。BLOCKED是目标操作结果，PASS只指预期阻断断言。恢复及7文件适配器保留例外均有独立核对。


2026-11-18的App原生压缩与角色追加验证见 [续验报告](../app-continuation-2026-11-18.md)及 `app-continuation-2026-11-18/`。新增真实PreCompact/ContextCompaction、检查点恢复、qa-tester完整指令加载、实际模型/推理继承和同一代理无重读追问证据。旧报告保留原时点的未评估结论，当前登记以追加证据为准。

2026-11-18 CLI 全面验证见[运行报告](../cli-comprehensive-2026-11-18.md)及 `cli-comprehensive-2026-11-18/`。105/105 框架测试、3/3 框架浏览器测试、18/18 既有游戏测试，75 Skills/49 角色结构清单及 9 次真实 CLI 执行均有证据；包含七类真实事件、原生 qa-lead 与同代理追问、异步待答/明确选择、压缩恢复及中文空格工作树。逐组件完整流程和 TUI 等缺口显式保留，不能将结构全覆盖读成所有实际行为均已运行。

后续 TUI、自动压缩和工作树 hook 证据位于 `cli-gap-validation/`。TUI 显示压缩完成，同时拒绝项目的 PreCompact 输出。代码与回执对照、项目行为和引擎试验见 [CLI 缺口复验](../cli-gap-validation.md)。
