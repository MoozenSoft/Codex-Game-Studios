# dusk-fish 隔离 CLI 验收：第二轮

日期：2026-11-16。**游戏 grow 和 R 单功能验收 PASS；工作区完整性审计 CONCERNS。** 本轮从修复后的 copy 接续，完成 TypeScript 拆分、规则红绿测试、真实 Chrome 测试、record、交接及 R 重试。收尾发现 .codex/hooks 的未预期哈希变化，来源未评估，不能宣称整个框架目录不变。人工试玩 **NOT ASSESSED**，没有 PROCEED 决定。

## 接续范围与授权

开始先确认 cwd 为 `<probe>`。读取本目录 `.agents/skills/prototype/SKILL.md`、新版 `references/one-shot-5-grow.md`、本地 runtime/automation 约定；没有使用插件同名 Skill。没有 .codegraph/，不调用 CodeGraph。运行 rule-routing.py 后，该次目标路径没有额外命中的领域规则。

显式解析配置：collaborative（默认）、workflow=minimal、review_mode=solo；沿用用户已批准的 grow、删除生成的过渡 JS、测试、限定路径提交与 R 单功能范围，无重复询问；未切换模型、未委派子代理、未创建 Story/epic 流程。反馈、基线、guard、reference 均复用上一轮结果，没有重新生成。

框架 copy 修复是主迁移会话同步的输入，不是本轮修改。本轮没有编辑 `.agents`、`.codex`、AGENTS.md 或检查器；没有 push、全局配置变更、npm 安装/升级、运行时或浏览器安装。Python 始终为指定的 python.exe，没有执行 py 或安装器。仅删除本轮 copy 生成且引用已迁完的 src/main.js、src/config.js、src/config-source.js，没有删除原型或未知文件。

历史 [core-grow-result.md](core-grow-result.md) 保持字节不变，不回写其失败结论。本轮官方回放覆盖了当前 copy.png/copy.tsv，新的成功结论以本报告和 round2 原始日志为准；上一轮失败的 raw 日志和最小复现仍保留。reference 全套文件保持哈希不变。

## 实际执行结果

| 环节 | 实际结果 |
| --- | --- |
| 修复后的 copy | npm run build:single 退出 0；官方 replay --as copy 退出 0，errors=0、match=yes；原先 ART 未定义异常消失 |
| TypeScript 拆分 | strict=true；CONFIG 使用 data/config.json 的有类型 live tune；ART 全量迁入 src/art.ts（tuple 坐标），screen/input/game rules/state/main 分离，使用 scaffold hook；build:single 与 replay --as typescript 均退出 0，errors=0、match=yes |
| 规则红灯 | 故意将 hasWon 的 >= 改为 >，Vitest 退出 1，恰好 1 failed / 5 passed；三鱼配额边界被真实断言捕获 |
| 规则恢复和 grow 测试 | 恢复后 npm test 退出 0：Vitest 6/6、Playwright 4/4；正式测试读取 data/config.json，未把空测试当通过 |
| record | 官方 record 输出 engine written Web 8.3.4、engine_reference written；project.yaml 仅追加 engine，版本参考写到 docs/engine-reference/web/VERSION.md；不改根 AGENTS |
| grow 检查 | npm run build、test-run.sh web、smoke 全部退出 0；runner 为 web:pass，10/10（6 unit + 4 e2e）；smoke 1/1 |
| R 实现前 | 对旧构建运行真实键盘行为测试，退出 1：2 failed（两个结果画面的 R 均无效）/ 3 passed（Enter 和非结果场景行为原本正确） |
| R 实现后 | 仅在 over/results 判断中加入 KeyR，并更新这两个画面的重试提示；9 项 Playwright 全过，状态无直接篡改，真实 page.keyboard.press 驱动 |
| 单功能 replay | smoke、build:single、replay --as story 均退出 0、errors=0；画面 match=no 是预期提示文案变化，已核对并 accept |
| 最终完整检查 | npm run build、npm test、test-run.sh web、smoke 全部退出 0；6 unit + 9 e2e = **15/15**；runner 明确 web:pass、zero_tests=no、browser=started；smoke **1/1** |

规则测试覆盖配置截止时间、时间上限、收鱼区域含边界/区外、三鱼胜利阈值、往返判定针、seed 随机序列。grow 的浏览器测试覆盖 boot、reference 开场三鱼胜利及全状态/画面确定性、移动/暂停/恢复、零 seed 与非法 seed 回退。没有 Loose/any，也没有未迁完的 config-source.js 依赖；无音频需求，因此没有新增音频模块。

