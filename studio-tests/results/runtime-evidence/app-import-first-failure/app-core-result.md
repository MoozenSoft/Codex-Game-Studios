# 真实 App 核心验收结果

日期：2026-11-17（Asia/Shanghai）。最终结论：**BLOCKED — 导入交接截图路径出现真实脚本适配缺陷**。全流程未通过，没有关闭 Story，没有作 PROCEED 或发布判断。

## 入口、配置与授权复用

- cwd 已实际核对为 <app-checkout>，分支 app-acceptance。
- 已读取本项目 AGENTS.md、codex-runtime、automation-modes 及本地 prototype 的导入、change、grow、handover 规则。没有调用全局 Skill、插件、MCP、私有客户端数据或其它插件工作流。
- yaml-helper 实际输出 automation=collaborative(default)、workflow=minimal、review_mode=solo、engine unset；未改变 rigor/automation。
- Git Bash 按 git --exec-path 定位为 D:/Program Files/Git/bin/bash.exe；Python 命令经 python-run.sh，并在进程内明确 CGS_PYTHON=C:/Users/xingxing/AppData/Local/Python/pythoncore-3.12-64/python.exe。没有调用裸 python/py 安装器。
- Chrome 使用 C:/Program Files/Google/Chrome/Application/chrome.exe，实际浏览器日志 UA 为 HeadlessChrome/157.0.0.0。Chrome 实际启动并渲染，截图均已打开查看。
- 复用本请求对测试输入、产物、限定路径提交及通过后关闭的明确授权，没有重复索要这些决定。必要命令经当前正常审批执行，未修改全局 PATH、沙箱或 hooks。
- 保持当前 Sol 策略，没有切换模型。阻断发生在 prototype 主会话脚本阶段，未到达 dev-story 的 programmer 或 code-review 的独立 reviewer 阶段；本次无原生角色委派，也不将主会话检查冒充独立角色评审。

## 阶段实际结果

| 阶段 | 结果 | 已执行或停止原因 |
|---|---|---|
| 入口与领域规则 | 已核对 | cwd/branch 一致；配置解析、rule-routing 均退出 0，读取 prototype-code 规则 |
| 45 秒游戏行为 | 下列四个自动场景达到预期 | 胜利、超时、暂停冻结、继续并从失败页 Enter 重试，均为真实 Chrome 结果；不等同于完整导入流程通过 |
| 导入 door 交接 | BLOCKED | 四张 door 基线截图均全黑且 state={}，helper 却退出 0；最小对照复现成立 |
| 45→60 秒 change | NOT ASSESSED — 未执行 | 按“真实脚本缺陷停止受影响阶段”的要求，停止顺序流程；duration 仍为 45，quota 仍为 3 |
| Grow guard/reference/copy/TypeScript/规则红绿/Playwright/record/build/test-run/smoke | NOT ASSESSED — 未执行 | 导入交接阻断；未调用 npm ci，未建立工程或安装依赖，未开始原型冻结阶段 |
| 普通 R 键功能与真实红绿 | NOT ASSESSED — 未执行 | 依赖 Grow 的后续阶段未开始；没有自动创建 Story |
| 显式 N 键 Story/readiness/失败 story-done/dev-story/code-review/smoke-check/最终 story-done | NOT ASSESSED — 未执行 | Story 文件尚未创建，未制造或宣称该 Story 的测试红灯；没有把文件存在当成测试通过，没有关闭 Story |

## 实际命令、退出码与场景证据

逐条实际 executable、完整 argv、时间与退出码保存在 app-acceptance/commands.jsonl；同名 .log 保存完整终端输出。没有仅依据进程退出码作通过判断。

以下 one-shot-run 均通过实际 Git Bash 调用，folder=prototypes/app-dusk-fish，seed=721，limit=60。W 表示固定输入串：Enter ArrowRight:0.5 ArrowLeft:0.5，随后 60 次 Space wait:0.65（完整字面值已保存在 commands.jsonl）。

