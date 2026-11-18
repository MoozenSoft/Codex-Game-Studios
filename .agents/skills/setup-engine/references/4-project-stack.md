# $setup-engine — Section 4: 记录引擎配置

> Part of `$setup-engine`. `SKILL.md` names when to read this file; the settings it
> resolved and the rules under its later headings still apply here.

## 4. 记录引擎配置

### Language Selection (Godot only)

If Godot was chosen, ask the user which language to use **before** showing the proposed Technology Stack:

> "Godot supports two primary languages:
>
>   **A) GDScript** — Python-like, Godot-native, fastest iteration. Best for beginners, solo devs, and teams coming from Python or Lua.
>   **B) C#** — .NET 8+, familiar to Unity developers, stronger IDE tooling (Rider / Visual Studio), slight performance advantage on heavy logic.
>   **C) Both** — GDScript for gameplay/UI scripting, C# for performance-critical systems. Advanced setup — requires .NET SDK alongside Godot.
>
> Which will this project primarily use?"

Record the choice. It determines the project.yaml 与技术约定, naming conventions, specialist routing, and which agent writes code files throughout the project.

### Primary Language (Unreal)

If Unreal was chosen, ask: "Will most gameplay logic live in
C++ or in Blueprints?" — `[A] C++ (Blueprints for tuning and prototyping)` /
`[B] Blueprint-primary (C++ only where needed)`. Default to C++ if the user has no
preference. The answer sets `engine.language` (`"C++"` or `"Blueprint"`).

---

## 记录引擎与语言

展示拟定的 engine.name、engine.version、engine.language、代码/测试目录及构建命令，按协作模式和已批准范围写入 project.yaml。
将引擎、语言、输入方式和专业角色同步到 `.agents/docs/technical-preferences.md`，保持其中脚本读取的英文字段名。
使用 `docs/engine-reference/<engine>/VERSION.md` 保存固定版本和来源；不存在时按后续章节创建，存在时核对并保留用户约定。
根 AGENTS.md 保存模型、提交、权限和规则入口，不写入引擎状态或 @ 导入行。需要参考时显式读取该版本文件。
