# 全项目 Codex 适配遗漏审查

基线：`a809e2e47273141ad338fa30fb45acfca6031199`。研究对象为当前工作树；无 `.codegraph/`，未创建索引。仅生成审查报告，未修改实现、index 或 HEAD。覆盖运行配置、hooks、脚本、75个 Skill 及引用/合同、共享规范、模板、行为规格、根和目录入口、CI。原文来源、历史报告、测试数据中的旧客户端字符串不直接计为遗漏。

结论：未发现已证实 Critical；6项 Important（其中1项依赖事件输入形状）、9项 Minor，以及若干待验证观察。全量结构/脚本测试通过不能代替这些运行语义和说明的适配。

## Important

### I1：禁止的本地引擎覆盖仍影响实际派生目录

- 位置：`.agents/scripts/yaml-helper.sh:1495–1505` 的 `_yh_engine_name()`；调用处1584、1630、2120；旧优先级同时留在 `.agents/docs/code-root-resolution.md:36`。
- 共享配置声明 Web，个人文件声明 Unity。`resolve_setting engine.name` 正确返回 `Web / project.yaml`，notes 也说本地 engine.name 不允许、已忽略。
- 但相同项目执行 `resolve_config --keys engine,engine_values,engine_row` 实际得到：

```text
engine: Web (project.yaml)
engine_values: name=Web(project.yaml) version=unset language=unset
engine_row: engine=Unity(project.local.yaml) code_root=Assets(project.local.yaml) test_root=Assets/Tests(project.local.yaml) ...
notes: local: not locally overridable, ignored — engine.name
```

- 使用项目约定的正斜杠 Git Bash 路径在临时项目实测，退出0。没有修改真实项目配置。
- 影响：扫描、规则与测试定位会使用另一引擎的目录。应统一所有解析入口的本地白名单策略，而非只修正文档或设置写入器。

### I2：原生 exec_command 输入分支的 matcher/参数适配不完整（条件性）

- 位置：`.codex/hooks.json:PreToolUse/PostToolUse` matcher 为 `Bash|apply_patch`；`.codex/hooks/event_input.py:33–39` 与 `dispatch.py:35–44` 支持 exec_command 名称却只读取 `command`。
- 当前可用 exec_command schema 使用 `cmd`。纯函数复现：Bash+command、exec_command+command 对危险 Git 字符串均拒绝；exec_command+cmd 返回 None；matcher 也不匹配 exec_command。
- 如果客户端事件保留原生名称和参数形状，命令守卫以及依赖 command 的提交前暂存 JSON 检查不会按文档预期工作。缺命令数据也没有在该分支明确标为未评估。
- 此处只将危险命令作为字符串传给判定函数，绝未执行。没有证明客户端 sandbox 被绕过，也不否定已有客户端采用 canonical Bash/command 形状的通过证据。应按各客户端实际事件规范补齐 matcher 和输入归一化并复测。

### I3：手工验收仍依赖多选字段和“空选=通过”

- 位置：`.agents/skills/smoke-check/references/4-manual-checks.md:45–52,64–129`；同类 multiSelect 字段见 `design-review/SKILL.md:405`、`qa-plan/SKILL.md:310`。
- 当前可用提问 schema 是单选，不提供这些 multiSelect 参数。smoke 还要求“未选任何失败项则通过”，不能可靠区分明确无问题与关闭/跳过问题。
- 影响：难以完成所定义的 UI 协议，或把未回答误判成手工检查通过。应使用实际可用接口，明确区分 PASS、FAIL、未测试/未回答；无法交互时保持未评估，不能靠空白判定成功。
- `design-review:368` 还禁止普通文本问答，与 runtime 无工具时对话回退规则矛盾。

### I4：正式行为规格仍精确要求旧客户端字段/注入

- 位置：`studio-tests/skills/utility/hotfix.md:50`、`day-one-patch.md:42`、`launch-checklist.md:47` 要求 `disable-model-invocation: true`；三份都由 catalog 收录。
- 当前实现正确使用 `agents/openai.yaml` 的 `allow_implicit_invocation: false`。skill-test 要求精确比较静态断言，因此正确实现仍可能按旧规格被判 FAIL。
- `studio-tests/skills/utility/next-step.md:374` 仍要求使用注入结果而不重新读取，规格开头也描述独立 Skill 模型和隐式注入；当前实现采用显式执行 helper。
- 应修正规格的可执行标准，不能为迎合旧测试补回废弃字段。

### I5：agent-memory 规则保留追加检查点与一刀切批准