| 命令阶段 | 实际命令/输入 | 退出码 | 实际观察与证据 |
|---|---|---:|---|
| 配置 | yaml-helper.sh resolve_config --keys review_mode,automation,workflow,automation_always_ask,engine_values | 0 | 默认 collaborative/minimal/solo，engine unset |
| 规则 | python-run.sh rule-routing.py prototypes/app-dusk-fish/ design/game-brief.md src/ data/ assets/ tests/ production/qa/ production/session-state/ project.yaml | 0 | 返回 .agents/rules/prototype-code.md，已读取 |
| import-45-win | one-shot-run.sh，--log W | 0 | step 413 进入 results；t=6.87、score=3；截图显示 3/3、剩余 38.1 秒；45-win.png |
| import-45-loss | one-shot-run.sh，--log "Enter wait:46" | 0 | step 2702 进入 over，t=45、score=0；45-loss.png |
| import-45-pause | one-shot-run.sh，--log "Enter ArrowRight:1 KeyP wait:5" | 0 | step 67 与 400 的 t=1.08、x=580、phase=0.7 完全相同；截图显示暂停、43.9 秒；45-pause.png |
| import-45-resume-retry | one-shot-run.sh，--log "Enter KeyP wait:2 KeyP wait:46 Enter ArrowLeft:0.5" | 0 | title→play→pause→play→over→play；重新开始 t=0，最终 x=310；45-resume-retry.png |
| baseline-add | git add -- 六个明确原型文件及 design/game-brief.md | 0 | 仅 index.html、config.js、brief.md、brief.source.md、feel-log.md、assets/provenance.yaml 与项目 brief |
| baseline-commit | git commit -m "保存应用验收原型与导入简报基线" -- 上述七个路径 | 0 | df53774ba1c299528e0e2134dd73ca5162b1652b；没有框架或旧 CLI 报告 |
| baseline-tag | git tag baseline/app-dusk-fish | 0 | 仅本地标签，没有 push；没有 one-shot/grown 标签 |
| door-baseline-shots | door-in.sh --shots app-dusk-fish --start Enter --play "ArrowRight:0.5 ArrowLeft:0.5 Space wait:0.65 Space wait:0.65 Space wait:0.65" | 0 | 四张截图均 blank，errors=0；这是阻断，不能算通过 |
| door-after | door-in.sh --after app-dusk-fish 源目录 | 0 | 保留已有 provenance；生成 evidence/door.md，追加 .gitattributes 的原字节规则。该命令在同一批次中已执行，之后才审阅到 blank 行；不是修复，也不是通过证据 |
| repro-normal | one-shot-run.sh --seed 721 --log Enter --stop 120 --limit 60 | 0 | scene=play，screen=449e1d2a drawn；repro-normal.png |
| repro-hookless | 同上一条，额外 --hookless | 0 | scene=hookless、state={}、screen=c9d0dc5 blank；repro-hookless.png |
| framework-static | python-run.sh validate-framework.py --scope all --format json | 0 | incremental 静态校验 passed=1、failed=0、not_assessed=0；覆盖 JSON 37、TOML 50、Skills 75、Skill 资源 206；不代表真实流程通过 |
| checkpoint | session-state.sh checkpoint（stdin 为实际阻断状态） | 0 | 创建 production/session-state/active.md，保留 BLOCKED 与恢复入口，未关闭阶段 |

统计：实际 Chrome 启动 10 次（正常路径 5 次、hookless 路径 5 次）；正常路径 5 次观察到绘制，hookless 5 次均为全黑。四个业务自动场景的完整日志均未报告 uncaught 错误；黑屏路径同样 uncaught=0，说明零异常计数不等于功能通过。Vitest/Playwright 测试函数数、npm test/test-run/smoke 执行次数均为 0。

