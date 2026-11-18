# dusk-fish 核心 grow CLI 验收

2026-11-16，当前隔离项目真实 CLI 执行。**整体 FAIL：grow 停在 copy 的浏览器等价性检查。** 45 秒反馈修改、原型基线、guard 和 reference 通过；未完成 grow，不可交接为可用生产工程。人工试玩 **NOT ASSESSED**，没有 PROCEED 决定。

## 范围、模式与授权

- 开始先执行 `Get-Location`，结果为 `<probe>`；`git rev-parse --show-toplevel` 同样指向此隔离目录。没有 `.codegraph/`，未使用 CodeGraph。
- 使用本目录 `.agents/skills/prototype/SKILL.md`（本地验收路径，未随证据归档）、`.agents/skills/prototype/references/one-shot-4-change.md`（本地验收路径，未随证据归档）、`.agents/skills/prototype/references/one-shot-files.md`（本地验收路径，未随证据归档）、`.agents/skills/prototype/references/one-shot-5-grow.md`（本地验收路径，未随证据归档），以及本地 runtime、automation 约定；未使用插件同名 Skill，未启用子代理。
- 显式运行 `yaml-helper.sh resolve_config --keys review_mode,automation,automation_always_ask,workflow`：`automation=collaborative (default)`、`workflow=minimal`、`review_mode=solo`；必须询问类别为 scope_changes、file_deletions、schema_changes。显式运行 rule-routing，加载 `.agents/rules/prototype-code.md`。
- 复用用户本轮对 change、指定路径基线提交、grow、锁文件安装及 R 重试的明确授权，无重复提问。此前不 grow/npm/提交的限制保留在 brief 原始请求记录中，当前有效边界已更新；反馈明确标为自动验收输入，没有冒充人工试玩。
- 未修改 `.agents`、`.codex`、`AGENTS.md`、检查器、全局配置、账号设置或外层仓库；未 push。Git staging 使用明确路径，没有 `git add -A`。未执行 `py`、`py list`、安装器或全局安装。
- Git Bash 在沙箱内无输出退出 1；后续经执行权限审核在同一 cwd 启动现有 Bash，未遭自动审核拒绝。命令记录器逐次断言 cwd，TMP/TEMP/TMPDIR 固定到隔离目录 `.tmp`，npm 缓存固定到 `.npm`，`PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`。

## 实际结果

| 环节 | 结果 | 可复核证据 |
| --- | --- | --- |
| change | PASS | `duration=45`、`quota=3`，其它配置和原型游戏代码未改变；两个 brief 同步当前规则 |
| 45 秒失败 | PASS | [timeout 日志](prototype/iteration-1-timeout.tsv)：step 2702 进入 over，t=45；[截图](prototype/iteration-1-timeout.png) |
| 仍可三鱼获胜 | PASS | [win 日志](prototype/iteration-1-win.tsv)：step 184 进入 results，t=3.05、score=3；[截图](prototype/iteration-1-win.png) |
| 小窗口文案 | PASS | [800×450 标题截图](prototype/iteration-1-small.png)显示 45 秒和三鱼，文字均 inside；已查看 |
| Keep 检查 | PASS（空列表） | helper 报 `keep lines 0 pinned 0`；未增加虚构的玩家偏好，艺术方向和 Avoid 约束保留 |
| 原型基线与 guard | PASS | `5237684`，仅 prototypes/dusk-fish 与 design/game-brief.md；node/engine/root/git/clean 均 pass |
| grow step 1：reference | PASS | seed=721、3600 steps，两次真实 Chrome 回放 `exact yes`、errors=0；[reference.tsv](grow-dusk-fish/reference.tsv)、[第二次](grow-dusk-fish/reference-again.tsv) |
| grow step 2：copy | FAIL | 脚本生成成功、npm ci 成功、build:single 成功；浏览器 `ART is not defined`，`errors 2`、`match no`；[copy.tsv](grow-dusk-fish/copy.tsv) |
| grow step 3：TypeScript 拆分 | NOT ASSESSED | 因 copy 失败未执行；未创建 game rules 或完成 strict 类型迁移 |
| grow step 4：规则和 Playwright 测试 | NOT ASSESSED | 未到达该阶段，未创建正式测试，未执行破坏规则再恢复的红绿验证 |
| grow step 5：record | NOT ASSESSED | 未运行 record，未写入 Web engine/version，未打 grown/dusk-fish tag |
| grow step 6：交接 | 未完成 | 生成工程黑屏，不能宣称可玩；原型入口仍可用 |
| grow 后 R 重试 | NOT ASSESSED | grow 未成功，未建立行为测试、未实现、未运行 story replay 或 accept；未创建 Story 流程 |

