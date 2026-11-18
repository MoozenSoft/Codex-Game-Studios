# Signal Tiles Web 迁移验收

起点：`one-shot/signal-tiles`（`337ca73343e3b2a7ab4927dfbc0fe47f73475ea8`）。
流程输入中的 PROCEED / Keep going / Grow it 是受控模拟，不是人工试玩结论。

| 步骤 | 实际结果 |
| --- | --- |
| 1. 冻结基线 | Chrome 同种子重放两次，`exact yes`，0 错误；[原型截图](reference.png)。 |
| 2. JavaScript 副本 | `npm ci --prefer-offline` 安装 47 个包；单文件构建成功，`match yes`，0 错误；[副本截图](copy.png)。 |
| 3. TypeScript | 严格类型检查和单文件构建成功，`match yes`，0 错误；[TypeScript 截图](typescript.png)与基线并排核对。 |
| 4. 自动化测试 | 故意移除加分时两个单测均失败；恢复后 Vitest 2/2、Playwright 3/3 通过，覆盖待机、胜利、同种子重放、键盘长按与重置。 |
| 5. Web 登记 | 写入 Web / Vite 8.3.4；保留现有版本参考。生产构建成功，工作室 runner 返回 `web:pass`（5/5），冒烟通过（1/1）。 |

- NOT ASSESSED：真实人工试玩与玩法体验。
- `Loose`：无。
- 不改动原型快照；未发布。迁移阶段提交及 `grown/signal-tiles` 未执行。
