# app-dusk-fish Grow 记录

原型提交：83646f5，one-shot/app-dusk-fish。自 Grow 开始整个目标原型冻结，清单在 ../app-acceptance/frozen-prototype.json。

| 步骤 | 实际结果 |
|---|---|
| guard/reference | Node 24.14.0，四项 guard pass；双跑 exact yes、errors 0 |
| copy | npm ci 使用项目 .npm、锁文件；build:single 退出0，match yes |
| TypeScript | strict 保持；ART、配置、输入、绘制、状态及纯规则拆分；三个过渡JS已删除；match yes |
| 规则与浏览器 | 规则破坏：2 failed/1 passed；恢复：Vitest 3 passed，真实Chrome Playwright 2 passed |
| record/检查 | engine Web/Vite 8.3.4；npm run build 退出0；test-run web:pass，5/5；npm run smoke 退出0 |

reference.png、copy.png、typescript.png 已打开比较；归一化逐步状态及画面 hash 相同。未使用 Loose/any 状态别名。TypeScript 首次构建的元组展开类型错误已修复，编译及回放复验通过。

NOT ASSESSED：人工试玩、操作体验、乐趣与完整人工 smoke。自动验收输入不视为人工试玩，不作 PROCEED 或发布判断。

运行：npm run dev；构建：npm run build；测试：npm test；启动门禁：npm run smoke。
