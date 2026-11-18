**Signal Tiles 已在隔离仓库迁移为 Vite + TypeScript Web 项目，并完成自动验证。** 运行 `npm run dev`，打开终端显示的地址即可试玩；也可直接打开 `dist-single/index.html:1` 离线玩。

- **行为一致：** 两次 Chrome 基准重放完全一致；JavaScript 副本和 TypeScript 版均匹配基线，最终截图的 SHA-256 也相同。
- **验证通过：** `npm test` 5/5，`npm run smoke` 1/1；生产构建和框架校验均通过。详情见 `production/qa/evidence/grow-signal-tiles/grow.md:1`。
- **快照未变：** `one-shot/signal-tiles` 仍指向 `337ca73`。本次迁移未提交、未打 `grown/signal-tiles` 标签，也未发布。

真实人工试玩仍为 **未评估**；模拟 PROCEED 不计为试玩结论。
