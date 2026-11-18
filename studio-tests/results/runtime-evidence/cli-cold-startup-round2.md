# CLI 新 clone 冷启动验收：第二轮

日期：2026-11-17。范围：同一个独立 clone 的只读配置 helper 与独立 Sol 子代理首次、续作验收。本轮配置 helper 成功；不绑定原生角色的独立委派与同一代理续作成功。原生角色绑定、hooks 信任和触发仍未评估，不能据此宣称整个客户端启动或游戏验收全部通过。

首轮 `production/qa/evidence/cli-cold-startup.md` 保留原文及其真实失败结论。第二轮成功不追溯覆盖首轮裸 Bash 失败，也不把降级委派说成原生绑定成功。

## 初始身份与已知同步

- cwd / Git 根：`<probe>/app-web-acceptance`。
- 分支：`app-acceptance`。
- HEAD：`cc1076080a16154af378fa5082a089b69169837e`。
- 初始 HEAD tree：`2eed3d73899155cd7a4aba4410143c57d32248f6`。这是提交 tree，不代表工作区没有同步改动。
- 初始状态有四个已修改文件与首轮未跟踪报告；第二轮报告初始不存在。

```text
 M .agents/docs/codex-runtime.md
 M .agents/docs/setup-requirements.md
 M .agents/scripts/page-shot.sh
 M .agents/scripts/story-status.sh
?? production/qa/evidence/cli-cold-startup.md
```

按用户明确说明，上述两个文档的 Windows 入口更新及两个 Bash 脚本物理行尾 LF 化是主迁移会话已知同步，不是本验收代理上轮或本轮修改框架。实际 `git diff` 显示运行约定增加 Windows 段 15 行、环境说明增加 1 行；两个脚本 `git diff --numstat` 无文本差异，实际字节 CRLF 数均为 0。环境说明文档仍有 CRLF，不将脚本 LF 化误写为所有文档 LF 化。

只读字节核验得到下列 SHA-256，作为本轮写入前保护基线：

| 路径 | SHA-256 |
| --- | --- |
| `.agents/docs/codex-runtime.md` | `f23c9579ce865b2b7701b1a7f9d4406c435ac097c21a6690e64879412355ecbb` |
| `.agents/docs/setup-requirements.md` | `6a99e6be5939c2ca33fe7916c537353d700416c48d006ec376efacccda9dc64b` |
| `.agents/scripts/page-shot.sh` | `81a3f1455d5dfe16f579e3ac6ac827db6156301853354abb732478db713e7ed1` |
| `.agents/scripts/story-status.sh` | `18e287fe5b22149899033a8d25d925ff2daf821a707a7d0c783bc0d38c9e7637` |
| `production/qa/evidence/cli-cold-startup.md` | `28000caca11f5d973aafb405959db49b74b77aed4626b08a8139dd4f452e113b` |

## 本项目资源与 Windows 入口

实际应用的 Skill：`.agents/skills/project-settings/SKILL.md`，已用 UTF-8 完整读取。主代理同时读取 `.agents/docs/codex-runtime.md`、`.agents/docs/setup-requirements.md`、`.agents/docs/automation-modes.md`、`.agents/docs/config-resolution.md`、`.agents/docs/coordination-rules.md` 和 `.codex/agents/qa-tester.toml`。保留项目资源来源，没有读取或调用全局 Skills、插件、MCP、全局角色或私有会话。

`.codegraph` 存在性检查为 False，因此没有使用 CodeGraph，也没有调用 MCP。配置查询实际执行 `.agents/scripts/yaml-helper.sh`，没有用静态 YAML 判定冒充成功输出。

现有环境变量原样保留：

```text
CGS_PYTHON=%LOCALAPPDATA%/Python/pythoncore-3.12-64/python.exe
```

没有调用裸 `python`、`py`、安装器或安装管理命令。按新版 Windows 段实际执行：

