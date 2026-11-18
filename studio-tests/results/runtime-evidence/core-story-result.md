# 显式 Story 路径真实 CLI 验收：N 键结果重试

**日期**：2026-11-17
**项目**：<probe>
**Story**：[story-001-n-retry.md](core-story/story-input-complete.md)
**最终结论**：COMPLETE WITH NOTES；Story Status: Complete。必要自动化及视觉检查通过；人工试玩仍未评估，不声称 PROCEED。

## 阶段、配置及授权

- 当前为已 grow 的 Web 游戏（现有 src、data、package.json、grow-dusk-fish/replay.args），本轮只做受控增量，没有再 grow。project.stage 解析为 not set，未把目录存在推定为已批准的 Production 阶段。
- automation=collaborative(default)；rigor/workflow/qa.level=minimal(default/rigor:minimal)；review_mode=solo；story_granularity=coarse；system_overrides=none。
- Web 8.3.4 来自 project.yaml；src/tests 来自规范 engine row；现有 Vite 8.3.4 实际安装值匹配。specialists.primary=lead-programmer，code/shader/ui unset。
- project.yaml 唯一增量为 testing.strict.integration: true；解析结果 integration=blocking(project.yaml)。没有改变模式、引擎或其它设置。
- 沿用本轮已批准的 Story 输入、保存/实施/验证/通过后关闭授权；不重复询问。不接受失败例外，不安装、不提交、不发布。
- 基线与结束 HEAD 均为 f56bab3c63f57504b0b9a73bd58426585412b53a（probe）。未写外层仓库或全局设置。

## 实际加载路径

五个 Skill 均实际读取自唯一指定规范源，未使用隔离副本、全局/插件同名 Skill 或 MCP：

1. D:/Git/Codex-Game-Studios/.agents/skills/story-readiness/SKILL.md
2. D:/Git/Codex-Game-Studios/.agents/skills/story-done/SKILL.md（红灯、最终各执行一次）
3. D:/Git/Codex-Game-Studios/.agents/skills/dev-story/SKILL.md
4. D:/Git/Codex-Game-Studios/.agents/skills/code-review/SKILL.md
5. D:/Git/Codex-Game-Studios/.agents/skills/smoke-check/SKILL.md

必需引用也从 D:/Git/Codex-Game-Studios/.agents/ 读取：docs/codex-runtime.md、automation-modes.md、config-resolution.md、code-root-resolution.md、run-and-observe.md、coding-standards.md、docs/templates/story.md；smoke-check/references/1-detect-setup.md 至 6-write-gate.md；code-review/references/lens-engine.md 由唯一引擎 helper 读取。
角色规范源为外层 .codex/agents/gameplay-programmer.toml 与 lead-programmer.toml（只读）。隔离项目 AGENTS.md 和 rule-routing 输出的 test-standards.md 已读取；无 .codegraph，跳过 CodeGraph。
五个规范 Skill 的 SHA256 收录在 [before-hashes.json](core-story/before-hashes.json) 与 [after-hashes.json](core-story/after-hashes.json)，前后一致。

## 顺序及真实结果

