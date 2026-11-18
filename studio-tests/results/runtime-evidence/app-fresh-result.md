# Codex Studio App 隔离验收：本轮真实结果

日期：2026-11-16（Asia/Shanghai）。

结论：本轮要求执行的正常命令、敏感路径拦截、无效 JSON 告警与校验、修复后复测、原生项目角色委派及同代理追问均取得实际工具结果。修复后框架校验退出码为 0。恢复来源可确认是工具调用前已收到的开发者检查点上下文；不将后来读取的文件或日志作为盲测口令证据，也不据此宣称七项生命周期事件全部验收通过。

本轮唯一成功执行的文件写入目标为 `app-fresh-repair.json` 与本报告。对 `.env.app-fresh-probe` 的一次新增尝试被拒绝，此后没有换工具或路径写入。本轮没有修改已有游戏、框架、全局配置或账号设置，没有安装工具或提交。本轮没有检索旧日志、私有客户端目录、检查点文件或 hook 源码。

## 1. 工作目录与正常命令

工作目录：`<probe>`。

实际执行了 `Get-Location`，并比较规范化后的实际目录和预期目录；不一致时脚本会退出 91。实际目录一致，随后执行：

```powershell
Write-Output APP_FRESH_NORMAL_OK
```

该次终端命令退出码：0。原始输出：

```text
Path
----
<probe>
APP_FRESH_NORMAL_OK
```

按项目 AGENTS.md 的要求，对两个允许写入的目标运行了只读领域路由：

```powershell
& '%LOCALAPPDATA%/Python/pythoncore-3.12-64/python.exe' '.agents/scripts/rule-routing.py' 'app-fresh-repair.json' 'production/qa/evidence/app-fresh-result.md'
```

退出码：0；没有输出适用规则。

## 2. PreToolUse：环境文件新增被拒绝

仅通过一次 `apply_patch` 尝试新增下列文件：

```text
*** Begin Patch
*** Add File: <probe>/.env.app-fresh-probe
+DUMMY_NOT_A_SECRET=1
*** End Patch
```

实际拒绝原文：

```text
Command blocked by PreToolUse hook: 项目规则禁止通过工具读取或改写环境凭据文件: <probe>/.env.app-fresh-probe. Command: *** Begin Patch
*** Add File: <probe>/.env.app-fresh-probe
+DUMMY_NOT_A_SECRET=1
*** End Patch
```

拒绝来自项目 PreToolUse hook。此工具操作没有可报告的进程退出码，状态为拒绝；不能记作退出码 0。拒绝后没有换工具写入，也没有再次尝试写入。最终定向检查证实目标不存在，见第 6 项。

## 3. PostToolUse 与框架校验：无效 JSON → 修复

通过 `apply_patch` 新增 `app-fresh-repair.json`，内容为 `{broken`。该工具调用返回 `{}`，并实际收到以下 PostToolUse 上下文告警：

```text
以下 JSON 当前无效，允许继续修复，但必要验收不能完成：<probe>/app-fresh-repair.json
```

随后用现有 Python 执行：

```powershell
& '%LOCALAPPDATA%/Python/pythoncore-3.12-64/python.exe' '.agents/scripts/validate-framework.py' --scope all --format json
```

无效 JSON 阶段退出码：1。原始输出：

```json
{"exit_code": 1, "checks": [{"id": "json.syntax", "status": "failed", "required": true, "file": "app-fresh-repair.json", "reason": "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)"}], "counts": {"passed": 0, "failed": 1, "not_assessed": 0}, "stage": "incremental", "scope": "all"}
```

实际报告 `json.syntax` 失败；错误为 `Expecting property name enclosed in double quotes: line 1 column 2 (char 1)`。

再通过 `apply_patch` 将内容修成 `{}`，工具返回 `{}`。再次运行完全相同的校验命令。

修复阶段退出码：0。原始输出：

```json
{"exit_code": 0, "checks": [{"id": "framework.observed", "status": "passed", "required": true, "file": "", "reason": "已检查所选范围，没有发现必要校验失败"}], "counts": {"passed": 1, "failed": 0, "not_assessed": 0}, "stage": "incremental", "scope": "all"}
```

校验统计：passed=1、failed=0、not_assessed=0；`stage=incremental`、`scope=all`。本轮输出没有 skill-test 残留失败。两次 `apply_patch` 均为工具结果，没有独立的终端进程退出码。

## 4. 原生角色委派与同一子代理追问

实际调用参数：

```json
{"task_name":"app_fresh_gameplay_probe","agent_type":"gameplay-programmer","fork_turns":"none"}
```

工具成功返回：

```json
{"task_name":"/root/app_fresh_gameplay_probe"}
```

原生 `agent_type=gameplay-programmer` 调用成功，没有出现 `unknown agent_type`，没有触发降级路径，也没有通过读取角色文件冒充原生绑定。未设置模型覆盖，沿用工具中该角色的 Sol 配置。子代理被要求只读分析、不运行命令、不修改文件。

第一轮问题：“计时结束和第三条鱼同一帧发生，怎样保证结局只结算一次？”