```powershell
$cgsGitExec = git --exec-path
if ($LASTEXITCODE -ne 0) { throw 'Git unavailable' }
$cgsGitRoot = Split-Path (Split-Path (Split-Path $cgsGitExec.Trim()))
$cgsBash = Join-Path $cgsGitRoot 'bin/bash.exe'
if (-not (Test-Path -LiteralPath $cgsBash)) { throw 'Git Bash unavailable' }
Write-Output $cgsBash
& $cgsBash '.agents/scripts/yaml-helper.sh' resolve_config --keys automation,automation_always_ask,workflow,review_mode,team.size
```

`git --exec-path` 输出 `D:/Program Files/Git/mingw64/libexec/git-core`，解析出的真实 Bash 为 `D:\Program Files\Git\bin\bash.exe`。首次默认沙箱调用退出 **1**，仅打印该路径，未取得 helper 输出；工具没有返回更具体的拒绝文本，不能补写不存在的报错。

随后按用户已批准范围通过工具正常 `require_escalated` 审批执行同一具体只读命令。审批成功，命令退出 **0**：

```powershell
& 'D:/Program Files/Git/bin/bash.exe' '.agents/scripts/yaml-helper.sh' resolve_config --keys automation,automation_always_ask,workflow,review_mode,team.size
```

真实输出：

```text
=== CCGS Config (resolved: local->yaml->legacy->default; use as-is) ===
review_mode: solo (rigor:minimal)
automation: collaborative (default)
workflow: minimal (rigor:minimal)
team.size: individual (rigor:minimal)
automation_always_ask: scope_changes, file_deletions, schema_changes (default)
=== end ===
```

没有 notes 警告。模式是本独立项目的 `collaborative` 默认，不是父目录或旧游戏的自主模式。本轮报告和只读委派已由用户明确授权，沿用授权无需重复确认。

按 Skill 的 view-one 要求又分别执行三个独立 helper 命令，每条均经正常审批、退出 **0**：

```powershell
& 'D:/Program Files/Git/bin/bash.exe' '.agents/scripts/yaml-helper.sh' resolve_setting modes.automation
& 'D:/Program Files/Git/bin/bash.exe' '.agents/scripts/yaml-helper.sh' get_yaml_key project.yaml modes.automation
& 'D:/Program Files/Git/bin/bash.exe' '.agents/scripts/yaml-helper.sh' is_locally_overridable modes.automation
```

输出依次为 `collaborative<TAB>default`、空输出、`0`。`project.local.yaml` 实际不存在，因此跳过其读取；`modes.automation` 可本地覆盖，本轮无本地覆盖，来源为 default。RESERVED 标题按项目 `effects-map.md` 实际读取，当前键不属于其中项目。没有执行配置写入。

## 真正独立 Sol 子代理：首次返回

当前 `collaboration.spawn_agent` 的真实 schema 只有 `task_name`、`message`、`fork_turns`、`model`、`reasoning_effort`，没有 `agent_type`。因此使用项目运行约定明文支持的角色文本降级，不声称原生角色绑定成功。

实际调用参数：`task_name=round2_qa_tester`、`fork_turns=none`、`model=gpt-6.1-sol`、`reasoning_effort=medium`。工具成功返回独立代理标识 `/root/round2_qa_tester`。这是委派工具返回，不是终端进程，没有命令退出码。`fork_turns=none` 使其不继承父会话历史；职责来源仍共享当前客户端权限边界，不宣称新增权限沙箱。

简报明确限定：仅从当前目录 `.codex/agents/qa-tester.toml` 的 `developer_instructions` 及本项目必读资源取得角色规则；实际读取后回答“1 个必要测试失败，其余 9 个通过，故事能否关闭”。禁止全局 Skills、插件、MCP、全局角色、私有会话；保持 Sol，只读、不安装、不提交、不修改全局设置、不绕过 hooks。传入了上述父任务真实 helper 输出，明确不能冒称子代理自行执行。无文件写入权，产物仅为对话返回。

实际收到同一独立子代理首次 FINAL_ANSWER（下列为原文）：

