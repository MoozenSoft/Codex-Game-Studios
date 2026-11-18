# Codex 游戏工作室适配方案与实施计划

> 状态（2026-11-17）：当前分支 `codex/codex-adaptation`。任务1–8的实施与必测验收已完成；75个正式Skills、49个角色、743项来源闭合，双端27项必测场景通过。框架73/73、真实导入浏览器回归2/2及grow作用域Chrome回归、App最终游戏19/19、CLI最终游戏18/18。最终独立Sol评审的3项Important已按一次修复流程通过回归，2项Minor明确延期；M1/M2范围已达成，未推送或合并。

**目标：** 保留上游游戏开发方法，把入口、Skills、角色协作、配置、校验和验证迁移为可实际运行的 Codex 工作流。

**架构：** `AGENTS.md` 承载项目规范，`.agents/skills/` 承载共享工作流，`.agents/` 下的公共资源保留领域知识与脚本，`.codex/` 承载 Codex 客户端配置、角色与 hooks。先完成核心路径，再迁移完整工作室；每批同时迁移引用、测试和文档。

**技术栈：** Codex、本地 Git、Markdown、TOML、YAML、现有 Bash/awk/Python/Node.js 工具。新增事件解析与自动化测试优先使用 Python 标准库；不为迁移引入新的 Agent 编排服务。

**需求依据：** 根目录 `AGENTS.md`、本次用户提供的附加指令，以及质询中确认的九项决定。目录布局、脚本接口和任务分解是落实这些决定的实施设计；客户端能力与最低版本仍需任务 1 实测确认。

## 已确认的范围与验收边界

| 决定 | 最终约定 |
| --- | --- |
| Q1 功能范围 | 全部 75 个正式 Skills、49 个角色均迁移；退役 3 个旧名别名。本轮不合并角色或精简正式工作流 |
| Q2 首要流程 | 先跑通 Web 游戏开发完整流程，再扩展完整工作室能力 |
| Q3 客户端 | Windows 本地 Codex App 和 CLI 都必须验收；云端不在本次范围 |
| Q4 环境依赖 | 接受 Git Bash、Python；优先复用 Bash/awk 脚本，不在本轮消除 Bash 依赖 |
| Q5 升级范围 | 覆盖本仓库自身迁移和从本仓库新建游戏项目；不提供任意已定制上游项目的自动升级工具 |
| Q6 验证覆盖 | 全量结构与契约检查，核心流程及各类别代表场景真实运行；未单独实跑项如实标记 |
| Q7 原生引擎 | 完整迁移 Godot、Unity、Unreal 的规则、角色、配置与脚本；真实编辑器、构建和游戏运行可在首版之后补齐 |
| Q8 协作模式 | 保留 `collaborative / guided / autonomous`，默认仍为 `collaborative` |
| Q9 校验策略 | 禁止操作事前阻断；一般问题允许继续修复，必要检查未通过不得关闭阶段或宣称完成；可选项遵循严格度配置并标记未评估 |

## 全局约束

- 只适配 Codex，不维护 Claude Code 或其他客户端兼容层；上游许可证、来源说明和历史记录保留。
- 共享 Skills 的唯一规范目录为 `.agents/skills/`。
- 模型与推理强度沿用用户的父会话选择，角色和项目不固定模型，委派默认省略模型覆盖。该规则按用户后续要求更新，既有 Sol 实测记录保留为历史证据。
- 中文文档、注释、提交标题和 PR 描述；标识符、路径和配置键保留原拼写；不附加 AI 署名尾注。
- 保留 `project.yaml` 的游戏项目配置职责，不把 Codex 客户端配置混进去。
- 保留三种协作模式及其区别，`modes.automation` 的默认值固定为 `collaborative`，不得在迁移中静默改为 `guided` 或 `autonomous`。
- 明确区分静态检查、脚本测试、Codex 实机工作流和人工试玩；未执行的检查不能记为通过。
- 远端基线无新增提交、已通过全量测试、整合后 tree 相同且工作区状态核对无误时，复用全量测试结果；仅对新增具体风险补定向验证。
- 实施前重新核对工作区与暂存区，保留用户修改，不用全量暂存覆盖提交边界；初次盘点时的 Git 状态不作为实施时的状态假设。
- 仓库当前没有 `.codegraph/`，不创建索引；将来已有索引时优先通过 CodeGraph 定位代码。

## 现状与迁移范围

初次盘点基于本地 `main` 的 `abc0de7`（上游 1.3.0），当时远端配置为 `origin=MoozenSoft/Codex-Game-Studios`、`upstream=Donchitos/Claude-Code-Game-Studios`。以下是迁移来源快照，未据此断言远端最新提交状态；实施时重新核对基线。

