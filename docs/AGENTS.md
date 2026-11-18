# 项目文档规范

ADR 使用 `.agents/docs/templates/architecture-decision-record.md`。必要章节包含 Title、Status、Context、Decision、Consequences、ADR Dependencies、Engine Compatibility、GDD Requirements Addressed。
状态依次为 `Proposed` → `Accepted` → `Superseded`；故事引用的决策未 Accepted 时不能当作开发前置条件满足。

`docs/architecture/tr-registry.yaml` 中的 TR ID 稳定，只增补，不重新编号；它连接 GDD 需求与故事。
`docs/architecture/control-manifest.md` 保存每层 Required、Forbidden、Guardrails；故事记录其日期标记的 `Manifest Version:`，完成验收时检查过期。

引擎参考按 `project.yaml` 固定版本维护在 `docs/engine-reference/<engine>/`，`<engine>` 为 godot、unity、unreal 或 web。
使用引擎 API 前读取对应版本参考；资料缺失时记录未评估，不能将猜测写成运行证据。

方案和实施文档优先中文。保留机器读取的标题、标识符与配置键；历史上游资料的来源和许可证不得移除。