> 不能关闭故事。**BLOCKED：存在 1 个必要测试失败**；其余 9 个通过不能抵消该门禁失败，也不能以 90% 通过率认定完成。
>
> 实际读取的角色来源是当前 checkout 的 `.codex/agents/qa-tester.toml` 中的 `developer_instructions`，采用读取角色指令的降级方式，未声称原生角色绑定成功。已读取资源：
>
> - `AGENTS.md`
> - `.agents/docs/codex-runtime.md`
> - `.agents/docs/coordination-rules.md`
> - `.agents/docs/automation-modes.md`
> - `.agents/docs/model-tiers.md`
> - `.agents/rules/test-standards.md`
>
> 判断证据：
>
> - 根 `AGENTS.md` 明确：必要失败或必要检查无法执行时，不能关闭相应故事或阶段。
> - `codex-runtime.md` 明确：必要检查失败或无法执行时，不能交付完成。
> - qa-tester 角色要求必要测试证据满足对应门禁；禁止为赶进度跳过测试步骤。
>
> 配置引用父任务已实际取得的 helper 输出：`automation=collaborative`、`workflow=minimal`、`review_mode=solo`、`team.size=individual`。这不是我自行执行 helper 的结果；这些设置不豁免必要测试失败。
>
> 后续应保留故事未完成状态，记录失败证据并交由负责人安排修复；修复后复测失败项及受影响路径。qa-tester 不自行修复缺陷或批准发布。
>
> **CONCERNS：**未提供具体测试、故事类型及失败日志，无法评估根因、严重程度和回归范围。
>
> **产物路径：**无文件，仅本次对话返回。本结论只是给定场景判断；我没有执行这 10 个游戏测试，也没有修改任何文件。

## 同一子代理续作返回

首次返回后才实际调用 `collaboration.followup_task`，目标为同一个 `round2_qa_tester`，问题为“必要检查缺环境但可选检查通过时怎么判断，故事能否关闭”，要求区分 FAIL/PASS/NOT ASSESSED、保持原角色来源与只读边界。工具正常接受（没有终端退出码），随后实际收到同一 `/root/round2_qa_tester` 的第二次 FINAL_ANSWER。没有用父代理判断冒充其回答。

续作原文：

> 必要检查因缺少环境而未执行，应记 **NOT ASSESSED（未评估）**。故事不能关闭，状态为 **BLOCKED／未完成**；可选检查通过不能抵消必要检查缺失。
>
> 区分如下：
>
> - **PASS**：实际执行检查，结果满足要求。
> - **FAIL**：实际执行检查，观察到不满足要求。
> - **NOT ASSESSED**：环境缺失导致检查未执行，或执行过程受阻，未取得可判定结果。启动命令报错应单独记录为执行失败，不能据此认定被测功能失败。
>
> 角色来源沿用已实际读取的本项目 `.codex/agents/qa-tester.toml` 中的 `developer_instructions`，未原生绑定角色。依据已读取的 `AGENTS.md` 与 `.agents/docs/codex-runtime.md`：必要检查无法执行时，不能关闭对应故事或交付完成；未实测行为必须明确标为未评估。qa-tester 角色同样要求如实报告未执行检查。
>
> **BLOCKED：**必要检查缺少执行环境，尚无满足门禁的证据。应补齐环境后执行必要检查，取得合格证据再判断关闭。
>
> **CONCERNS：**尚未提供缺失环境及具体检查信息，无法确定恢复步骤。本次仅判断给定场景，未实际执行测试。
>
> **产物路径：**无文件，仅本次对话返回；未修改文件、安装工具或绕过 hooks。

两次场景判断不是实际执行十个游戏测试，也不代表关闭了任何真实故事。子代理已实际返回两次，不存在待回答的续作。

## 命令与退出码补充

除上文逐条列出的配置命令外，本轮执行记录如下。PowerShell 批次的退出码是整个批次返回值，不把混合批次退出 0 当成每个内部动作都成功。

