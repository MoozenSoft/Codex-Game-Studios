# 项目技术约定

`project.yaml` 保存引擎、语言、专业角色、命名、平台、性能及测试配置。
本文件保留未写入配置键的人工约定；配置键缺失时，解析器按原有规则读取这里的旧格式值。
`Forbidden Patterns` 与 `Allowed Libraries / Addons` 仍在这里维护。

以下英文标题与字段被脚本解析，是数据接口，填写时保留其拼写；方括号占位符表示尚未配置。
引擎设置流程填写实际值，同时更新项目配置与版本参考。

## Engine & Language

- **Engine**: [TO BE CONFIGURED — 使用 $setup-engine]
- **Language**: [TO BE CONFIGURED]
- **Rendering**: [TO BE CONFIGURED]
- **Physics**: [TO BE CONFIGURED]

## Input & Platform

交互设计、测试和开发流程读取此处以确定输入设备范围。

- **Target Platforms**: [TO BE CONFIGURED]
- **Input Methods**: [TO BE CONFIGURED]
- **Primary Input**: [TO BE CONFIGURED]
- **Gamepad Support**: [TO BE CONFIGURED]
- **Touch Support**: [TO BE CONFIGURED]
- **Platform Notes**: [TO BE CONFIGURED]

## Naming Conventions

- **Classes**: [TO BE CONFIGURED]
- **Variables**: [TO BE CONFIGURED]
- **Signals/Events**: [TO BE CONFIGURED]
- **Files**: [TO BE CONFIGURED]
- **Scenes/Prefabs**: [TO BE CONFIGURED]
- **Constants**: [TO BE CONFIGURED]

## Performance Budgets

- **Target Framerate**: [TO BE CONFIGURED]
- **Frame Budget**: [TO BE CONFIGURED]
- **Draw Calls**: [TO BE CONFIGURED]
- **Memory Ceiling**: [TO BE CONFIGURED]

## Testing

- **Framework**: [TO BE CONFIGURED]
- **Minimum Coverage**: [TO BE CONFIGURED]
- **Required Tests**: 数值公式、游戏机制，以及适用的网络行为

## Forbidden Patterns

- [尚未配置；随架构决策补充本项目禁止使用的实现模式]

## Allowed Libraries / Addons

- [尚未配置；只登记本项目已经批准的依赖]

## Architecture Decisions Log

- [尚无 ADR；此处保存指向 docs/architecture/ 中完整决策的索引]

## Engine Specialists

引擎配置流程维护角色选择。代码和架构评审按此路由；未配置的细分角色回退到 Primary。

- **Primary**: [TO BE CONFIGURED — 使用 $setup-engine]
- **Language/Code Specialist**: [TO BE CONFIGURED]
- **Shader Specialist**: [TO BE CONFIGURED]
- **UI Specialist**: [TO BE CONFIGURED]
- **Additional Specialists**: [TO BE CONFIGURED]
- **Routing Notes**: [TO BE CONFIGURED]

### File Extension Routing

| File Extension / Type | Specialist to Spawn |
| --- | --- |
| Game code (primary language) | [TO BE CONFIGURED] |
| Shader / material files | [TO BE CONFIGURED] |
| UI / screen files | [TO BE CONFIGURED] |
| Scene / prefab / level files | [TO BE CONFIGURED] |
| Native extension / plugin files | [TO BE CONFIGURED] |
| General architecture review | Primary |