| 步骤 | 实际行为 | 结果与原始证据 |
|---|---|---|
| 保存 Story、$story-readiness | 项目 Story 模板，Ready / Integration / Core / S；brief 第 7 项批准增量；ADR N/A 有理由；Dependencies None | READY；[readiness.md](core-story/readiness.md)、readiness-config-final.log、readiness-facts-final.log |
| 测试先红灯 | 先创建 n-retry.spec.ts，旧源码不含 KeyN；真实 Chrome 键盘和固定步进到达胜败 | **3 tests：1 passed、2 failed**；两项期望 play，实际 over/results；[red.log](core-story/red.log) |
| 红灯 $story-done | 显式解析必要集成门禁并实际 test-run filter；检查 runner 的失败数，不只看 helper 退出码 | **BLOCKED**；helper exit 0，但 e2e_exit=1、failed=2、zero_tests=no、rule=web:failed；[story-done-red-runner.log](core-story/story-done-red-runner.log) |
| 失败时不关闭 | Story 保持 Ready，无 Complete；前后原样复制并 cmp | [story-done-red.md](core-story/story-done-red.md)、red-story-before.md / red-story-after.md、[red-state.log](core-story/red-state.log) |
| $dev-story | 标为 In Progress；真实 gameplay-programmer 仅写 src/main.ts 两处输入条件和结果提示 | Implemented；[dev-story.md](core-story/dev-story.md) |
| 本轮构建及全套 npm test | tsc + Vite build；Vitest + Chrome Playwright | **18/18**（6 unit + 12 integration），exit 0；[green-build-and-suite.log](core-story/green-build-and-suite.log) |
| test-run.sh web | 规范源脚本 --root .；unit/e2e 分别解析 | **18/18**，failed=0、zero_tests=no、rule=web:pass；[green-test-run.log](core-story/green-test-run.log) |
| Web smoke、重建及回放 | npm run smoke、npm run build:single、规范 replay dusk-fish --as story --root . | **@boot 1/1**，exit 0；回放 errors=0；[smoke-and-replay.log](core-story/smoke-and-replay.log) |
| 新截图查看及提示差异 | 打开胜败 N 重试前后四图和同 seed 新旧图，另作像素与玩法轨迹比较 | 见下；[replay-comparison.json](core-story/replay-comparison.json) |
| $code-review | 父代理完整复核；唯一 fresh-context lead-programmer 引擎 helper，未参与实现 | **APPROVED WITH SUGGESTIONS**，无 Required Changes；[code-review.md](core-story/code-review.md)、[engine-helper.json](core-story/engine-helper.json) |
| $smoke-check | 按规范全部六个引用检查，复用本轮当前有效的真实 suite；不把人工未答当通过 | 自动化 PASS；完整人工批次 **NOT ASSESSED**；[smoke 报告](../smoke-2026-11-17.md) |
| 最终 $story-done | AC 5/5；必要结果均通过，receipt 未变；按 solo 跳过内部两门禁 | **COMPLETE WITH NOTES，已关闭**；[story-done-final.md](core-story/story-done-final.md)、story-done-final-config.log、[final-audit-complete.log](core-story/final-audit-complete.log) |

raw runner 日志保留在 core-story/red-runner-raw.log.e2e、green-runner-raw.log.unit / .e2e；全部真实命令、根目录、Bash/Python 路径、时间及退出码见 [commands.jsonl](core-story/commands.jsonl)。没有使用上轮 15/15 代替本轮行为验证；最终仅元数据/brief 改动后复用本轮 18/18，不重复全量。

## 行为与观察证据

- 新 N 测试 3 项：胜利、失败的完整 State 与事件重置；同样输入再玩一局比较终态，覆盖 RNG；标题/play/pause 与无 N 同 seed 对照。
- 输入是 page.keyboard.press/down/up，实际进入 Chrome KeyboardEvent.code；window.game 仅用于读取与推进确定帧，不直接伪造结果状态或注入 N hit。
- 失败测试先钓到 1 条并移动后超时，胜利测试到 3 条；N 后完整 state 等于初始值、events=['start']，包含时间/分数/反馈/冷却/位置/目标/鱼位置。N 测试从红灯至绿灯未修改或放宽。
- 原 R/Enter 的胜败四种重试及 R 非结果用例本轮通过；45 秒、3 鱼、移动暂停、seed 回退与确定性原回归一并通过。
- 已打开 [失败前](story-001-n-retry/n-over-before.png)、[失败重试后](story-001-n-retry/n-over-after.png)、[胜利前](story-001-n-retry/n-results-before.png)、[胜利重试后](story-001-n-retry/n-results-after.png)。提示含 N、无溢出；两种重试后均显示 45.0s、0/3、渔夫初始位置。
- 同 seed 原始 match=no：frame 3481 新 a0c632cd，旧 5cd95c32，不能宣称完全相同。已打开 [旧 accepted](core-story/accepted-before.png) 与 [新 story](core-story/final-story.png)；玩法轨迹行完全一致，0 errors；仅提示区域 x500–780/y393–411 的 2617 像素变化。画面由“Enter or R”变为“Enter, R or N”。
- 该提示增量属于已批准 Story，按本轮“若只是提示文案变化，明确核对与记录”的授权接受；保留旧 accepted-before.png/.tsv，再调用规范 accept 更新隔离 evidence 基线。结论为 **CHANGED, accepted — 仅提示变化**，不是 SAME。

