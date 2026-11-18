# Codex 工作流配置解析

游戏项目配置位于 `project.yaml`；个人覆盖位于被 Git 忽略的 `project.local.yaml`。
客户端模型、沙箱、工具连接和 hooks 由 `.codex/` 与用户的 Codex 设置管理。

工作流需要配置时显式执行解析器，并读取实际输出：

```text
bash .agents/scripts/yaml-helper.sh resolve_config --keys automation,workflow,review_mode
bash .agents/scripts/yaml-helper.sh --root <project-directory> resolve_config --keys automation
```

不依赖 Skill 内的 shell 注入或客户端专有环境变量。需要 Git Bash/Bash 和可运行的 Python 3；缺少解释器时直接入口退出 2，调用者记录“未评估”并处理必要检查缺失。

共享工具使用 Python 3.11+（包含标准库 tomllib）。可用 `CGS_PYTHON` 指定实际解释器绝对路径；显式路径无效就报告未评估，不静默回退。
Windows 优先检查已安装运行时目录，跳过 PyManager、WindowsApps 与 Python/bin 安装器入口；不要用 `py list` 或安装管理器定位运行时，以免探测产生自动更新或下载副作用。

## 取值顺序与来源

1. `project.local.yaml`：只对个人覆盖白名单内的键生效。
2. `project.yaml`：项目共享的显式值。
3. 既有状态镜像：`modes.review_mode` 对应 `production/review-mode.txt`，`project.stage` 对应 `production/stage.txt`。
4. `modes.rigor` 展开：只对严谨程度管理的六项设置生效。
5. 文档默认值。

枚举值无效时跳过该值继续解析，并在 `notes:` 中说明。重复配置块沿用上游的合并读取行为并给出提示；不要通过写入重复键处理配置变更。
个人文件中不在白名单内的键会被报告，而不会静默改变共享配置。

每行保留取值来源，例如 `automation: collaborative (default)` 或 `automation: autonomous (project.local.yaml)`。
读写个人白名单必须同步维护；引擎等决定项目产物的设置由全员共享。

## 默认值和三种协作模式

`modes.automation` 默认 `collaborative`，可以为 `guided` 或 `autonomous`；它独立于严谨程度和团队规模。
具体流程保留各模式的确认与记录行为，遵循会话明确授权和客户端权限。
`modes.automation_always_ask` 默认包含 `scope_changes`、`file_deletions`、`schema_changes`。

`modes.rigor` 默认 `minimal`；显式配置的子项优先，不应在模板中预填六个子项并遮蔽展开结果。

| rigor | workflow | docs.density | qa.level | story_granularity | review_mode | team.size |
| --- | --- | --- | --- | --- | --- | --- |
| minimal | minimal | terse | minimal | coarse | solo | individual |
| standard | standard | balanced | standard | balanced | lean | individual |
| full | full | thorough | full | fine | full | studio |

## 项目定位与接口

显式 `--root` 优先。没有显式根目录时，当前目录包含 `project.yaml` 或 `project.local.yaml` 就使用当前目录，保留嵌套项目语义；否则使用解析器文件所在 checkout 的根目录。
不向父目录寻找另一份项目配置，也不读取 `CLAUDE_PROJECT_DIR` 等上游客户端变量。

`resolve_config` 保留既有配置块格式；`resolve_setting` 保留值与来源的 TSV 输出。
独立读取入口还包括 `get_yaml_key`、`get_effective_yaml_key`、`validate_yaml_enum`、`validate_enum_value`、`is_locally_overridable`。
未知命令或无效 `--root` 退出 2；校验查询保留各自的状态码。

`is_always_ask_category` 和 `log_decision` 仅作为 source 后的 Bash 函数提供，不属于上述直接子命令。在目标项目目录 source 本 checkout 的 helper；若项目与 checkout 不同，先进入目标项目，再用 helper 的绝对路径 source。不要把 `--root` 当成 source 参数。

```bash
source .agents/scripts/yaml-helper.sh
if is_always_ask_category scope_changes; then
  printf '%s\n' 'Required category: resolve the decision using current authorization.'
fi
# Only after this decision was actually made:
log_decision "next-step" "Choose next approved task" "Task A; Task B" "Task A" "Its dependencies are complete" "workflow_routing"
```

类别查询返回 0 为命中、1 为未命中，不自动提问或批准。`log_decision` 必须接收六个位置参数：Skill、Decision point、Options considered、Chosen、Reason、Category；检查退出状态和 `production/session-logs/decision-log.md` 中的实际记录。记录失败不等于授权失效，但必须报告日志未落盘，不能伪造证据。

引擎目录和默认命令来自 `../engines/engines.tsv`，由 `../scripts/engine-row.awk` 读取。
尚未写入项目配置的旧格式技术约定见 [technical-preferences.md](technical-preferences.md)；其中供解析器读取的英文标题与字段保持原拼写。
代码根和测试根均排除 `.agents/`、`.codex/` 等框架目录；无法确定游戏根目录时返回未设置或无效，不猜测扫描目标。

## 当前验证边界

配置解析器已有真实脚本测试，覆盖默认值、本地覆盖、无效枚举、严谨程度、中文空格路径、子目录启动、显式根目录和框架目录拒绝。
其余共享脚本、正式 Skills 与客户端集成仍按迁移清单逐批启用；本解析器的测试结果不代表整套工作室已完成迁移。
