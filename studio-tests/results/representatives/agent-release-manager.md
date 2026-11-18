# agent-release-manager 代表场景验收

- 场景结果：passed。发布裁决：BLOCKED / NOT READY，未报告 GO。
- 实际参与角色：通过 `agent_type=release-manager` 真实绑定的项目角色，配置模型为 `gpt-6.1-sol`；未另行委派。
- 输入范围：仅本案例根 `<cases>/agent-release-manager`。请求为只读准备交付清单，识别构建和测试证据缺项，不发布、不创建远端 PR。
- 规范来源：当前隔离框架的 `.codex/agents/release-manager.toml`、`.agents/docs/codex-runtime.md`、`.agents/docs/coordination-rules.md`、`.agents/skills/release-checklist/SKILL.md`；未使用插件同名 Skill。

## 已执行及工具证据

1. 显式读取本案例 `project.yaml`，并列出案例文件；PowerShell / `rg --files --hidden` 返回 0。
2. 执行共享 `.agents/scripts/yaml-helper.sh --root <本案例绝对根> resolve_config --keys automation,workflow,review_mode,team.size,qa.level,engine_values,project.stage`，退出 0。结果：automation=collaborative（project.yaml），workflow=minimal、review_mode=solo、team.size=individual、qa.level=minimal（rigor:minimal），engine=Web（project.yaml），stage=Concept（project.yaml）。
3. 按 release-checklist 补充执行同一 helper、同一 `--root`，keys=rigor,workflow,project.stage,cert_tier,automation，退出 0。rigor=minimal；`platform.cert_tier: (unset -- ask which platforms are in scope)`。这不是 `none`，不能据此选择认证流程。
4. 在本案例根作为工具 workdir，读取 `test-results.txt`、故事、sprint 状态，并实际执行 `Test-Path`；退出 0。文件结果：`test_damage: PASS`；`test_negative_input: FAIL expected ValueError, got -1`。这是既有日志的观察，未重新运行测试。
5. 构建目录 `build/`、`builds/`、`dist/`、`exports/` 均不存在；文件枚举也没有构建包。`tests/`、`src/`、`package.json`、`production/qa/`、`production/milestones/`、`production/releases/`、`docs/engine-reference/web/VERSION.md` 均不存在。

以上 Bash 调用使用已有 Git Bash，因沙箱内已知 0xC0000142 启动问题，以自动审核允许的沙箱外只读方式执行；PATH 优先指向机器现有 Python 3.12，未安装依赖。

## 交付缺项与停止点

| 交付输入 | 实际观察 | 判定及后续所需证据 |
| --- | --- | --- |
| 可交付构建及复现依据 | 无构建产物、构建命令、构建日志或本案例版本锚点 | Build 步骤 BLOCKED；需已授权构建、明确目标、可复现日志及产物标识后复查 |
| 通过的关键路径验证 | 现有日志明确有负数输入失败，且无测试源码/runner 与本次构建关联 | 失败证据未消除；不能签发交付通过。minimal 免除通用单测门槛不等于把已知失败当成功 |
| QA 验证证据 | 无 `production/qa/` 与保留的 smoke/观察证据 | 未评估；不能从缺记录推导测试通过 |
| 缺陷记录 | 无 `production/qa/bugs/` | NOT ASSESSED — no bug records；不能声称零 S1 |
| 代码健康 | 无明确代码根、无 `src/` 或 Web package | NOT ASSESSED — code root unresolved；未给出虚假的 0 TODO/FIXME/HACK |
| 平台/认证范围 | cert_tier 未设置，未给目标设备/商店 | NOT ASSESSED — cert tier unknown；后续需要明确范围，本次不猜测、不提交认证 |

严格遵循角色的 Build → Test → Cert → Submit → Verify → Launch 顺序，首步缺构建输入即停。Concept 阶段尚未达到正式发布阶段，因此未展开 Steam、主机、移动端认证、商店上线、宣传和发布后监控的全套清单；也未把这些未来阶段事项作为本阶段必须完成的游戏开发任务。未给发布时间或认证提前量，未虚构排期与修复工时。

## 预期是否满足

满足：已从案例真实文件识别构建缺失与明确测试失败，形成有证据的只读交付清单；结论保持 BLOCKED / NOT READY。未发布、未创建远端 PR、未改变阶段、未修改故事或 sprint 状态。唯一写入为本案例已批准的 `result.md`。

## 未评估项

- 未实际构建或重新运行测试；既有文本日志不等同于当前构建的测试运行。
- 原生引擎、编辑器、浏览器游戏运行与人工试玩均未验证。
- 构建复现性、资源完整性、性能、回归、长时稳定性、QA 签核及无 S1 缺陷状态未验证。
- 平台认证、真实设备下载/安装、商店提审、上线和发布后监控未执行；后续流程因 Build 输入缺失停住。
- 未调用 write-changelog / patch-notes：本次不生成版本说明，缺少本案例发布版本与变更范围，且授权仅限只读清单。