保留了两次实施中的失败：首个类型检查指出靴子坐标的 union tuple 不能直接 spread，改为显式索引后通过；第一轮 e2e 把官方按键节奏误译成三帧，导致胜利时间 3.00 与 reference 的 3.05 不符。读取运行器实际契约（两帧按下 + 两帧间隔），修正测试为四帧后通过。没有为这些检查修改游戏数值或框架。主动规则破坏与 R 旧行为测试的红灯均为预期负验证，已保留原始失败输出。

## replay 与单功能的预期变化

既有 reference：seed=721，3600 steps，固定输入为 `Enter wait:0.45 Space wait:1.15 Space wait:1.25 Space wait:56`；上一轮两次回放 exact=yes。本轮 copy、typescript 均匹配该 reference。

R 功能的 story 与同一个 reference 比较：首次差异为 frame 3481 的 hash（fa661e67 → 5cd95c32）。[玩法行比较](core-grow/round2/story-state-comparison.json)确认场景、状态、按键、终点和错误等共 10 行完全相同；[像素比较](core-grow/round2/story-pixel-comparison.json)确认仅 2433 像素变化，边界 x=513..768、y=393..407，位于结果提示文案。没有改变 quota=3、duration=45、运算顺序或玩法状态。

R 行为测试新增 5 项：胜利/失败 × R/Enter 共 4 项验证整个状态与初始状态相同（t/score/位置/判定针/冷却/目标/鱼群全部重置）；另 1 项验证 R 在标题、游玩和暂停均不重开，游玩状态与无 R 的对照完全一致。Enter 原行为保留。仅此次单功能预期的输入响应与结果文案变化发生；工作区 hooks 哈希变化是另列的范围审计异常，不混入游戏结论。

已查看 [typescript](grow-dusk-fish/typescript.png) 与 [reference](grow-dusk-fish/reference.png)，以及最终 [story 胜利画面](grow-dusk-fish/story.png)、[失败画面](core-grow/round2/retry-over-before.png)、[R 后新局](core-grow/round2/retry-results-after.png)。重试提示在框内，新局回到 45.0 秒、0/3；完整胜负 R 前后 JSON 和截图在 round2。已运行官方 accept，将预期的 story 作为后续 accepted 基准，未改 reference。

## 命令、退出码与测试数量

全部 runner 命令的完整 shell 文本、cwd、时间、耗时、退出码见 [commands.jsonl](core-grow/round2/commands.jsonl)；各次原始 stdout/stderr 合并保留于下表链接。命令通过已有 Bash 执行，环境绑定指定 Python/Chrome，npm cache 为本目录 .npm，TMP/TEMP/TMPDIR 为本目录 .tmp，并设置 PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1。没有运行 npm ci，因为锁定依赖已安装。

| 原始记录（含完整命令） | 退出码 | 秒 |
| --- | --- | --- |
| [copy-build](core-grow/round2/copy-build.log) | 0 | 10.046 |
| [preflight](core-grow/round2/preflight.log) | 0 | 1.297 |
| [copy-commit](core-grow/round2/copy-commit.log) | 0 | 1.609 |
| [typescript-check](core-grow/round2/typescript-check.log) | 1 | 0.938 |
| [typescript-replay](core-grow/round2/typescript-replay.log) | 0 | 7.656 |
| [typescript-commit](core-grow/round2/typescript-commit.log) | 0 | 1.157 |
| [rule-red](core-grow/round2/rule-red.log) | 1 | 0.969 |
| [tests-green](core-grow/round2/tests-green.log) | 1 | 12.672 |
| [tests-green-corrected](core-grow/round2/tests-green-corrected.log) | 0 | 7.484 |
| [tests-commit](core-grow/round2/tests-commit.log) | 0 | 1.047 |
| [record](core-grow/round2/record.log) | 0 | 15.406 |
| [grow-commit](core-grow/round2/grow-commit.log) | 0 | 1.39 |
| [retry-red](core-grow/round2/retry-red.log) | 1 | 13.75 |
| [retry-green](core-grow/round2/retry-green.log) | 0 | 8.204 |
| [story](core-grow/round2/story.log) | 0 | 13.86 |
| [story-compare](core-grow/round2/story-compare.log) | 0 | 4.437 |
| [final-checks](core-grow/round2/final-checks.log) | 0 | 26.203 |
| [feature-commit](core-grow/round2/feature-commit.log) | 0 | 1.719 |
| [audit-final](core-grow/round2/audit-final.log) | 1 | 0.203 |
| [git-final](core-grow/round2/git-final.log) | 0 | 0.953 |
| [scope-summary](core-grow/round2/scope-summary.log) | 0 | 0.141 |

