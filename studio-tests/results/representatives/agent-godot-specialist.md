# agent-godot-specialist 验收报告

- 场景结果：`passed`。完成给定参考范围内的静态核对，并保留原生引擎运行未验证。
- 实际角色：通过项目角色 `godot-specialist` 真实绑定运行，读取当前隔离项目 `.codex/agents/godot-specialist.toml`、`.agents/docs/codex-runtime.md` 与 `.agents/docs/coordination-rules.md`；未使用其他插件 Skill，未再委派。
- 输入根：`runtime-cases/agent-godot-specialist`，输入仅为该根下 `project.yaml`、`engine-reference.md`、`sample.gd`。未借用其他案例或共享项目的引擎配置。

## 实际行为与工具证据

显式读取项目配置后，执行共享 helper：

```text
D:/Program Files/Git/bin/bash.exe .agents/scripts/yaml-helper.sh --root <cases>/agent-godot-specialist resolve_config --keys automation,workflow,review_mode,team.size,engine_values
exit: 0
review_mode: solo (rigor:minimal)
automation: collaborative (project.yaml)
workflow: minimal (rigor:minimal)
team.size: individual (rigor:minimal)
engine_values: name=Web(project.yaml) version=unset language=unset
```

Git Bash 使用已获自动审核通过的沙箱外只读执行方式；PATH 优先指向已有 Python 3.12，不安装依赖。首次批量读取命令返回 1：最后的可选参考目录不存在，前面的文件内容已成功返回；随后用已有 Python 解释器逐行读回与显式存在性检查，退出 0。

`engine-reference.md:2` 规定“Godot 4：场景脚本可 extends Node”，并明确没有运行或导出证据。`sample.gd:1` 实际为 `extends Node`，符合这条给定规则。Python 静态包含检查输出 `STATIC extends Node: True`，参考无运行证据检查输出 `True`。`sample.gd:3-4` 仅可观察到 `_ready()` 打印 sample 的代码文本，不能据此判定它已执行。

## 适用性与预期

配置 `project.yaml:5-6` 和解析器均确认 `engine.name: Web`。因此 Godot specialist 不是该项目实际引擎的适任整体评审者；本次仅依明确请求核对独立 Godot 样例与给定参考，不切换项目引擎，也不将此结果扩展为 Web 或 Godot 项目批准。

预期满足：实际核对了可验证规则；明确报告配置冲突、参考缺失和无法运行项目；没有声称编辑器、解析器、游戏或导出通过。只写本报告，未改 `sample.gd`、配置、阶段或框架文件。

## 未评估项

- 原生引擎运行：`NOT VERIFIED`。本案例无编辑器，未启动 Godot、运行 `_ready()`、检查控制台输出或导出构建。
- GDScript 语法/类型检查与场景加载：`NOT ASSESSED`，没有调用 Godot 解析器；静态读取不等于解析通过。
- Godot 精确版本、弃用 API、版本迁移和当前最佳实践：`NOT ASSESSED`。显式检查以下案例相对路径均为 ABSENT：`docs/engine-reference/godot/VERSION.md`、`deprecated-apis.md`、`breaking-changes.md`、`current-best-practices.md`。不从记忆补充版本 API 结论。
- 静态类型、信号、资源释放、节点架构、性能等更宽角色规则：未作验收裁决，给定 `engine-reference.md` 不提供这些规则，用户限定仅依据该参考。

CONCERNS：项目实际引擎为 Web；本报告只证明给定样例满足参考中的一条静态规则。无须新增授权的阻塞项。
