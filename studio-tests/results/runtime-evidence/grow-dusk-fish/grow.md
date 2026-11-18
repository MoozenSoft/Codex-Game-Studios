# dusk-fish grow 记录

起点：`5237684`，tag `one-shot/dusk-fish`；reference 提交 `5b90e81`。沿用上一轮的 guard 与 reference，不重跑；本轮从修复后的 copy 构建接续。首轮 ART 丢失的失败结论保留在 `../core-grow-result.md`；框架修复由主迁移会话完成，本轮没有修改框架。

| 步骤 | 结果与证据 |
| --- | --- |
| 1 reference | 上一轮 seed=721、3600 steps 两次运行 exact=yes、errors=0；原有 reference 未改 |
| 2 copy | 本轮 build:single 退出 0；copy 回放 errors=0、match=yes；提交 ad655cf |
| 3 TypeScript | strict 保持开启，ART 完整迁入 art.ts；main/config/config-source 三个过渡 JS 迁完后删除；回放 errors=0、match=yes；提交 41f6f4e |
| 4 tests | 胜利阈值故意 >=→> 时 1 failed / 5 passed；恢复原规则后 npm test：Vitest 6/6、Playwright 4/4；提交 6d50a7d |
| 5 record | engine written Web 8.3.4，版本参考 written；build 退出 0；test-run.sh web 报 web:pass，10/10；smoke 1/1，退出 0 |

已查看 `typescript.png` 与 `reference.png`，画面与回放一致，均为三鱼胜利。copy 的 ART 启动回归已在真实 Chrome 中消失。原型目录使用 `../core-grow/prototype-before.json` 对比，31/31 文件不变。

Loose：无；没有 any 别名或未类型化的 entity。src/game 中的计时、判定、配额、随机序列为无浏览器依赖的纯规则；screen、input、art、config、state 类型与 main 场景循环分开。没有音频需求，无 audio 模块。

NOT ASSESSED：人工试玩、主观乐趣/难度、长时间稳定性、跨浏览器和发布部署。自动验收通过不构成 PROCEED。

交接：`npm run dev` 启动开发服务器并打开输出的本机地址；反引号或 `?tune` 打开开发调参面板。保存块可用 one-shot-tune.sh 写入 data/config.json 与 design/feel-log.md。`npm run build` 输出 dist/，`npm test` 运行 Vitest 后运行真实 Chrome Playwright，`npm run smoke` 只运行 @boot。这些不是人工试玩结论。

下一项已批准的普通单功能：胜利或失败画面按 R 重试，Enter 保持，游玩中 R 不重置。按单次功能实现、先运行能失败的行为测试，再验证与提交，不创建 Story 流程。
