已实现故事 001，五条验收标准均已验证。胜利后按 `N` 直接进入新一局，三格全暗、分数归零。其他场景按 `N` 不改变进度，`R` 仍按原规则回到待机。

- 修改源码前，新增单测和 Playwright 用例都在按 `N` 后的状态断言上按预期失败。
- 实现后，完整测试通过，Vitest 3/3、Playwright 6/6。Web 冒烟 1/1，框架校验通过。
- grow 同种子重放与原参考一致，零错误，截图哈希一致。已核对原型及其快照未变，未发布。

故事保留 `In Progress`，实际验收结果已写入会话检查点。人工试玩未评估。[验收记录与截图](<gap-fixtures>/fresh-game/production/qa/evidence/story-001-restart-from-victory/verification.md)

```text
Story: production/epics/signal-tiles/story-001-restart-from-victory.md — Implemented
Run result: OBSERVED — 按 N 后显示「正在点亮」、0 分、三格暗。production/qa/evidence/story-001-restart-from-victory/02-restarted.png
Same-seed run: SAME — match yes，errors 0。production/qa/evidence/grow-signal-tiles/story.png
Next step: $story-done production/epics/signal-tiles/story-001-restart-from-victory.md
```