首次获胜输入的第三次 Space 时机不合适，只钓到两条；保留 [change-win.log](core-grow/raw/change-win.log)。修正固定输入时序后获胜，没有为让测试通过修改判定规则。自动运行也不等于人工试玩或乐趣验证。

## 真实缺陷与最小复现

原型 `prototypes/dusk-fish/config.js`（本地验收路径，未随证据归档） 除 `window.CONFIG` 外还定义 `window.ART`（绘图坐标、颜色和样式）。copy 在 `.agents/scripts/one-shot-grow.sh:276` 只提取 `sb.window.CONFIG`，删除原 config.js script tag 后，生成的 `src/config.js:7` 仅设置 `window.CONFIG = data`。`src/main.js:63` 保留 `const A = ART, C = A.colors, S = A.style;`，因此启动立即异常。copy 没有对被遗漏的 ART 发出 `left` 或 `config_lost` 提示。

原型两次 reference 都正常，生成工程在同一 Chrome 中失败；最小诊断也独立确认原配置有 CONFIG、ART，而生成配置只有 CONFIG。构建器对 JavaScript 未发现此运行时引用错误，构建退出 0 不代表游戏通过。

当前保留产物可直接复现，无需再次 copy：

```bash
npm run build:single
bash .agents/scripts/one-shot-grow.sh replay dusk-fish --as copy
node production/qa/evidence/core-grow/raw/minimal-repro.mjs
```

执行环境需沿用下文指定路径。前两条实际退出 0，但第二条输出 `match no`；第三条退出 1，抛出相同 ReferenceError。[最小复现脚本](core-grow/raw/minimal-repro.mjs)仅本地保留，不提交；[输出](core-grow/raw/minimal-repro.log)记录原始错误。它是针对生成配置的诊断，不计入正式规则测试。

停步依据是用户明确要求“若脚本有真实缺陷，保留最小复现并停止受影响步骤”，同时符合本地 grow 引用的 “A failed check stops the grow at that step”。因此没有修补框架、调整原型去迁就 copy、手工补 ART 绕过失败、继续 TS/record 或声称 grow 成功。失败 copy 的工程文件留在工作区，未提交为成功的迁移步骤。

已查看 [reference.png](grow-dusk-fish/reference.png)（正常三鱼胜利）和 [copy.png](grow-dusk-fish/copy.png)（黑屏），不能声称只有预期变化发生：迁移导致了非预期启动回归。R 功能尚未进行，无该功能的预期变化结论。

## 命令与退出码

完整 argv、cwd、时间、耗时、退出码见 [commands.jsonl](core-grow/raw/commands.jsonl)，原始 stdout/stderr 合并保留在 [raw](core-grow/raw) 内。下表省略公共的 `bash .agents/scripts/` 前缀；组合命令完整内容以 JSONL 为准。

