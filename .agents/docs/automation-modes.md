# 三种协作模式

工作流通过 yaml-helper.sh 显式读取所需配置；涉及协作模式时读取 `automation`，涉及强制询问类别时按需读取 `automation_always_ask` 或查询 `is_always_ask_category`。取值顺序为允许的本地覆盖、project.yaml、默认值。
默认模式为 `collaborative`；`modes.rigor` 不改变它。个人模式可在 project.local.yaml 中覆盖。

| 模式 | 决策 | 写入 |
| --- | --- | --- |
| collaborative | 询问目标，呈现选项，取得决定，展示草稿，确认后执行 | 按已批准草稿或变更集合写入；多章节逐段审阅 |
| guided | 重大决策询问，细节简述推荐后继续 | 更新已有文件简述后进行；新文件按上游约定确认 |
| autonomous | 选择有依据的方案，记录决定后继续 | 直接写入，不逐份审阅草稿；必须询问类别仍等待回答 |

所有模式遵守明确会话授权与更高优先级指令：同一决定或变更范围已明确批准就直接沿用，不为同一授权反复询问。
必要问题被跳过、关闭或返回空白不算同意；无可用提问工具时在对话中列明问题并等待。无法取得必要回答的无人值守运行报告阻塞，不能猜测授权。
自主模式中本来无需询问的一般选择可自行决定并记录；已要求必须由用户决定的事项仍等待明确回答。

## 重大与细节决策

重大决策包括系统命名或产物路径、互斥设计方向、引擎和架构路线、影响后续实施的选择、范围变化及需要大量返工的决定。
guided 对重大选择提供至多两个清晰方案及推荐。
章节顺序、表达结构、已批准方向内的细化、可选说明章节及普通下一步路由属于细节。

## 必须询问类别

只对 `modes.automation_always_ask` 实际配置的类别强制询问，默认三个：`scope_changes`、`file_deletions`、`schema_changes`。
可配置的其他类别为 `architecture_decisions`、`version_bumps`、`external_calls`；未配置的类别不能假定为当前项目的硬性门禁。
`is_always_ask_category <category>` 是 source 后可用的 Bash 函数，不是 yaml-helper.sh 的直接子命令。返回 0 表示命中当前配置，1 表示未命中，不能把 1 当成执行故障。

在目标项目目录内运行，使用本 checkout 的真实 helper 路径；跨项目时先切换到目标项目，再 source helper 的绝对路径。Windows 从 PowerShell 进入 Git Bash 的方式见 `codex-runtime.md`。

```bash
source .agents/scripts/yaml-helper.sh
if is_always_ask_category scope_changes; then
  printf '%s\n' 'Required category: resolve the decision using current authorization.'
fi
```

该查询只决定类别是否要求明确决定；它不会发起提问，也不生成授权。已有同范围明确授权仍可复用。

scope_changes 包含删减验收条件、切换范围或改变交付承诺；schema_changes 指结构或模板变化。
追加实体注册表中的事实或更新已有配置值不自动等同于结构变更；按实际影响和项目已明确授权判断。

## 始终协作的工作流

`hotfix`、`gate-check`、`day-one-patch`、`setup-engine` 保留其明确协作阶段，即使全局设为自主模式也不跳过必要决定。
它们同样复用当前会话已有的明确决定，不能将客户端权限或范围变更默认为已授权。

## 决策日志

autonomous 模式把原本会交给用户的选择写入 `production/session-logs/decision-log.md`，使用 yaml-helper.sh 的 `log_decision`。
每项包含时间、Skill、Decision point、Options considered、Chosen、Reason、Category。
该函数同样必须先 source；严格传入六个位置参数，依次是 Skill、Decision point、Options considered、Chosen、Reason、Category。以下为已实际作出决定后的调用示例，不得把示例直接记作本项目的决定：

```bash
source .agents/scripts/yaml-helper.sh
log_decision "next-step" "Choose next approved task" "Task A; Task B" "Task A" "Its dependencies are complete" "workflow_routing"
```

检查命令状态及实际日志产物；无法写入时报告缺失，不能声称决定已记录。不要使用 `bash yaml-helper.sh log_decision ...` 或 `bash yaml-helper.sh is_always_ask_category ...`，直接入口不导出这两个函数。
记录实际选择，包括与推荐不同的决定；一次组合问题可合并一项，普通文件写入确认并入它所实现的决定，不另写重复日志。
日志是可核对的产物，不是事后补造授权的依据；原有记录保留，追加新决定。
