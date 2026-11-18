# Codex 工作流运行约定

根 AGENTS.md 定义项目政策；工作流与角色读取当前 checkout 的资源。Skills 唯一目录为 `.agents/skills/`，角色规范源为 `.codex/agents/<role>.toml`。
名称相同的个人或插件 Skill 可能同时存在；工作流明确属于本项目时读取本仓库路径，避免误用另一个同名 Skill。
角色正文保留方式及旧客户端机制的对应边界见 `role-migration.md`。

## 工具与协作

工具调用以本轮实际 schema 为准。文件读取、搜索、补丁与终端执行使用当前可用工具；上游的 Read、Glob、Grep、Write、Edit、Bash 等名称仅描述动作，不构成 Codex 中存在这些同名工具的保证。
任务清单和执行记录保存到项目文件；没有任务管理工具时沿用文件清单，不编造 TaskCreate/TaskUpdate 调用。

子代理使用当前 Codex 委派接口。支持绑定角色时使用规范名；不支持绑定时读取对应 TOML 的 developer_instructions，传入有边界的任务简报。
委派前检查角色 TOML 是否声明模型家族。声明时按 `model-tiers.md` 解析当前型号，原生绑定与通用委派都传入解析结果。Skill 的会话模型同样按该规则解析。子代理沿用父会话的权限限制。写入同一文件的任务串行；并发额度不足时排队或串行，并说明实际参与角色。
返回合同包含产物路径、简要结果、证据与阻塞项；缺产物或工具失败不得记为完成，独立评审不能由实现者自查冒充。

## 提问与已有授权

先解析 `modes.automation`，默认 collaborative，按 `.agents/docs/automation-modes.md` 执行。
使用当前环境可用的提问工具；无工具时在对话中明确问题并等待必要回答。
已经明确批准的同一决定或变更范围沿用授权；必要问题被关闭、跳过或未回答不视为同意。
项目模式控制工作流停顿，不能放宽客户端 sandbox、账号权限或更高优先级指令。

## 配置与文件资源

配置必须显式执行 `.agents/scripts/yaml-helper.sh` 读取，检查实际退出状态与 notes，不依赖 ! shell 注入、$ARGUMENTS 展开或客户端专属环境变量。
`@file` 在上游表示自动导入；迁移后的流程通过明确路径按需读取，不假定 Codex 自动展开该语法。
改动文件前根据 `.agents/scripts/rule-routing.py` 的输出加载跨目录领域规则。
游戏引擎状态写入 project.yaml 与 docs/engine-reference，不修改根 AGENTS 的模型、提交或权限政策。
Python 工具统一通过 `bash .agents/scripts/python-run.sh <Python脚本及参数>` 执行；该入口复用真实解释器解析并优先遵循 `CGS_PYTHON`。正文里的 `python` 示例表示实际解释器，不授权调用 Windows 安装管理器别名。

## Explicit read-guard workflow contract

Before reading a whole text file under `design/`, `docs/architecture/` or
`production/session-state/`, the workflow must explicitly run the helper and
inspect its observations. This is a workflow instruction, not native Read-hook
enforcement: `.codex/hooks.json` does not intercept every file-read tool.

```bash
cgs_read_path='design/gdd/example.md'
bash .agents/scripts/read-guard.sh check "$cgs_read_path" --bounded no
```

Use the actual target path, relative to the project; for another project pass
`--root <project-directory>` to the helper. The `guard`, `threshold`, `watched`,
`size` and `bounded` TSV rows describe the check; exit 0 means observations were
emitted, not permission to read. If a `LARGE` row appears, do not perform the
whole-file read. Request the headings first:

```bash
bash .agents/scripts/read-guard.sh sections "$cgs_read_path"
```

Choose the needed section from those line numbers, then use a file-reading tool
with a real offset/limit or a terminal command with an explicit line range.
`check ... --bounded yes` describes that planned bounded read; it does not add
bounds to a later tool call. Images, PDFs and notebooks are outside this text
guard. With `guard off`, no `LARGE` row is emitted; retain an appropriate read
scope for the task.

If `size` is `-`, the file was not found; do not interpret the missing `LARGE`
row as a successful read. Nonzero exit, missing helper or unavailable Bash means
`NOT ASSESSED`: report the check that did not run and use a verified bounded read
when possible. If a necessary read still cannot be performed, keep the dependent
check incomplete. Record whether the explicit helper actually ran; its presence
in the repository alone is not evidence of runtime coverage.

## Windows PowerShell 的 Bash 入口

Skill 中的 Bash 代码块在 Bash 终端直接执行；Windows PowerShell 必须先从实际 Git 安装定位 Git Bash，不能裸调用可能指向 WSL 的 `bash`。不修改全局 PATH 或执行策略。

```powershell
$cgsGitExec = git --exec-path
if ($LASTEXITCODE -ne 0) { throw '需要已安装的 Git for Windows' }
$cgsGitRoot = Split-Path (Split-Path (Split-Path $cgsGitExec.Trim()))
$cgsBash = Join-Path $cgsGitRoot 'bin/bash.exe'
if (-not (Test-Path -LiteralPath $cgsBash)) { throw '未找到 Git Bash，检查未执行' }
& $cgsBash '.agents/scripts/yaml-helper.sh' resolve_config --keys automation
& $cgsBash '.agents/scripts/python-run.sh' '.agents/scripts/rule-routing.py' 'src/main.ts'
```

后续 Bash 示例均通过该实际路径执行，参数保持原样。显式目标目录的 `--root` 按对应脚本用法传递；yaml-helper.sh 要放在命令名前。若已定位的 Git Bash 被当前沙箱拒绝，只为必要的具体命令走当次 Codex 正常审批；审批不可用或被拒绝时报告未评估，不换用 WSL 或自动安装工具。

## 验收与恢复

共享 helper 输出观察结果，工作流依据当前模式和严格度作判定；必要检查失败或无法执行时不能交付完成。
脚本测试、真实客户端工作流和人工试玩分别记录；缺少工具或尚未实测的引擎行为写明未评估。
检查点使用 `production/session-state/active.md`，由 session-state.sh 更新；恢复时先核对当前任务、已完成步骤、决策与下一步，避免重复已完成工作。
参考图片使用工具实际提供的文件路径，调用 references-save.sh --file；只有粘贴编号时返回未评估，不读取私有客户端日志推测图片。