- 位置：`.agents/rules/agent-memory.md:11–14,23–24`，声称 active.md 只能 append、不能 rewrite，其他写入全部先询问，并将这三项豁免错误归于当前 AGENTS。
- 当前合同是 checkpoint 标记区 overwrite、正文记录另行追加；session-state helper 按合同覆盖，三种模式也复用已有批准。
- 此规则在写角色笔记时会由 paths 路由加载，并会指导后续其他写入。若按其建议追加第二个 CHECKPOINT，SessionStart handler 只提取首块。
- 临时文件含 OLD 和 NEW 两个块时，实际 dispatch 仅恢复 OLD。这不是要求修改首块读取算法；首先应让规则与单块覆盖合同一致，避免代理制造过期恢复数据。

### I6：read_guard 自动拦截承诺没有生产接线

- 位置：`.agents/docs/effects-map.md:130–131,2050–2087`，称 read_guard 默认开启，由 validate-read.sh 的 PreToolUse Read 自动拒绝大文件。
- validate-read.sh 已退役；当前 matcher 没有 Read，未找到 Skill 对 read-guard.sh 的生产调用。`.agents/docs/hooks-reference.md:11` 也承认它只是需显式执行的 helper。
- 算法存在不等于自动约束生效。配置文档不能把当前没有接线的能力写成已启用功能；应明确未实现或补足实际调用路径与验收。

## Minor

| 编号 | 位置 | 遗漏与影响 |
| --- | --- | --- |
| M1 | `studio-tests/templates/agent-test-spec.md:19–20` | 新建角色规格模板还要求 model/tools frontmatter、固定gpt-6.1-sol及禁止Astra，与原生TOML和父会话继承冲突，会把新规格带回旧标准 |
| M2 | `.agents/docs/hooks-reference.md:3` | “已实测七类事件”超过证据；真实PreCompact触发仍未评估，不能由fixture或注册状态推出已实测 |
| M3 | `.agents/docs/templates/session-state.md:58–72` | 仍承诺旧statusline、压缩后的SessionStart和自动分支差异警告；当前dispatch不比较Git分支，状态栏入口已退役 |
| M4 | `.agents/docs/automation-modes.md:26,38`、`config-resolution.md:50–54` | is_always_ask_category/log_decision 是source后函数，不是yaml-helper直接命令；文档缺调用协议及完整日志参数。直接运行前者已复现退出2 |
| M5 | `.agents/docs/effects-map.md:199–211` | 枚举错误/孤立个人文件/未知键启动审查的说明与当前fallback+notes及SessionStart实现不一致 |
| M6 | `.agents/skills/start/SKILL.md:61` | 模板远端只识别旧上游，克隆当前Codex模板不会触发同样的远端提醒；未发现自动push路径 |
| M7 | `.agents/skills/dev-story/SKILL.md:324–326` | 仍称story-done只检查文件、runs nothing；实际story-done检查必要运行结果或按条件复用。这是交接说明错误，不是完成门禁已经失效 |
| M8 | `asset-audit/SKILL.md:18–21,110–112`、`perf-profile:97–100`、`project-settings:63–65`、`project-stage-detect:60–62` | 正文仍把已删的Skill allowlist当实际命令授权；asset-audit还因此固定声称音频duration不可测。应按实际工具/权限判断，不据不存在的授权表判缺能力 |
| M9 | `.agents/skills/write-changelog/SKILL.md:45–50,91–97` | 声称历史块在正文前auto-resolved、读取injected subjects；当前是需显式执行的普通Bash代码块，可能混淆“未执行”和“空历史” |

## 观察项：不能据此断言已经越权或失败

- 68个包含 resolve_config --keys 的 Skill 入口中，65个初始化片段不请求 automation_always_ask。后续对照用户指定原项目确认：原项目也仅3个入口初始化读取，其他入口按需查询；不能把这一实现差异直接认定为 Codex 适配缺陷。本轮曾批量补齐，已按用户要求撤销。
- design-review 假定能读取上下文百分比、code-review 假定固定25k读取上限、start 用独立Skill模型解释重新调用。当前没有给出可靠检测来源；未逐个验证各客户端上下文工具和slash命令能力，不应编造百分比或模型切换。
- bug-report、balance-check、tech-debt 的旧 preload/子代理无提问工具说明与当前显式读取、实际schema不完全一致，但其父代理回退仍安全；没有据此判定真实工具调用失败。
- Windows反斜杠绝对脚本路径的额外复现：Bash可以打开helper，但其资源目录推导可能将引擎表当成不存在；同一项目改用正斜杠后查表正常。已区分路径因素与I1本地覆盖问题，尚未遍历所有调用者，暂不认定所有Windows入口都有此故障。

## 验证与排除

