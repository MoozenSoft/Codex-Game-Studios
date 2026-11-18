# Codex Game Studios

面向游戏开发的 Codex 工作室框架，基于 [Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) 改造，保留设计、架构、开发、测试与交付方法。
共享工作流唯一目录为 `.agents/skills/`，专业角色位于 `.codex/agents/`；本项目只适配 Codex。

## 开始使用

1. 克隆本仓库或用它作为游戏项目模板：

   ```text
   git clone https://github.com/MoozenSoft/Codex-Game-Studios.git my-game
   cd my-game
   ```

2. 准备 Git for Windows/Git Bash（Windows）、Python 3.11+ 与 Codex。浏览器原型检查需要 Chrome、Edge 或 Chromium；grow 为 Web 工程还需要与 scaffold 声明匹配的 Node.js。
3. 在 Codex App 打开本地项目，或在项目根运行 `codex`。PowerShell 包装脚本被执行策略拒绝时可使用 `codex.cmd`，不需要为此自动修改系统执行策略。
4. 信任你已经检查的项目目录，并在正常 Review hooks/Settings → Hooks 或 CLI `/hooks` 中检查本项目定义。配置文件存在不表示 hooks 已运行。
5. 使用 `$start` 选择入口，或 `$prototype` 描述游戏。个人或插件有同名 Skill 时，明确使用本仓库 `.agents/skills/<name>/SKILL.md`。

模型与推理强度沿用用户的会话选择，子代理默认继承父会话；角色与项目配置不固定模型，委派时省略模型覆盖参数。
当前最小机制验收起点为 Windows CLI 0.169.0、App 26.1111.2228.0。完整流程实测范围见 [验收状态](studio-tests/results/codex-adaptation-status.md)，不由版本号推断兼容。

## 从想法到游戏

- **先玩到原型**：需求与问答 → `design/game-brief.md` → `prototypes/<name>/` → 脚本输入检查与截图 → 交接卡。人工未试玩就写明未评估，不自动决定 PROCEED。
- **继续修改**：明确 Keep、Avoid 与本次变化，保留已批准决定；按相同 seed 检查行为变化。
- **grow**：用户选择成为真实 Web 工程后保留原型，创建 TypeScript、数据文件、测试与构建，再做同 seed 对比。
- **按功能迭代**：一次实现一个明确功能；需要 Story 路径时使用 `$create-stories`、显式 `$dev-story` 与 `$story-done`。
- **工作室流程**：设计、ADR、TR、团队专业管线、sprint、QA、发布与运营按项目规模启用，目录与条件由 `.agents/docs/workflow-catalog.yaml` 维护。

Godot、Unity、Unreal 的规则、角色、配置与脚本属于迁移范围；真实编辑器、构建和游戏运行单独留证，未执行就不承诺已通过。

## 配置与协作

`project.yaml` 是游戏项目共享配置；`project.local.yaml` 保存允许的个人覆盖并被 Git 忽略。客户端默认值与 hooks 位于 `.codex/`。
`modes.rigor` 控制产物严谨度，默认 minimal；`modes.automation` 独立控制协作，默认 collaborative。

| 模式 | 行为 |
| --- | --- |
| collaborative | 呈现选择和草稿，按批准范围执行；默认模式 |
| guided | 重大决定询问，细节继续；新文件保留确认约定 |
| autonomous | 自行选择并记录一般决定；配置的必须询问类别仍等待回答 |

三种模式都复用已有明确授权，问题被跳过不视为同意；它们不能扩大客户端权限。
配置解析、模式与角色协作分别见 [配置解析](.agents/docs/config-resolution.md)、[协作模式](.agents/docs/automation-modes.md)、[运行约定](.agents/docs/codex-runtime.md)。

## 验证与能力状态

完整框架检查在开发虚拟环境中执行，先安装固定测试依赖：

```text
python -m pip install -r studio-tests/requirements.txt
python -m unittest discover -s studio-tests/automated -p 'test_*.py' -v
python studio-tests/validate-yaml.py
python .agents/scripts/validate-framework.py --scope all --stage complete --format json
```

需要实际解释器；可设置 `CGS_PYTHON` 为绝对路径。Windows 工具优先寻找已安装 Python，跳过可能触发更新或下载的安装器入口。
测试可通过 `CGS_TEST_BASH` 指定 Git Bash。领域文件规则用 `python .agents/scripts/rule-routing.py <paths...>` 选择并读取。
PyYAML 仅用于框架的 YAML/Skill 元数据语法检查；游戏工作流和事件处理器仍使用 Python 标准库与 Bash。开发检查的安装和证据范围见 [studio-tests](studio-tests/README.md)。

静态结构、脚本测试、真实 Codex 工作流与人工试玩分开登记。75 个正式 Skills、49 个角色的结构覆盖不等于逐个真实运行通过。
当前验收记录和未验证项见 [验收状态](studio-tests/results/codex-adaptation-status.md)、[运行矩阵](studio-tests/runtime-matrix.json)；最初的机制探测另存于 [能力基线](studio-tests/results/codex-capabilities.md)。
CI 配置覆盖 Windows/Linux 框架检查；远端 CI 执行状态以具体提交的运行结果为准。

## 目录

| 路径 | 用途 |
| --- | --- |
| AGENTS.md | 中文项目规范和入口 |
| .agents/skills、docs、rules | 工作流、领域资料与跨目录规则 |
| .agents/scripts、engines、genres | 公共工具、引擎表/scaffold、类型问卷 |
| .codex/config.toml、agents、hooks | Codex 配置、角色和事件适配 |
| design、docs、production | 游戏设计、架构、生产与证据 |
| studio-tests | 框架自动化、行为规范、迁移与运行记录 |

升级边界见 [UPGRADING.md](UPGRADING.md)，贡献约定见 [CONTRIBUTING.md](CONTRIBUTING.md)。
沿用上游 [MIT 许可证](LICENSE) 与作者归属；历史更新记录不作为当前客户端能力声明。