| 命令/记录标签 | 实际退出码 | 观察 |
| --- | --- | --- |
| preflight：工具版本、配置解析、Git 状态、`one-shot-check.sh prototypes/dusk-fish --keep` | 0 | collaborative；无 Keep pin |
| `one-shot-run.sh prototypes/dusk-fish ... --log "Enter wait:46" --stop 2762` | 0 | 45 秒超时 |
| `one-shot-run.sh ... --log "Enter wait:0.45 Space wait:1.15 Space wait:2.2 Space wait:1" --stop 400` | 0 | 输入未达获胜，score=2，非成功获胜证据 |
| `one-shot-run.sh ... --log "Enter wait:0.45 Space wait:1.15 Space wait:1.25 Space wait:1" --stop 400` | 0 | score=3，results |
| `one-shot-run.sh ... --log "wait:0.1" --size 800x450` | 0 | 标题显示 45 秒 |
| baseline：限定路径 add/commit 与 `one-shot-grow.sh guard dusk-fish` | 0 | guard 全 pass |
| `git tag one-shot/dusk-fish` 与 `one-shot-grow.sh replay dusk-fish --as reference --log "Enter wait:0.45 Space wait:1.15 Space wait:1.25 Space wait:56"` | 0 | 两次 run 各 0，exact yes |
| reference-commit：仅提交 grow-dusk-fish reference 文件夹 | 0 | `5b90e81` |
| `one-shot-grow.sh copy dusk-fish` | 0 | 生成工程，27 config entries / 26 sliders，无 left 提示 |
| `npm ci` | 0 | 安装锁定的 47 个包，未执行 npm 升级提示 |
| `npm run build:single` | 0 | tsc 与 Vite 完成，dist-single/index.html 生成 |
| `one-shot-grow.sh replay dusk-fish --as copy` | 0 | 内部 run 0；errors=2、uncaught=1、match no，属于失败 |
| `node .../minimal-repro.mjs` | 1 | 预期复现 ReferenceError |
| final-audit：哈希、`npm ls --depth=0`、Git 提交路径/状态/tag、版本 | 0 | 原型 31/31 文件一致，无暂存文件 |

Skill 最终检查 `npm run build`、`npm test`、`npm run smoke`、`bash .agents/scripts/test-run.sh web`：**均未执行 / NOT ASSESSED**，原因是 copy 的真实缺陷触发停步，不是通过，也不存在 `web:pass`。没有为了填满检查表在缺少迁移测试的阶段运行空测试。正式规则单测数量 **0（未建立/未运行）**，正式 Playwright 测试数量 **0（未建立/未运行）**，smoke 数量 **0（未运行）**。本轮官方 one-shot 浏览器运行共 7 次（change 四次、reference 两次、copy 一次），不能冒充 Vitest/Playwright 测试数量。

## 环境、冻结与提交

- Node `v24.14.0`，npm `11.9.0`，Python `3.12.10`，Chrome `157.0.0.0`。Python 使用 `%LOCALAPPDATA%/Python/pythoncore-3.12-64/python.exe`；浏览器使用 `C:/Program Files/Google/Chrome/Application/chrome.exe`；Bash 使用 `D:/Program Files/Git/bin/bash.exe`。Node/npm 沿用当前 PATH 已有安装。
- 锁定开发依赖实际安装：`@playwright/test@1.64.1`、`typescript@7.0.2`、`vite@8.3.4`、`vite-plugin-singlefile@2.3.3`、`vitest@5.0.5`。没有缺依赖或自动浏览器安装；框架 copy 错误是本轮阻塞。
- guard 通过、grow 开始时冻结原型目录全部 31 个文件（含 evidence），随后没有再写入原型。对比：[before](core-grow/prototype-before.json)、[after](core-grow/prototype-after.json)、[comparison](core-grow/prototype-comparison.json)：`unchanged=true`、`differences=[]`。原型和主 brief 的 Git 状态均干净。
- 提交 `5237684`：中文标题“原型迭代一：单局改为四十五秒并保存验收基线”，32 个文件，仅限 prototypes/dusk-fish 和 design/game-brief.md；这包括上一轮由本测试创建、此前未提交的原型自有文件。
- 提交 `5b90e81`：中文标题“验收：保存 dusk-fish 同种子迁移参考回放”，仅 5 个 reference 证据文件。tag `one-shot/dusk-fish` 指向 `5237684`。无 AI 署名尾注，无 grown tag。
- 未提交框架副本、驱动脚本、runtime-cases、个人文件或失败 copy 的工程。项目原有未知文件保持原状；没有用隐藏、删除或提交未知内容绕过 guard。
- 用户要求的报告、原始日志、哈希和最小复现均保留在 evidence；生成的 npm 缓存、依赖与临时运行目录仅在隔离项目内。

原型可继续通过 `prototypes/dusk-fish/index.html` 打开。生成工程的 `npm run dev`、build/test/smoke 属于尚未完成的交接，当前不能推荐其作为已验收游戏入口。下一项前置工作是在独立框架修复任务中处理 copy 对 config.js 非 CONFIG 数据的遗漏，然后重新验收此阶段；本次按要求不修框架。