| 现有内容 | 已核对的状态 | 迁移处理 |
| --- | --- | --- |
| 根 `AGENTS.md` | 已存在，给出 Codex 约束 | 保留为最高层项目规范，补充简短工作入口 |
| 根及子目录 `CLAUDE.md` | 根、`src/`、`design/`、`docs/`、`studio-tests/` 共 5 份 | 提取领域规则，转为对应作用域的 `AGENTS.md`，去掉 `@` 隐式导入 |
| `.claude/skills/` | 78 个 `SKILL.md` | 75 个正式 Skill 逐批迁移；3 个旧名别名单独退役 |
| `.claude/agents/` | 49 份角色定义 | 保留角色职责与产出，重写客户端配置与委派方式 |
| `.claude/rules/` | 14 份路径规则 | 按目录作用域与跨目录匹配分别处理，保留适用范围 |
| `.claude/hooks/` | 18 个 shell 文件，包含 `yaml-helper.sh` 等辅助文件 | 区分校验逻辑、配置逻辑与事件处理器，不按文件数宣称 hook 覆盖率 |
| `.claude/settings.json` | 注册 8 类事件，含 Claude 权限、statusLine、worktree 设置 | 按 Codex 当前 schema 重建，逐项登记替代或退役 |
| `.claude/scripts/` | 54 个辅助文件 | 优先复用算法与输入输出契约，修复根目录和客户端依赖 |
| `studio-tests/` | 75 个正式 Skill 的 catalog 与行为规范、49 个 Agent 规范 | 保留规范，补可执行自动化及真实运行证据 |
| `.github/` | 当前无 workflows 目录 | 新增框架自身的 CI，和生成游戏的测试区分 |

3 个旧别名分别是 `help → next-step`、`settings → project-settings`、`changelog → write-changelog`；其文件明确仅负责调用旧 `Skill` 工具转发。目录与 catalog 的差异不是 3 个正式工作流漏登记。这三个别名在 Codex 版退役，发布说明列出替代入口。

本地 `codex.cmd --version` 返回 `0.169.0`，但伴随受限临时目录警告；直接运行 `codex` 的 PowerShell 包装脚本被执行策略阻止。因此这只证明版本输出，不能作为 Skill、角色或 hook 已运行的证据，也不据此修改系统执行策略。

## 路线选择

| 路线 | 好处 | 代价与适用性 |
| --- | --- | --- |
| 一次性完成全部原生迁移 | 最终结构可一次收敛 | 75 个工作流同时变化，出错后难定位，首个可用版本较晚 |
| 按可运行流程分批原生迁移（采用） | 先验证核心能力，每批可回归、可审阅 | 过渡期需要清晰登记未迁移内容，禁止新入口依赖旧目录 |

采用第二条。仅改名不能满足 AGENTS.md；同时维护 Claude Code 与 Codex 会扩大范围，也不符合本项目定位。Codex App 和 CLI 共用同一套框架，分别验证客户端集成。过渡期 `.claude/` 仅是待迁移来源，不维护双份运行实现。每迁移一个组件就迁移其完整依赖，登记旧副本退役；最终移除整个旧运行目录。

分批验收只检查已启用组件的必需依赖闭包。清单中的计划目标可以尚未存在；尚未迁移的组件不得放入 Codex 自动发现目录。依赖分为执行必需项与下一步建议：必需项必须随组件迁移，尚未可用的下一步只能明确提示，不得调用。中间校验报告同时列出已启用、待迁移和退役数量；“当前批次通过”不等于完整迁移通过。M2 才要求全部正式 Skill/角色与 catalog 对齐且有效运行引用全部可达。

## 目标设计

### 文件职责

```text
AGENTS.md                         项目规范、入口索引、验证与恢复约定
.agents/
  skills/<name>/SKILL.md           正式工作流与引用资料
  skills/<name>/agents/openai.yaml 按需配置显式调用策略
  docs/                           配置解析、协作协议、模板、工作流目录
  rules/                          跨目录的游戏领域规则
  scripts/                        共享辅助脚本；保留原有文件名
  engines/                        引擎表、Web scaffold 和 starter
  genres/                         类型问卷与配置
.codex/
  config.toml                     项目级 Codex 默认值
  agents/<role>.toml               49 个角色的唯一规范定义
  hooks.json                      Codex 事件注册
  hooks/                          事件输入解析与调用入口
src/AGENTS.md                      代码领域约束
design/AGENTS.md                   设计与叙事约束
docs/AGENTS.md                     ADR、TR 与引擎参考约束
studio-tests/
  AGENTS.md                       框架测试规范
  catalog.yaml                    正式 Skill/角色与行为规范登记
  migration-inventory.json        全量迁移映射与处置状态
  fixtures/                       配置、hook 事件、项目和产物样例
  automated/                      可执行测试
  results/                        版本、平台、输入与运行证据
.github/workflows/framework-checks.yml
project.yaml                      继续保存游戏项目共享配置
production/session-state/active.md 继续保存会话检查点
```