- I1使用Git Bash和已安装Python在本任务临时目录实际运行；最终证据使用正斜杠路径及正常引擎资源定位，排除了调用路径造成的查表干扰。
- I2仅运行判定函数并检查matcher；I5仅运行临时检查点的SessionStart handler；M4仅运行无副作用的类别查询。均未运行破坏命令、未读取凭据、未触发真实部署或客户端权限绕过。
- 技能/文档问题已按实际实现、catalog消费和schema交叉核对，不把英文领域术语或通用Read/Write动作当旧客户端接口。
- 49个活动角色已经英文适配；没有把差异JSON里的原文、历史迁移报告或明确的未评估事项当活动残留。未发现需要在本轮新增报告的genres/engines领域内容问题。
- 当前结构校验仍可通过；现有80项框架测试不覆盖所有上述交互、来源形状、规则与文档语义。这些发现不等于全部功能都未迁移，也不能据测试通过消除它们。
- 本轮没有修改任何实现，不重跑无变化的全量/收费模型矩阵。后续优先修复I1–I3，再同步恢复与规格合同，逐项补针对性验证。

## 修复处置（2026-11-17）

用户随后要求修复。上文保留的是修复前审计，不再代表当前实现；以下为本轮结果。英文领域正文保留，客户端专用机制以英文定点适配；没有复制新的上游全文快照。

| 编号 | 当前处置 | 核验 |
| --- | --- | --- |
| I1 | `_yh_engine_name` 只读取共享引擎或受支持的旧格式回退；个人 engine 不再影响派生根。同步 code-root 文档 | Web/shared + Unity/local 的实际脚本回归；engine_row、代码根和测试根一致 |
| I2 | matcher、工具名和输入统一支持原生 exec_command/cmd、functions. 前缀及 patch input/raw。缺失、冲突或无法提取 patch 目标明确未评估 | 危险命令判定、路径保护、写后 JSON 与实际暂存 JSON 回归；均未执行破坏性命令或真实 commit |
| I3 | smoke/QA/design 改用当前实际单选工具 schema；同步与异步接口分开，异步回执保留 WAITING。空白、关闭或缺项不能成为通过或批准 | JSON 示例解析、状态映射合同及正式行为案例；没有以静态合同冒充实际用户交互 |
| I4 | 正式规格对齐 agents/openai.yaml 的原生显式调用策略，依赖内容显式读取，取消独立 Skill 模型和隐式注入前提 | 原生策略与正式合同检查 |
| I5 | agent-memory 使用单块 CHECKPOINT 覆盖、块外正文追加；写入遵循当前模式和已有授权 | 共享合同；临时文件连续更新后恢复最新单块 |
| I6 | 删除自动 Read hook 拦截承诺，在 codex-runtime 建立显式 read-guard 调用协议，LARGE 后真实有界读取 | 合同与临时 helper 场景；这是工作流约束，未实现原生自动读拦截 |
| M1 | 角色测试模板使用原生 TOML 键，默认省略模型与推理覆盖以继承父会话 | 模板合同；49角色源未因本轮改写 |
| M2 | 区分七类事件注册、fixture 和真实客户端证据，真实 PreCompact 保留未评估 | 共享合同和实际证据边界检查 |
| M3 | 会话模板按实际 SessionStart STATUS/CHECKPOINT 恢复；由代理核对 Git 分支，不承诺 statusline 或压缩后自动事件 | 恢复合同与临时检查点场景 |
| M4 | 给出 source-only 类别查询及完整六参数 log_decision 调用、状态和产物检查 | 实际 Git Bash 类别命中/未命中和临时日志 |
| M5 | effects-map 改为真实 fallback+notes、白名单和显式校验行为，移除不存在的启动全量审查 | 与现行解析器合同对照；定向配置回归 |
| M6 | start 使用只读模板远端分类 helper，识别当前 Codex 模板及上游，fork 区分准确；已登记 native_components | 9个真实子进程分类样例，不改远端或联网 |
| M7 | dev-story 交接包含必要测试、结果和已测 tree；story-done 按证据执行或有条件复用 | 正式规格及合同同步 |
| M8 | 移除正文中以已删 Skill allowlist 作为授权/能力依据的表述；音频 duration 按实际可用工具测量 | Skill 与正式合同同步，未假称音频资源实测 |
| M9 | write-changelog 显式读取历史并核验状态，区分 NOT RUN、失败和真实无提交 | 合同及失败/未执行正式案例 |

补充观察项：曾批量补齐配置初始化读取，后因不属于必要适配按用户要求撤销；保留原项目的按需读取方式。其他处理保留：移除无来源的上下文百分比、固定读取上限和独立 Skill 模型假设；依赖按实际读取/工具能力处理；Windows 反斜杠绝对 helper 路径在资源定位前规范化，并通过真实 Git Bash 回归。

