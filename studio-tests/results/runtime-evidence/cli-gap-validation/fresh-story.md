已写入 [故事 001「胜利后按 N 立即重开」](production/epics/signal-tiles/story-001-restart-from-victory.md)。故事为 Logic，状态 Ready，预估 S。

故事将「重开」定义为从胜利画面直接进入新一局，三格全暗、分数清零。五条验收标准覆盖真实键盘输入、再次通关、N 在其他场景无效，以及 R 原有的待机重置行为。

已将需求登记为简报第 5 项待办，并更新 Epic 和会话检查点。框架校验退出码为 `0`，grow 的构建、重放和测试基线已核对。交付止于文档，N 键运行验收与人工试玩均待评估。

```text
Verdict: COMPLETE — 1 story written to production/epics/signal-tiles/ (1 Ready, 0 Blocked)
Review: QL-STORY-READY skipped — Solo mode
Index: Epics index not updated: production/epics/index.md absent
Next step: $dev-story production/epics/signal-tiles/story-001-restart-from-victory.md
```