这是目标树，不预先建立空的游戏引擎目录。共享资料按需读取，不把整个角色库、规则库或引擎参考灌入根 `AGENTS.md`。

### 入口、Skills 与配置

- Codex CLI/IDE 文档使用 `$start`、`$prototype` 等 Skill 调用形式；App 的选择器入口单独实测说明。`/start` 不再被描述为 Codex 内置命令。[官方 Skills 文档](https://learn.chatgpt.com/docs/build-skills)
- 保留各正式 Skill 的原有名称、参数含义、输出路径、GDD/ADR/TR/Story 关系和验收规则。迁移时同时检查 `references/`、模板和下一步引用。
- 删除 Claude 专属 `allowed-tools`、`model: sonnet/opus/haiku`、`context: fork`、`!` shell 注入以及 `$ARGUMENTS` 展开假设。需要配置时，Skill 明确执行 `.agents/scripts/yaml-helper.sh resolve_config`，检查实际结果，不将执行失败当成默认配置成功。
- `dev-story`、`story-done` 等显式入口通过 `agents/openai.yaml` 的 `policy.allow_implicit_invocation: false` 表达，并做触发测试；不只删除原 `disable-model-invocation` 字段。[官方调用策略](https://learn.chatgpt.com/docs/build-skills#optional-metadata)
- 保留解析顺序：允许本地覆盖的 `project.local.yaml` → `project.yaml` → 既有项目状态镜像 → `modes.rigor` 展开 → 文档默认值。继续输出取值来源与无效值提示，保持本地读写白名单一致。
- 保留 `minimal/standard/full`、团队规模、review 深度、自动化模式的区别。项目自动化模式只能约定工作流停顿，不能放宽客户端 sandbox、权限和用户指令，也不应对已经授权的相同操作反复询问。
- `CLAUDE.md` 中的引擎 fallback 和脚本写入逻辑转为 `project.yaml` 与 `docs/engine-reference/<engine>/VERSION.md`；不让引擎配置脚本改写根 AGENTS 的政策内容。

### 协作模式的保留规则

| `modes.automation` | 迁移后保留的行为 |
| --- | --- |
| `collaborative`（默认） | 设计选择、草稿与写入按协作流程确认；保留分段审阅和多文件变更确认 |
| `guided` | 重大决策询问，细节推荐后继续；已有文件更新可在简述后进行，新文件沿用上游确认规则 |
| `autonomous` | 一般决策自行选择并记录，不要求逐份草稿和写入确认；仍遵守已配置的必须询问类别 |

保留 `modes.automation_always_ask` 默认类别 `scope_changes`、`file_deletions`、`schema_changes`，以及 `hotfix`、`gate-check`、`day-one-patch`、`setup-engine` 的强制协作规则。将上游 `AskUserQuestion` 调用转换为当次 Codex 可用的交互方式，不通过删除确认步骤把协作模式实际变成自主模式。

以上规则遵循更高优先级指令和明确的会话授权：已经批准的同一决定或变更范围直接沿用，必要问题被跳过不视为同意。个人可通过 `project.local.yaml` 覆盖模式；未配置时返回 `collaborative`，不受 `modes.rigor` 展开影响。

### 角色与协作

49 个角色保留专业边界，不意味着同时启动 49 个代理。按 `team.size` 和所选工作流激活角色，并在执行开始说明实际参与者。

以 `.codex/agents/<role>.toml` 为角色规范源，包含名称、描述、职责、输入输出和约束。省略 model 与 model_reasoning_effort 以继承父会话；不复制上游模型等级。[官方子代理配置](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents)

工作流按当次工具 schema 委派：支持角色绑定时使用绑定；本会话的 `spawn_agent` 没有 `agent_type` 参数，此类环境由父代理读取对应角色定义，将必要指令和输入放入委派消息。两种方式读取同一份角色职责，不另建通用多客户端适配框架。

每次委派明确任务、可改文件、共享输入、验收条件、返回路径、摘要、阻塞项。共享目录避免并发修改同一文件；有依赖的阶段串行。工具不可用或并发额度不足时串行执行并披露执行方式；独立评审是强制要求时，不把同一代理自查记为独立评审通过。

原 `tools`、`disallowedTools`、`maxTurns`、`memory: project` 和 `isolation: worktree` 分别登记处理，不能只改成 TOML 后视为等价。角色指令不构成独立权限沙箱；隔离需求通过受支持的环境能力和经核验的工作树流程实现。会话检查点继续使用现有路径，角色临时记忆另设 gitignored 目录并保留失效条件规则。

### hooks、权限与路径规则

Codex 当前提供项目 `.codex/hooks.json`；实际目标客户端必须验证项目与 hook 信任状态。事件名称相似不代表输入协议相同，尤其 `apply_patch` 提供 patch 命令，不能沿用 Claude 的 `file_path/old_string/new_string` 解析。[官方 hooks 文档](https://learn.chatgpt.com/docs/hooks)

| 上游机制 | 目标处理 |
| --- | --- |
| `SessionStart`、`PreCompact`、`Stop` | 初始化、读取与保存检查点，保留缺项提示；实测对应生命周期 |
| `PreToolUse` 提交/推送检查 | 复用可独立运行的检查逻辑，适配实际 shell 事件；区分提醒和阻断 |
| `PreToolUse` 写入检查 | 解析多文件 patch 的新增、修改、删除、移动；对明确禁止的目标或操作事前阻断，一般产物问题进入后置或阶段校验 |
| `PostToolUse` 资产与 Skill 检查 | 根据实际变更文件校验；错误影响后续交付判断，不声称能够撤销已经发生的写入 |
| `SubagentStart/Stop` | 角色日志和产物核验，测试失败、缺产物和重复事件 |
| `Notification`、`statusLine` | 核对目标客户端支持；没有等价行为时明确退役或改用完成报告，不虚构事件 |
| `.claude/settings.json` 的权限列表 | 按 Codex 支持的项目配置与执行规则重建必要约束，不原样复制，不降低托管权限 |
| `.claude/rules/*.md` 的 `paths` | 目录内规则写入嵌套 AGENTS；跨目录 glob 规则保留索引，由工作流按涉及文件加载，自动约束另由校验器实现 |

事件处理与领域校验分开：领域检查可以从命令行、hook 或 CI 调用。原有只输出观察结果的 helper 保留契约，聚合校验入口负责退出码。不能把一个打印“提醒”的脚本宣称为硬性 gate。

校验分成操作与阶段两个层次：明确禁止的操作在执行前阻断；编辑过程中的普通结构、引用或证据缺失可以继续修复，不能因此拦截每一次编辑。关闭故事、通过阶段或交付前，必要校验失败或无法执行都阻止完成。可选校验无法执行时记录 `NOT ASSESSED` 及原因；是否必要由现有模式和 `testing.strict.*` 等配置决定，不通过迁移降低原有要求。

现有 hooks 覆盖并非完整安全边界；对 shell 写文件、MCP 写入、未覆盖工具路径分别记录覆盖情况。关键产物在交付和 CI 再校验，不能把缺少运行环境或未触发检查记为通过。

### 平台与发布边界

- Windows 本地 Codex App 和 CLI 都是首版必须通过的验收入口；分别验证 Skill 发现与调用、提问授权、子代理、hooks、工作树和核心工作流。任一入口必要场景失败则不满足双入口交付条件。云端不在本次范围；Linux 作为脚本/CI 验证环境，macOS 在获得实际环境之前标记未验证。
- App 和 CLI 共用框架代码及自动化测试。同一 tree、相同依赖和执行环境下的共享脚本测试结果可复用；两个客户端的集成场景分别实跑，不要求各自重复全量脚本测试。Windows 与 Linux 的平台验证不能相互替代。
- 所有 75 个正式 Skills 和 49 个角色均检查结构、输入输出契约、依赖及行为规范；真实 Codex 运行覆盖核心端到端流程和 catalog 中各 Skill 类别、角色类别的代表场景。未单独实跑的组件继续标记，不由抽样推断全部运行通过。
- 现有 Bash/awk 脚本先复用；Windows 明确探测 Git for Windows 的 Bash，不能把 PATH 中的 `C:\Windows\System32\bash.exe` 当作 Git Bash。统一处理中文、空格、盘符、反斜杠、CRLF 和子目录启动。
- 新事件入口优先 Python 标准库，保留现有 Node 浏览器驱动。配置解析不新增 PyYAML 依赖；暂不全量重写 54 个脚本。
- 第一个里程碑跑通 Web 主路径。Godot、Unity、Unreal 的领域规则、角色、配置、脚本和 scaffold 全部属于首版迁移范围；真实编辑器、构建与游戏运行验收可在首版之后分别补齐，不作为 M2 完成的前提。首版仅承诺已实测的 Web 运行路径，原生引擎未实测项保持“运行未验证”。
- 本轮只迁移当前仓库，并保证从迁移后的仓库新建游戏项目可用；不提供任意已定制上游项目的自动升级、冲突合并、备份恢复工具。`UPGRADING.md` 说明本仓库变更与人工迁移边界，不承诺通用无损升级。
- 不增加本地框架运行所不需的 MCP 服务、API 密钥或云端编排。

## 实施任务

以下命令和测试文件是实施阶段要提供的接口，不表示当前仓库已经具备或通过这些测试。

### 任务 1：固定迁移清单与验证基线

**文件：** 新增 `studio-tests/migration-inventory.json`、`studio-tests/automated/test_inventory.py`、`studio-tests/results/codex-capabilities.md`；参考 `.claude/scripts/compat-inventory.sh`。

**接口：** 每条记录含 `source`、`target`、`kind`、`disposition`、`status`、`dependencies`、`validation`、`evidence`；`disposition` 为 `migrate/retire`，`status` 为 `pending/active/retired`，依赖类型为 `required/next_step`，验证状态分别记录 static、script、runtime。退役项以明确替代或理由取代目标路径。

- [x] 为 78 个 Skill、49 个角色、14 份规则、全部脚本和事件注册建立清单；显式登记 3 个别名退役理由。
- [x] 增加 `test_inventory_covers_sources`、`test_formal_skills_match_catalog`、`test_retirement_has_replacement`，断言来源无漏项、来源正式 Skill 集合等于 catalog、每条来源均有计划目标或退役理由；此阶段不要求尚未迁移的目标存在。
- [x] 分别记录 Windows App 和 CLI 的版本、可用工具、Sol ID、Git Bash/Python/Node/浏览器和 hook 信任流程；两个客户端均选择最小 Skill、角色和无害 hook 做实机探测。
- [x] 建立运行验收矩阵：App/CLI 核心流程为必测，catalog 各 Skill 类别与角色类别选定代表场景并预留证据字段；列明未单独实跑的组件和暂缓的原生引擎运行项。场景执行与证据填写按后续任务推进。
- [x] 执行 `python -m unittest discover -s studio-tests/automated -p test_inventory.py -v`；输出通过且清单覆盖完整。实机探测单独留证，以已测 CLI `0.169.0`、App `26.1111.2228.0` 为最低验收起点，较低版本不作支持承诺；完整运行支持仍需后续场景验证。

### 任务 2：迁移公共依赖、配置与作用域规则

**文件：** 迁移 `.claude/docs/`、`.claude/rules/`、`.claude/engines/`、`.claude/genres/` 到目标树；将 `.claude/hooks/yaml-helper.sh` 移到 `.agents/scripts/yaml-helper.sh`，其余共享脚本迁入 `.agents/scripts/`；新增 4 份子目录 `AGENTS.md`、`.agents/docs/rule-routing.md`、`studio-tests/automated/test_config.py`、`test_paths.py`。

**接口：** 保留 `resolve_config --keys ...` 及现有 helper 的 TSV、参数和退出码约定；根路径由脚本位置或显式 `--root` 确定，去除 `CLAUDE_PROJECT_DIR/CLAUDE_SKILL_DIR` 依赖。

- [x] 固定配置样例：无配置、三种 rigor、三种 automation、本地合法/非法覆盖、无效枚举、状态镜像冲突；断言值、来源和警告，不只检查命令成功。
- [x] 增加 `test_default_automation_is_collaborative`、`test_automation_independent_of_rigor`、`test_local_automation_override`：未配置时始终解析为 `collaborative`，任意 rigor 不改变它，合法本地覆盖优先于共享设置。
- [x] 迁移公共内容并翻译有效指令，处理跨引擎代码根、模板和相对引用；新增 AGENTS 只放领域约束，不覆盖根层模型与提交规定。
- [x] 更新 `web-scaffold.sh`、`one-shot-grow.sh`、`config-set.sh` 等写配置或识别空项目的代码，避免再次生成 `CLAUDE.md`，避免将新增 AGENTS 当作已有游戏代码。
- [x] 用含中文/空格的根目录、子目录启动和 Windows/Unix 路径测试配置与根目录解析；校验已启用共享资源的必需引用可达，指向后续 Skills 的导航登记为未可用。
- [x] 执行 `python -m unittest discover -s studio-tests/automated -p 'test_config.py' -v` 和对应 `test_paths.py`；已有脚本行为不回退。

### 任务 3：建立 Codex 角色与调用约定

**文件：** 新增 `.codex/config.toml`、核心角色对应的 `.codex/agents/*.toml`、`.agents/docs/coordination-rules.md`、`studio-tests/automated/test_agents.py`；迁移相应 `studio-tests/agents/` 规范及角色的必需 Skill 依赖。

**接口：** 保持原 49 个角色名；委派输入/输出采用“任务、输入、可改路径、验收、产物、摘要、阻塞项”契约，任务后续统一使用。

- [x] 先迁移 `prototyper`、`gameplay-programmer`、`lead-programmer`、`qa-tester`、`technical-director` 与必需依赖（如 `lead-programmer` 原预加载的 `tech-debt`）；其余角色在任务 6 完成。
- [x] 配置测试断言本批启用角色齐全、schema 合法、没有 Claude 专属字段或非授权模型；必需 Skill/资料必须存在。对 `prototyper` 指向 `vertical-slice` 等后续入口，按实际执行语义分类，不能以“下一步建议”掩盖必需依赖。
- [x] 实测普通委派、失败反馈、追问续作、并发额度不足与无角色绑定参数的路径；同文件写入任务不得并发。
- [x] 为角色记忆与会话状态定义读取、写入、失效和忽略规则；迁移 `.worktreeinclude` 的有价值语义，不假设 Codex 自动识别该文件。
- [x] 执行 `python -m unittest discover -s studio-tests/automated -p test_agents.py -v`，并保存至少一次真实角色产出与回收证据。

### 任务 4：迁移事件校验并建立可靠交付检查

**文件：** 新增 `.codex/hooks.json`、`.codex/hooks/dispatch.py`、`.codex/hooks/event_input.py`、`.agents/scripts/validate-framework.py`、`studio-tests/fixtures/hooks/`、`studio-tests/automated/test_hooks.py`；迁移原校验脚本中的领域检查到 `.agents/scripts/`。

**接口：** `validate-framework.py --scope all|changed --stage incremental|complete --format text|json` 返回 `0=所选阶段通过`、`1=必要校验不通过`、`2=必要检查无法执行`；`stage` 默认 `incremental`，只验已启用组件及必需依赖，`complete` 还要求无待迁移组件和有效旧运行引用。JSON 包含阶段、覆盖数量、检查 ID、状态、是否必要、文件、原因。可选项未评估单独记录，不冒充通过，也不单独触发退出码 2。事件入口读取 stdin JSON，按目标 Codex 事件协议返回结果。

- [x] 先建立真实事件 fixture 与失败测试：多文件 patch、移动/删除、CRLF、中文路径、越界路径、坏 JSON、空输入、缺 Python/Bash、无效注册表、过期评审凭据。
- [x] 实现输入解析与领域检查调用，不套用旧 Write/Edit 内容重建协议；不能重建的变更明确报告，不臆造写后内容。
- [x] 增加 `test_forbidden_operation_blocked_before_execution`、`test_incomplete_artifact_allows_repair`、`test_required_failure_blocks_completion`、`test_optional_unassessed_is_reported`：分别验证禁止操作阻断、普通缺项不阻止修复、必要失败/缺环境拒绝完成、可选未评估不伪报通过；切换严格度后按新要求判断。
- [x] 逐项覆盖已登记事件；对 Notification/statusLine 等登记替代或退役；保留停止循环防护、日志幂等和并发写入约束。
- [x] 分别在受信任的 Windows App 和 CLI 会话验证至少一次放行、一次禁止操作的事前阻断、一次后置告警及一次检查点恢复；未信任或禁用 hooks 必须能被验收发现。
- [x] 执行 `python -m unittest discover -s studio-tests/automated -p test_hooks.py -v` 和 `python .agents/scripts/validate-framework.py --scope all --format json`；记录工具覆盖范围。

### 任务 5：交付核心游戏开发流程

**文件：** 迁移以下 Skill 及完整 `references/` 依赖到 `.agents/skills/`：`start`、`next-step`、`project-settings`、`project-stage-detect`、`brainstorm`、`prototype`、`setup-engine`、`create-epics`、`create-stories`、`story-readiness`、`dev-story`、`code-review`、`smoke-check`、`story-done`；增加 `studio-tests/automated/test_core_skills.py` 和 `studio-tests/fixtures/projects/`。

**接口：** 保持 `design/game-brief.md`、`prototypes/<name>/`、`production/epics/`、`production/qa/evidence/` 等既有产物位置；保留故事状态、需求追踪与 checkpoint 格式。

- [x] 从迁移清单求完整依赖集；若 `next-step` 可能引向尚未迁移的正式 Skill，先显式说明未可用，完整发布前再消除这些缺口。
- [x] 改写工具调用、参数读取、显式执行的配置解析、审批复用与下一步推荐；不机械替换所有以 `/` 开头的文本。
- [x] 为三种协作模式建立行为用例，核验默认协作模式的草稿/决策确认、guided 的新文件确认、autonomous 的决策日志、必须询问类别和四个强制协作 Skill；另测已有授权复用及必要问题被跳过时不能擅自推进。
- [x] 完成 Web 流程：需求 → brief → 浏览器原型 → 试玩反馈/修改 → grow → 单功能迭代 → 测试与交付。另测用户明确选择的 Story 路径及 `--from` 导入原游戏。
- [x] 测试模糊需求、空参数、无浏览器、依赖缺失、取消/跳过问题、已有配置和恢复会话；未完成试玩不能自动判定 PROCEED。
- [x] 执行核心静态与 fixture 测试，随后在 Windows App 和 CLI 各用临时项目完成核心端到端演练；保留截图、命令结果、产物和未评估项。两端均验证默认 `collaborative`，模式差异按验收矩阵补代表场景；模板中不提交生成游戏。

**里程碑 M1：** Windows App 和 CLI 的 Web 核心流程、角色协作与关键校验均实测可用；README 清楚列出已迁移和待迁移范围。M1 是中间检查点，完整迁移仍需推进到 M2。

### 任务 6：迁移其余工作室工作流与引擎能力

**文件：** `.agents/skills/` 的剩余正式 Skills、`.codex/agents/` 的剩余角色、`.agents/docs/workflow-catalog.yaml`、`studio-tests/catalog.yaml`、对应行为规范、`.agents/engines/` 和 `docs/engine-reference/` 引用。

**接口：** 正式 Skill 集合按 catalog 保持 75 个，角色保持 49 个，除非后续批准合并或删除；每个工作流的入口、配置、角色、模板、输出和下一步引用闭合。

- [x] 按“设计与架构 → 团队管线 → QA/发布/运营 → Skill 自检”迁移剩余工作流；每组同步变更测试和文档。
- [x] 将 `skill-test`、`skill-improve`、`skill-lint.sh`、`agent-check.sh` 改为验证 Codex 规范，不再要求 Claude frontmatter；确认行为按所选协作模式检查，不强制所有模式出现同一句逐文件审批措辞，也不移除 collaborative 的确认要求。
- [x] 覆盖全部正式 Skills 和角色的结构、输入输出契约、依赖与行为规范；按任务 1 的矩阵完成每个 Skill 类别、角色类别的代表场景，含团队管线、发布和自检。其他组件的真实运行状态按清单记录，不能由抽样推断全部运行通过。
- [x] 对 Web/Godot/Unity/Unreal 分别验证配置、代码根、测试根、scaffold 和引用；原生引擎真实编辑器、构建和游戏运行可后续补齐，未执行项标为“运行未验证”。原生引擎角色的代表场景可验证规则与产物契约，不以此代替编辑器运行证据。
- [x] 每组运行相关测试及依赖引用校验，检查 `minimal/standard/full` 下的产物要求和 reviewer 深度未丢失。

### 任务 7：文档、CI 与旧运行入口退役

**文件：** 更新 `README.md`、`CONTRIBUTING.md`、`UPGRADING.md`、`SECURITY.md`、`CHANGELOG.md`、`docs/WORKFLOW-GUIDE.md`、`docs/skill-flow-diagrams.md`、`docs/COLLABORATIVE-DESIGN-PRINCIPLE.md`、`.github/` 模板、`.gitignore`、`.gitattributes`；新增 `.github/workflows/framework-checks.yml`、`studio-tests/automated/test_migration_complete.py`。

**接口：** CI 使用统一框架校验入口；迁移清单中每个来源都有已迁移目标或明确退役理由。历史文档、LICENSE、来源说明与迁移记录允许保留 Claude 名称，其余有效运行引用不允许。

- [x] README 改为中文 Codex 安装、启动、Skill 使用、平台要求、hooks 信任和能力状态说明；明确三种模式及默认 `collaborative`、Windows App/CLI 验收范围、Git Bash/Python 依赖、原生引擎未验证项。更新 GitHub 地址，以真实 remote 为依据。
- [x] CI 在 Windows/Linux 跑自动化与 `--stage complete` 结构校验；分别验证 Bash 语法、TOML/YAML/JSON、模板引用、角色映射、禁用模型与残留运行语法。
- [x] 全部新工作流不再依赖 `.claude/` 后删除旧目录、5 份 `CLAUDE.md`、无效 worktree 配置；保留上游 MIT 许可和作者归属。
- [x] 新 clone 使用独立测试配置分别在 App 和 CLI 完成启动，不依赖维护者私有 Skills、全局角色、MCP 或旧本地配置；验证从本仓库新建游戏项目可用。针对当前仓库迁移核对已有内容保留情况，不扩展为任意上游定制项目的自动升级测试。
- [x] `UPGRADING.md` 明确本次只覆盖当前仓库迁移与新建项目，说明旧入口替代和人工迁移注意事项，不新增通用升级器或承诺自动合并用户定制。
- [x] 执行全部框架测试与 `--stage complete` 全量引用校验，确认没有未经说明的缺失检查；真实模型工作流的证据不冒充普通 CI 测试。

### 任务 8：发布前验收与证据登记

**文件：** `studio-tests/results/` 下的验收记录、迁移清单验证状态、README 能力表、发布说明。

- [x] 运行 `python -m unittest discover -s studio-tests/automated -p 'test_*.py' -v` 与 `python .agents/scripts/validate-framework.py --scope all --stage complete --format json`。
- [x] 分别复核 Windows App 和 CLI 的必测矩阵，覆盖 Skill 发现、角色委派、hooks、提问授权、工作树、核心流程、故障反馈、恢复与交付；记录客户端/模型/平台、输入场景、Git tree、结果和证据路径。同一 tree、依赖和执行环境的共享脚本测试复用已有结果，两端集成证据分别提供。
- [x] 将每项能力分别标记“静态通过 / 脚本通过 / 实际运行通过 / 未验证”，人工试玩另列；修复失败项或收窄发布声明。
- [x] 按 AGENTS.md 和已确认边界检查中文文档、父会话模型继承策略、无 AI 尾注、唯一 Skill 目录、无 Claude 运行依赖、三模式保留且默认 `collaborative`、用户修改未丢失，以及原生引擎/自动升级支持声明没有超出证据或范围。
- [x] 整合时核对远端基线、tree、提交关系和工作区；满足复用条件则复用本次全量结果，不因 squash 或 SHA 改变重跑。

**里程碑 M2：** 全部 75 个正式 Skills 和 49 个角色完成迁移与结构/契约检查，目录与运行引用闭合；Windows App 和 CLI 的核心必测场景通过，各 Skill/角色类别代表场景有实测证据。三种协作模式保留且默认 `collaborative`。原生引擎已完成规则、配置、脚本与角色迁移，但真实运行验收可后续补齐；未单独实跑的工作流、角色和引擎保留“未验证”。这是首个 Codex 版本的完成条件，不要求逐个实跑全部组件，也不包含通用上游项目自动升级工具。

## 评审重点与对应验证

| 易遗漏情况 | 预期结果 | 归属任务 |
| --- | --- | --- |
| 根路径带中文/空格，从子目录或 worktree 启动 | 始终使用当前 checkout 的配置与资源 | 任务 2、3 |
| hooks 未受信任、缺 Bash/Python、事件解析失败 | 明确显示校验不可用，不能伪报通过 | 任务 1、4 |
| 单个 patch 修改多文件、移动、删除或越界 | 逐目标检查，失败有具体原因 | 任务 4 |
| 普通产物未完成、必要检查失败、可选证据缺失 | 允许修复；必要失败阻止完成；可选缺失明确未评估 | 任务 4、8 |
| 用户已授权、问题被跳过、无提问工具或子代理工具 | 复用已有授权；必要决定不凭空假定；说明降级边界 | 任务 3、5 |
| 未配置 automation、改变 rigor、切换个人模式 | 默认 collaborative；rigor 不改变模式；本地覆盖生效 | 任务 2、5 |
| 当前仓库和新建项目中的自定义 Skill、引擎配置与游戏内容 | 保留用户内容，不误覆盖或误判空项目；不承诺通用上游自动升级 | 任务 2、7 |

## 执行顺序与历史记录

顺序为 **1 → 2 → 3 → 4 → 5 → 6 → 7 → 8**。角色扩展、独立 Skill 批次与文档可在明确文件所有权后并行，但共享配置、脚本接口和事件协议先固定。建议每个任务形成独立可审阅变更；提交时使用中文标题，不附署名尾注。

任务 1 已完成：来源清单与运行矩阵建立，Windows CLI 与 App 的最小 Skill、项目角色和正常受信任的 SessionStart 均取得真实运行证据；App 中完整最终答案和三个正确口令已直接查看确认，此前 Thinking 显示问题已关闭。任务 2 进行中：配置解析器及最小依赖已建立，8 项配置行为测试与 7 项清单测试均通过；其他公共资源、正式 Skills 与角色仍待迁移。证据与边界见 `studio-tests/results/codex-capabilities.md`。后续按任务 1–5 达成 M1，再按任务 6–8 达成 M2；原生引擎真实运行验收在首版后按需要补齐。

任务 2 验证补充：公共脚本与跨引擎规则已迁移，26 项自动化测试通过；角色/Skill 自检与生命周期专用工具按任务 4、6 继续适配，未启用项保持 pending。