## 门禁、评审范围与未评估项

显式要求优先于 qa minimal 默认豁免。红灯时的必要失败实际挡住关闭；helper 退出 0 不代表测试通过。必要结果若未知或缺环境必须 NOT ASSESSED，本轮必要结果均实际可读且通过。
完整 $smoke-check 的人工 Batch 1/2/3 保持 NOT ASSESSED，不声称完整人工 smoke 或 QA hand-off PASS；本轮要求的 Web smoke 及自动化部分已经通过。人工试玩是用户明确保留未评估、minimal 下可选的后续，不作为本 Integration Story 关闭的必要结果，不用于掩盖任何必要失败。

review_mode=solo：QL-STORY-READY、QL-TEST-COVERAGE、LP-CODE-REVIEW 内部门禁按规范跳过。Reviewed by 为 **self, no independent review**；完整覆盖、验收与截图结论均为父代理自查。独立范围仅 /root/review_n_retry 的引擎只读检查，其 helper-result/1 完整返回、无写入，父代理逐项核实 7 条证据，不能把它扩称为全量独立评审。当前工具支持 agent_type，未使用角色降级。

可选或范围外项目继续未评估/未修复：人工手感、性能、乐趣难度、PROCEED/PIVOT/KILL；Web 全版本 API 文档核验；既存全局状态耦合建议；VERSION.md 缺 Installed at pin time/标准 Engine Version 字段。安装版本和构建/实际 Chrome 输入已验证，但不能因此把缺失文档检查记为通过。

## 原型及范围完整性

**prototypes/dusk-fish：31/31 文件 SHA256 相同，0 新增、0 缺失、0 改变。** 每个路径的完整前后哈希分别保存在 [before-hashes.json](core-story/before-hashes.json) 和 [after-hashes.json](core-story/after-hashes.json)，[final-audit-complete.log](core-story/final-audit-complete.log) 实际打印 prototype identical: True。
保护目录比对仅发现 design/game-brief.md、src/main.ts、tests/integration/n-retry.spec.ts 的批准变更；隔离 .agents、.codex、data、其余源码/测试/参考文档未变。AGENTS 与原型无 Git 差异。
另有批准的 project.yaml strict 追加、Story、evidence/smoke、active.md；既有 retry.spec.ts 会更新旧 core-grow/round2 内的 R 截图，仍全部落在允许 evidence 范围。构建产物为 dist/dist-single 与测试临时输出，无安装或配置扩展。

## CLI 边界及保留的异常

- Bash 按新版 runtime 从 git --exec-path 向上定位，实际 D:/Program Files/Git/bin/bash.exe；Python 固定使用 %LOCALAPPDATA%/Python/pythoncore-3.12-64/python.exe。没有使用 py、安装器或改全局 PATH。
- 初次 sandbox 内 Bash 启动无输出、exit 3221225794；原尝试记录保留。仅对已授权具体命令使用客户端 require_escalated，经批准执行；未换用 WSL。
- 初次 yaml-helper --root 位置错误已纠正，最终取值均以 --root . resolve_config --keys 的成功原始输出为准；未把首次回退输出当成正确参数验证。
- project-coherence 无 --root，先核对隔离副本与规范源字节相同，再在隔离项目运行；这是脚本入口适配，未调用隔离 Skill。
- 隔离 story-status 与规范源不同，final-audit.log 保存 cmp 失败；未运行旧副本。规范脚本无 --root，随后从隔离 production/qa 以 stdin 原样运行规范源，其两级目录定位落在隔离根，未改脚本，实际输出 **COMPLETE 1 of 1**，见 final-story-status.log。
- 最终 git diff --check exit 0；代码/测试 receipt UNCHANGED；无提交，无发布。所有可读中文产物经 apply_patch 写入 UTF-8，未用 PowerShell 默认管道生成中文文档。

下一步：人工试玩当前 build；此已批准受控 Story 不继续扩展。
