# 模型与推理配置

上游 Opus 指定点使用 `astra` 家族，Sonnet 指定点使用 `sol` 家族。来源提交、原字段、文件哈希和对应路径见 [模型迁移清单](../../studio-tests/fixtures/model-routing.json)。

## 解析最新可用版本

在本次执行或委派前解析所需家族。同一轮或同一个评审面板可复用一次成功结果。下一次独立调用重新解析。

```bash
bash .agents/scripts/python-run.sh .agents/scripts/model-routing.py astra
bash .agents/scripts/python-run.sh .agents/scripts/model-routing.py sol
```

Windows PowerShell 按 [运行约定](codex-runtime.md#windows-powershell-的-bash-入口)使用实际 Git Bash。解析器查询 Codex App Server 的 `model/list`，读取所有页面，在当前提供方可见的正式型号中按数字版本排序。需要使用其他已配置提供方时传 `--provider <id>`。 [目录接口](https://learn.chatgpt.com/docs/app-server#list-models-modellist)

当前客户端已提供可核实的完整目录时，可复用它。完整 `model/list` 结果对象通过标准输入传给 `--catalog-stdin`。同一执行后端明确列出的可选 ID 可作为 JSON 数组传给 `--available-stdin`。委派接口的列表用于该接口，当前会话的选模器列表用于 Skill 会话。只传实际列出的型号。

退出 0 且 `status` 为 `resolved` 时使用返回的 `model`。查询失败、检测到刷新失败、家族缺失或目录不完整时，退出 2 并返回 `not_assessed`。这时报告模型未能确认，等待能核实的当前目录或用户明确选择。Codex 目录可能来自客户端缓存，结果只说明所查目录中的最新可用版本。

## 角色模型

- 调用方先读取角色 TOML 的 `developer_instructions`。声明 **Model family** 时解析型号，并在实际支持的委派接口中同时传入规范角色名和 `model`。角色 TOML 省略原生 `model` 字段，让调用时的模型参数生效。
- 只有通用委派可用时，载入该 TOML 的角色指令并传入同一解析结果。接口无法传入相应型号时，报告该角色未按要求运行，按工作流处理缺失结果。没有家族要求的角色使用会话默认模型。
- 项目配置维持会话默认值。`model_reasoning_effort` 由 Codex 根据客户端配置解析。用户另有指定时用实际支持的参数，并记录能核实的运行值。角色共享父会话的权限限制。 [Codex 原生角色配置](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents)

## Skill 会话模型

读取 Skill 正文的 **会话模型要求**。先解析该家族，再确认会话使用解析出的型号。适用于直接调用和代用户执行。没有这项要求的 Skill 使用当前会话模型。原型的 Web one-shot 在直接构建前单独解析 Astra。

以客户端显示、会话元数据或明确的启动参数为依据。当前模型与解析结果不同时，通过客户端提供的选模入口切换。需要用户操作时，提示通过 CLI `/model <解析出的模型 ID>` 或模型选择器确认，随后按已有授权继续。CLI 自动化可用 `codex exec -m <解析出的模型 ID> '$<skill> …'` 启动。 [Codex 模型选择](https://learn.chatgpt.com/docs/models?surface=cli)

`SKILL.md` 的模型要求属于工作流入口指令。Skill frontmatter 与 `agents/openai.yaml` 的原生元数据不提供会话模型覆盖字段。 [Codex Skill 结构](https://learn.chatgpt.com/docs/build-skills)
