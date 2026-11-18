# 设计产物规范

先解析 `modes.workflow`。full 要求 8 个 GDD 章节；standard 要求 Overview、Detailed Rules、Edge Cases、Dependencies、Acceptance Criteria，机制包含数值规则时另需 Formulas；minimal 使用 `design/game-brief.md`，不强制 GDD。
完整 8 章为 Overview、Player Fantasy、Detailed Rules、Formulas、Edge Cases、Dependencies、Tuning Knobs、Acceptance Criteria。`Detailed Design` 与 `Detailed Rules` 为同一章节的合法别名。

GDD 文件使用 `[system-slug].md`，新增系统同步 `design/gdd/systems-index.md`；按 Foundation → Core → Feature → Presentation → Polish 设计。
公式明确变量和例算；依赖双向记录；验收标准可判定通过或失败。写作确认步骤遵守当前协作模式和已有会话授权。

轻量设计位于 `design/quick-specs/`；界面规格位于 `design/ux/[screen-name].md`，HUD 为 `design/ux/hud.md`，交互库为 `design/ux/interaction-patterns.md`。
项目级无障碍要求固定为 `design/accessibility-requirements.md`，不要挪入 UX 子目录；阶段门禁和架构检查使用这个路径。
编辑设计或叙事文档时读取规则选择器返回的 `.agents/rules/design-docs.md`、`narrative.md` 等适用规则。