45 秒阶段尚未单独验证上下方向键、胜利结果页 Enter 重试；已实际验证左右移动、胜利、超时、暂停、继续与失败结果页 Enter 重试。不能把未测分支推定为通过。

## 阻断与最小复现

最小复现见 app-acceptance/repro.md，正常与故障两张截图均已实际打开查看。真正失败的检查是“导入截图应实际显示并推进游戏”，不是进程退出状态。

- door-in.sh:114 强制传入 --hookless。
- one-shot-run.sh:160 总是加入 manual=1，:169 再加入 hookless=1。
- one-shot-driver.js:625 用 hookless || window.game，因而不驱动该游戏已有的真实 hook。
- 本游戏 manual=1 会停用自身帧循环，只能由真实 game.step 推进。该组合在本次 Chrome 中实际产生空状态与全黑截图。
- 没有修改 .agents、.codex、AGENTS.md 或 studio-tests，也没有换一套检查器伪造通过。导入交接及其下游步骤保留为未完成。
- 红灯阻断已经体现在该真实检查异常上。用户指定的“N 测试先红、首次 story-done 必须 BLOCKED”尚未到达，不能用此导入红灯冒充 Story 门禁演练。

## 同 seed、画面与文案

- seed=721 不变。最小对照仅改变 runner 的 hookless 模式，正常结果为 play / drawn，hookless 为 {} / blank；这不是获准的玩法变化。
- Grow reference 的双跑 exact、copy/typescript 的 match、R/N 的 same-seed run 都未执行，确定性全流程结论为 NOT ASSESSED。
- 页面保留源标题 dusk-fish，原型目录为 app-dusk-fish；这属于原样导入的命名差异，没有改名实现。
- 已查看胜利、失败、暂停、重试、四个 door 基线及两个最小复现截图。正常截图中的渔夫、池塘、鱼、HUD 和结果文字可见；door 的四张均为全黑。
- R/N 功能未实施，所以没有新提示文案或相应截图差异可以报告。

## 哈希与文件范围

完整 SHA-256 清单见 app-acceptance/before.json 与 app-acceptance/after.json，按文件记录原型及源清单，含配置、页面和历史证据；不只记录一个不可追溯的总哈希。

| 范围 | 实际核对 |
|---|---|
| 只读源 prototypes/dusk-fish | 31 个文件，新增/修改/删除均为 0，逐文件 SHA-256 未变 |
| 本轮前已有的目标原型 | 原有 32 个文件 SHA-256 均未变，包括 index.html、config.js、两个新旧 brief；仍是 45 秒、3 条、seed 721 |
| 本轮新增的目标证据 | 10 个文件：evidence/baseline 下 4 张 PNG、4 份 TSV、inputs.txt，加 evidence/door.md；因此目标当前共 42 个文件 |
| 框架保护范围 | .agents、.codex、studio-tests 全部文件及根 AGENTS.md，共 854 个文件，数量与 SHA-256 全部未变 |
| .gitattributes | door-after 添加两行，仅记录 app-dusk-fish 的原字节规则；保留未提交状态 |
| 旧 production/qa 内容 | 未修改、未提交；本轮产物在新建 app-acceptance 子目录与本结果文件中 |

已提交内容只包括本测试明确授权的七个原型/brief 文件。新证据与 .gitattributes 尚未提交，未为越过后续 guard 再提交任何内容。Grow 未开始，因此“Grow 后冻结目标整个目录”的阶段尚未触发。

## 尚未评估与后续入口

人工体验、乐趣、完整人工 smoke 均为 NOT ASSESSED。没有人试玩，不宣称 PROCEED。没有生成根 Web 工程、没有 npm 下载、没有安装浏览器或运行时，没有创建或关闭 Story。

下一步需要先解决本报告复现的框架导入适配缺口，再恢复导入交接；修复框架不在当前允许修改范围。后续仍须从 60 秒 change、Grow、R 功能及显式 N Story 的真实红绿与完成门禁依次继续，不能用本报告替代这些结果。