copy-build：`npm run build:single` → `bash .agents/scripts/one-shot-grow.sh replay dusk-fish --as copy`。typescript-replay 同理使用 --as typescript。record：官方 record → npm run build → `bash .agents/scripts/test-run.sh web --log .../test-run-grow.log` → npm run smoke。story：smoke → build:single → replay --as story。final-checks：build → npm test → `test-run.sh web --log .../test-run-final.log` → smoke，链上各步均成功才继续。

最终去重测试数为 **15（6 Vitest + 9 Playwright）**，不是把多次执行相加。smoke 1 项是这 9 项中的 @boot 子集。官方 runner 再次执行的是同一套 15 项，不能额外计数。规则红灯 6 项（1 失败）、R 红灯 5 项（2 失败），分别记录负验证，不能混为通过。主迁移会话所称 11 项框架回归不是本轮执行结果，不加入本轮测试数量。

## 原型冻结、范围审计与提交

本轮继续使用上一轮 `core-grow/prototype-before.json`；开始、收尾两次比对均为 **31/31 文件完全一致、differences=[]**。原型包括所有旧 evidence，没有在 grow 后写入其中任何文件。[原型哈希结论](core-grow/prototype-comparison.json)。主 brief 的 Keep、Avoid、Out of scope、Look and references 与冻结原型 brief 逐字相同，只更新了已批准的生产结构与 R 操作内容。

额外范围审计保留了 597 个原始文件的哈希。22:14:11 全目录核对退出 1，记录 [immutable-comparison.json](core-grow/round2/immutable-comparison.json)：发现 .codex/hooks/dispatch.py、event_log.py 以及两个 pyc 与初始集合不同（集合共 599 文件）。只读元数据显示源码写入时间在 22:11:04–05，pyc 在 22:11:11。本轮工具调用没有写入这些路径；变化来源未评估，没有覆盖、还原或放宽判据。后续对原始已知集合的快照仍检测到 dispatch.py 与一个 pyc 不同，见 [scope-summary.json](core-grow/round2/scope-summary.json)；不能以定向检查的退出 0 抹掉首次全目录审计失败。

定向核对确认 `.agents`、根 AGENTS、历史失败报告、原有 reference 全部保持哈希；project.yaml 仅追加 engine，见 [project-record.diff](core-grow/round2/project-record.diff)。首次审计因异常中断后，其后的 Git/npm 只读检查单独补执行，并没有继续修改 hook 或游戏逻辑。全部异常的哈希基线与比较结果保留，没有声称整个工作区干净。

| 提交 | 内容 |
| --- | --- |
| ad655cf | 通过等价性检查的 JavaScript copy 与证据 |
| 41f6f4e | TypeScript 拆分与匹配证据，删除三个过渡 JS |
| 6d50a7d | 规则红绿测试与 4 项 grow 浏览器测试 |
| bec28ab | Web 引擎记录、最终 grow 检查与交接；tag grown/dusk-fish |
| ac15b36 | R 单功能、主 brief、真实行为测试及对应证据 |

提交均使用明确路径，标题中文，无 AI 署名尾注；没有 git add -A、没有 push。框架副本、诊断/迁移驱动、其他 runtime-cases 与个人文件不提交。原型基线 5237684 与 reference 5b90e81 沿用。Tracked 工作区在最终 Git 核对时无 diff/暂存变更；原有未跟踪内容保留。报告与剩余原始日志另作限定路径证据提交，不引入代码变化，也不因证据提交重跑已通过测试。

## 交接与未评估

- 游玩：`npm run dev`，打开它打印的本机地址；也可打开 dist-single/index.html。此命令作为交接说明，本轮未启动开发服务器或验证调参面板交互。
- 构建：`npm run build` 输出 dist/；`npm test` 为 Vitest + 真实 Chrome Playwright；`npm run smoke` 为 boot 子集。开发调参用反引号或 ?tune，保存块由 one-shot-tune.sh 写入数据和 feel-log；没有执行未请求的调参。
- 工具沿用 Node v24.14.0、npm 11.9.0、Chrome 157；Python 为 %LOCALAPPDATA%/Python/pythoncore-3.12-64/python.exe，Chrome 为 C:/Program Files/Google/Chrome/Application/chrome.exe，Bash 为 D:/Program Files/Git/bin/bash.exe。锁定开发依赖保持已安装版本，没有缺依赖假通过。
- NOT ASSESSED：人工试玩、乐趣与主观难度、长期运行、跨浏览器、发布部署、开发调参 UI，以及所检测 hook 文件变化的来源。本轮没有 PROCEED/PIVOT/KILL 人工结论。