### 独立复核及补充修复

独立只读评审提出两项 Important、一项 Minor，均已处理：

- smoke 最终规则覆盖包括存档、性能和平台的全部必测失败，FAIL 优先于未评估和警告。平台表保留未评估计数；quick 后缀保留实际 verdict。正式 Case 17 覆盖上述失败和未回答组合。
- 提交检查先核实 workdir/cwd、事件 cwd 和 git -C 的实际 Git 根目录。当前项目子目录可用；外部/嵌套独立仓库、目录切换或不支持的 Git 配置/环境覆盖明确拒绝并报告未评估，不拿另一个索引冒充通过。实际临时仓库回归包含 LF、CRLF 和空白行目录切换，命令始终只作为字符串输入，未实际提交。多行边界修复已由评审者限定复核确认。
- QA 完成结果覆盖两项输出的四种明确组合和待回答状态；异步回执不能关闭流程。评审者已确认 smoke 与 QA 修复。

命令检查仍是辅助约束，不是完整 shell 解析器或安全边界；不支持的任意嵌套 shell、MCP 与其他工具不因此获得完整覆盖。

### 最终验证

- 批量读取回滚前的 Windows 完整框架回归 **106/106，通过，46.875秒**；原有80项加26项针对配置、原生事件、提交上下文和文档/交互合同的回归。该历史输出包含后来删除的1项全覆盖断言，不是回滚后的全量结果。见 [完整测试输出](framework-tests-2026-11-17.txt)。
- **17份 YAML、75个 Skill frontmatter、50份 TOML** 与 complete 全阶段校验通过。743项来源仍为733 active、10 retired、pending=0；native_components=20。见 [YAML结果](framework-yaml-validation.json)、[complete结果](framework-complete-validation.json)。
- 本轮修改的 yaml-helper.sh 已通过实际 Git Bash 的 bash -n；diff --check 通过。之前51份脚本语法结果保留为历史记录，本轮未冒称重新运行51份。
- 本轮没有重跑 App/CLI 信任、事件投递、模型行为或游戏引擎端到端。hook 定义有变化，需客户端正常审阅后才能补充新的真实触发证据；真实 PreCompact、人工试玩、原生引擎和远端 CI 仍未评估。未将它们登记为通过。


### 按用户要求撤销非必要增强

已撤销65个 Skill 初始化命令的批量补读，全部68条初始化命令与本轮修复前 HEAD 一致；仅 adopt、story-done、propagate-design-change 保留原有 automation_always_ask 初始化读取。公共协作规则改为决策点按需读取或查询，移除强制全部初始化包含该项的测试，不删除原项目配置与函数。

回滚后剩余 Skill 合同定向测试10/10通过，17份YAML和75个Skill frontmatter检查通过。当前测试集合105项；上面的106项全量输出保留为回滚前历史，本轮未重复全量，也未将历史结果改写为105项实跑。其他配置、hooks、交互及文档修复保留。


### 提交458b4a0的CLI实机补证

按用户要求追加真实CLI验收，启动恢复、配置解析、原生工具前后hooks、异步待答与明确输出选择、实际索引阻断均取得运行证据；初次隔离目录不完整的失败保留，补齐后校验退出0。详见 [CLI定向验收及范围](cli-audit-458b4a0.md)。这次证明实际CLI路径，不把fixture、受信任定义数量或模型决策计算冒充所有客户端形状、七类真实事件或游戏完整运行；App和真实PreCompact等原未评估事项保持不变。


### 提交458b4a0的App实机补证

按用户要求追加App原生界面四回合验收，含真实问题卡片的两个独立答案及可见最终结果；写后JSON、env/跨仓库/坏索引阻断均保留直接hook回执。详见 [App定向验收及业务结果边界](app-audit-458b4a0.md)。阻断断言通过不表示被拒绝操作或内容合格；smoke只验证模型对fixture的判定，原有未评估范围不变。隔离恢复后的适配器保留例外单独登记，未宣称所有文件完全未变。


### 2026-11-18 App压缩与角色追加验证

App真实PreCompact的待验证项已由原生菜单压缩、真实事件和ContextCompaction完成记录补证；当前qa-tester的原生角色完整指令加载、实际父子模型/推理继承和同一代理追问也已验证。七类事件在本轮App受控路径均有真实日志。详见 [续验报告](app-continuation-2026-11-18.md)；CLI/自动压缩与其它未评估范围不据此扩大。更新当前说明与登记，旧审计和旧日期报告保留原时点状态。