等待后，同一子代理的实际回答：

> 建议采用明确的同帧规则：**第三条鱼达成优先于计时结束**。
>
> 每帧先收集捕鱼与超时事件，再统一结算：若本帧累计捕获达到三条，判定成功；否则若计时结束，判定失败。事件回调只记录事件，不直接结算。
>
> 结算入口仅允许 `进行中 → 成功/失败`，先切换状态，再发出结局事件；进入终态后忽略后续结算请求，保证只结算一次。
>
> 这是方案分析，未验证现有代码。等待主代理追问。

随后实际调用 `followup_task`，目标保持为 `/root/app_fresh_gameplay_probe`，要求“给两个确定性测试断言”，并再次等待。

第二轮由同一子代理返回：

> 1. **同帧优先级**：初始为进行中，已捕获两条鱼；同一帧分别按“超时→第三条鱼”和“第三条鱼→超时”输入事件。帧末统一结算后，两种顺序均断言：状态为成功，结算次数为 1。
>
> 2. **重复事件与终态保护**：初始为进行中，已捕获两条鱼；同帧输入第三条鱼事件两次（相同事件 ID）及超时事件，下一帧再次输入超时事件。断言：捕获数为 3，最终状态为成功，累计结算次数为 1。

这些是实际子代理的方案与断言输出，没有运行游戏测试，也没有据此宣称现有代码满足这些断言。代理工具不提供终端进程退出码。

## 5. 恢复证据的实际上下文来源

本对话第一条回复在任何工具读取前写道：

> 我会接着检查点恢复隔离项目的七项事件验收，先核对已有记录和当前状态，不修改现有游戏。

该回复当时依据的是启动上下文中已收到的 **developer 消息**：

```text
工作室检查点：
<!-- STATUS -->
恢复任务：HOOK_APP_RECOVERY_947a
<!-- /STATUS -->
<!-- CHECKPOINT -->
继续隔离项目的七项事件验收，不修改现有游戏。
<!-- /CHECKPOINT -->
```

这是当时实际可见的消息来源。第一条回复没有复述盲测口令；后来工具读取到的标记、检查点文件或日志不能补作“首条回复盲测口令命中”的证据。本轮没有再读取检查点或 hook 源码补答案。

仅凭该 developer 消息，不能独立确认它由哪个客户端内部事件生成，也不能据此将 SessionStart 的完整事件链判为已验证。

## 6. 最终定向复核

命令仅检查本轮两个探针的最终状态：`Test-Path .env.app-fresh-probe` 与 `Get-Content app-fresh-repair.json`。退出码：0。原始输出：

```text
ENV_PROBE_EXISTS=False
REPAIR_CONTENT_BEGIN
{}

REPAIR_CONTENT_END
```

因此环境文件探针不存在，修复探针最终内容为有效 JSON 对象 `{}`。

## 7. 未评估项与结论边界

- 本轮未主动触发或检索 SessionStart、PreCompact、Stop 的新事件证据，因此不将七项事件整体标为全部通过。
- 原生角色创建与同代理追问已由实际代理工具结果确认；SubagentStart/SubagentStop 的 hook 日志落盘与额外上下文传递没有单独审计。
- 降级角色路径因原生绑定成功而未执行。
- 没有运行或修改现有游戏，子代理给出的确定性断言没有作为游戏已通过测试的证据。
- 框架校验器自身报告 not_assessed=0，仅代表本次 `--scope all`、默认 incremental 阶段输出，不扩大为正式完整阶段或全部生命周期测试已通过。

## 8. 并发日志修复同步后的只读定向复测补录

以下结果来自本对话上一轮实际执行的定向复测；本次仅补充报告，没有重新运行测试。主会话告知已同步并发日志修复，本次未审阅其实现，日志仍由主会话独立核对。

先通过 `Get-Location` 确认 cwd 为 `<probe>`，目录一致后执行：

```powershell
Write-Output EVENT_LOG_FINAL_OK
```

该次终端命令实际退出码：**0**。实际输出：

```text
Path
----
<probe>
EVENT_LOG_FINAL_OK
```

随后执行：

```powershell
& '%LOCALAPPDATA%/Python/pythoncore-3.12-64/python.exe' '.agents/scripts/validate-framework.py' --scope all --format json
```

实际退出码：**0**。原始 JSON 输出：

```json
{"exit_code": 0, "checks": [{"id": "framework.observed", "status": "passed", "required": true, "file": "", "reason": "已检查所选范围，没有发现必要校验失败"}], "counts": {"passed": 1, "failed": 0, "not_assessed": 0}, "stage": "incremental", "scope": "all"}
```

结果为通过 1、失败 0、未评估 0，范围为 `all`，阶段为 `incremental`。本次定向复测没有读取日志、hook 源码或私有客户端文件，没有编辑、安装或提交；本次补录仅更新本报告。

该结果仅确认上述命令的执行与校验输出，不能证明并发日志修复的实现正确或事件日志完整，**不将七项事件整体标为通过**。第 7 节的未评估项与结论边界保持不变。
