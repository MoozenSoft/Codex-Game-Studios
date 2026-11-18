# 文件领域规则选择

Codex 的目录 AGENTS.md 承载局部规范；跨目录规则由共享选择器按目标路径加载。

```text
python .agents/scripts/rule-routing.py src/gameplay/movement.ts Assets/Game/UI/Menu.cs
```

读取输出列出的规则，再编辑对应文件。选择器直接解析 `.agents/rules/*.md` 的 `paths`，支持 `**`、`*`、`?` 与 `{a,b}`，不维护另一份容易漂移的规则表。
规则覆盖 Web/Godot 的 src、Unity 的 Assets、Unreal 的 Source/Content，以及数据、shader、场景、设计、叙事、测试和框架维护。
没有规则匹配时仍遵守根及目录 AGENTS.md；规则路径越出项目时返回错误。