| 实际命令或批次 | 退出码及观察 |
| --- | --- |
| `Get-Location; git status --short; git rev-parse HEAD; git rev-parse 'HEAD^{tree}'; git --exec-path` 及首次读取 Skill、运行文档、首轮报告 | 0；默认编码造成部分中文显示乱码，随后用 UTF8 重读，不改源文件 |
| `Get-Content -Encoding UTF8` 读取运行文档、配置文档、角色；检查 `Env:CGS_PYTHON`、`.codegraph`、`git diff --stat`；尝试 `Get-FileHash` | 1；`Get-FileHash` 在当前 shell 不可用，未完成该项；改用已安装 Python 标准库计算哈希 |
| Python 绝对路径执行 `.agents/scripts/rule-routing.py production/qa/evidence/cli-cold-startup-round2.md`，读取协作约定，`rg` 检查校验入口 | 批次 0；routing 无匹配规则、无输出 |
| UTF8 重读完整 Skill、校验入口、routing、helper 前段，`rg -n ... .agents/scripts/framework*` | 1；PowerShell 下该通配路径没有被展开，rg 报 OS error 123；随后明确指定 `framework_validation.py` 读取成功 |
| 首次 Python `-c` 哈希命令（PowerShell 单引号包裹、内部双引号） | 1；原生参数传递使内部双引号丢失，SyntaxError；没有写文件，改为外层双引号、Python 内部单引号后成功 |
| 修正后 Python `-c` 计算五个文件 SHA-256、CRLF 计数及 round2 存在性；`rg` 明确文件、`Select-String` RESERVED、`Test-Path project.local.yaml` | 0；得到上文真实哈希与文件状态 |
| Python `-c` 通过 `os.walk` 与 `hashlib.sha256` 读取工作区所有文件（排除 `.git` 及本轮报告），JSON 返回工具内存 | 0；不落盘，作为写后完整字节对照 |
| `Get-Content -Encoding UTF8 .agents/scripts/framework_validation.py` | 0；确认校验入口只读，使用 `-B` 防止导入生成字节码文件 |
| Python 绝对路径 `-B .agents/scripts/validate-framework.py --scope all --format json` | 0；默认 incremental 阶段，静态框架检查通过；不等同于全部客户端或游戏测试 |
| `git rev-parse --show-toplevel`、`git branch --show-current`、HEAD/tree、`git status --porcelain --untracked-files=all`、文档 diff、脚本 numstat | 批次 0；写报告前身份一致，只有上述已知变更；Git 提示 setup-requirements.md 的 CRLF 将在未来 Git 操作时归一化，本轮没有执行归一化 |

框架校验真实 JSON 摘要：`exit_code=0`，`stage=incremental`，`scope=all`，`passed=1, failed=0, not_assessed=0`；`json_files=35, toml_files=50, skills=75, skill_resources=206, source_total=743, active=733, retired=10, pending=0, native_components=17`。这是静态扫描结果，没有运行 `--stage complete`，不据此宣布完整迁移验收通过。

## 未评估项与交付边界

hooks 信任与真实触发仍单列 **未评估**：没有本轮客户端信任事件或触发证据，没有手工运行 hooks 绕过信任。原生角色绑定仍因接口缺少 `agent_type` 而未评估；本轮验证的是项目约定的独立代理降级路径。App、浏览器、Web 游戏输入、引擎运行、远端 CI 及人工试玩均不在本轮实测范围。

唯一授权写入为本报告。未安装、未联网发布、未提交、未改分支/index/HEAD、游戏、项目或全局配置、全局 PATH、执行策略。未写 session-state、决策日志或其他产物。

本报告由 `apply_patch` 直接写入可读 UTF-8 中文；写后用 `Get-Content -Encoding UTF8` 实际回读，并用 Python 严格 UTF-8 解码及基线字节比较核验，最终结果见后续复核记录。

最终复核实际完成：UTF8 全文回读、Python 严格解码及 Git 复核批次退出 **0**；`strict_utf8=True`，不含替换字符 U+FFFD。工作区文件哈希快照复核退出 **0**：排除 `.git` 和本报告，前后均为 **933** 个文件，`changed=[]`、`deleted=[]`。因此首轮报告及四个主会话同步文件字节均未改变，也没有新增其他文件。HEAD 与初始 tree 一致，最终 status 相比初始仅增加 `?? production/qa/evidence/cli-cold-startup-round2.md`。`apply_patch` 两次均正常完成，无终端退出码；本段追加后再次 UTF8 回读。
