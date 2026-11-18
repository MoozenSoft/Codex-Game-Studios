# Smoke Check 报告

**日期** 2026-11-18（UTC+08:00）
**命令** `$smoke-check sprint --platform pc`
**项目** Dusk Fish，Web（Vite 8.3.4）
**Sprint** 未识别。`production/sprints/` 无当前计划。
**QA 计划** `production/qa/` 下无 QA 计划。`workflow: minimal` 下 QA 计划为可选项。

## 环境

- 使用隔离目录里的 `.agents/skills/smoke-check/SKILL.md` 及其阶段参考文件。显式调用 `D:/Program Files/Git/bin/bash.exe`。首次配置调用在默认沙箱中以 `-1073741502` 退出，未产生输出。通过 Codex 自动审批重试后退出码为 `0`。
- `yaml-helper.sh resolve_config --keys automation,workflow,qa.level,testing.strict` 解析为 `automation: collaborative`、`workflow: minimal`、`qa.level: minimal`。`testing.strict.integration` 为 `true`，`logic`、`visual`、`ui` 和 `config` 均为 `unset`。
- `project-coherence.sh` 退出码为 `0`，2 项一致、0 项差异、3 项未检查。声明版本与 Web 引擎参考和本地 Vite 一致。未检查项为固定版本写入时的已安装版本、Web 项目文件对照，以及未声明的 `commands.build`、`commands.test`。
- 找到 1 个 Vitest 文件与 3 个 Playwright 文件。Playwright 使用本机无头 Chrome（`C:\Program Files\Google\Chrome\Application\chrome.exe`）。`.github/workflows/framework-checks.yml` 配置了框架测试，隔离目录未配置游戏 Web 套件的 CI 步骤。
- 项目要求的 `validate-framework.py --scope all --format json` 在增量阶段退出码为 `0`，1 项通过，0 项失败，0 项未评估。`migration.coverage` 返回 `pending=0，total=743`。

## 自动化测试

**PASS — 18/18 通过，0 失败。** `project.yaml` 未声明 `commands.test`，因此执行 Web 默认全量入口。`test-run.sh web` 分别运行 `npm run test:unit` 与 `npm run test:e2e`，每段超时上限 900 秒。

| 检查 | 结果 | 证据 |
|---|---|---|
| Vitest | PASS，6/6 | `unit_exit=0`，未超时 |
| Web 单文件构建 | PASS | `npm run build:single`，`e2e_build=ok` |
| Playwright | PASS，12/12 | `e2e_exit=0`，`e2e_browser=started`，未超时 |
| Web 全量套件 | PASS，18/18 | `rule=web:pass`，`exit=0` |

## 测试覆盖检查

已检查实际测试文件与断言。QA 计划与 Sprint 计划均缺失，逐故事覆盖和 `$story-done` 所需证据为未评估。项目未配置已安装的 Vitest 覆盖率提供程序，本次无行覆盖率或分支覆盖率数据。

| 已验证行为 | 测试文件 | 通过 |
|---|---|---:|
| 固定步进和截止时间、命中区边界、三鱼配额、判定针周期、seed 随机序列 | `tests/unit/rules.test.ts` | 6 |
| 标题和画布启动、钓满三鱼，同 seed 状态和画面一致，移动、暂停与恢复，零和非法 seed | `tests/integration/boot.spec.ts` | 4 |
| 超时和获胜画面支持 R 或 Enter 重试并重置状态，R 在标题、游玩和暂停时不触发重试 | `tests/integration/retry.spec.ts` | 5 |
| 超时和获胜画面支持 N 重试并重置状态及随机序列，N 在标题、游玩和暂停时不触发重试 | `tests/integration/n-retry.spec.ts` | 3 |

## 人工冒烟检查

**Checklist source:** Skill Phase 4 标准清单。隔离目录缺少 QA 计划的 Smoke Test Scope、`production/qa/smoke-tests.md` 和 `tests/smoke/`。

本次无人工试玩记录。核心稳定性未执行人工检查，后续批次因缺少人工启动和试玩结果记为 `NOT TESTED`。Sprint 检查参考现有测试体现的钓鱼和重试行为。

| 检查 | 人工结果 |
|---|---|
| `core_launch` 启动当前构建并进入标题画面，无崩溃 | NOT TESTED |
| `core_new_game` 开始新一局 | NOT TESTED |
| `core_menu` 标题菜单响应输入 | NOT TESTED |
| `core_navigation` 基本导航无崩溃或卡死 | NOT TESTED |
| `sprint_primary` 钓鱼主循环 | NOT TESTED |
| `sprint_secondary` 结算画面重试 | NOT TESTED |
| `sprint_regression` 移动、暂停及恢复回归 | NOT TESTED |
| `sprint_other` 试玩范围内的意外问题 | NOT TESTED |
| `data_save_load` 存档与读取 | NOT TESTED |
| `performance` 目标设备帧率与卡顿 | NOT TESTED |

## PC 平台检查

| 平台 | 已执行 | 通过 | 失败 | 未评估 | 平台裁决 |
|---|---:|---:|---:|---:|---|
| PC | 0 | 0 | 0 | 4 | NOT ASSESSED |

| 检查 | 人工结果 |
|---|---|
| `pc_keyboard` 键盘控制 | NOT TESTED |
| `pc_mouse` 鼠标与光标 | NOT TESTED |
| `pc_window_mode` 窗口与全屏切换 | NOT TESTED |
| `pc_resolution` 分辨率切换 | NOT TESTED |

## Verdict: NOT ASSESSED

Web 自动化测试和单文件构建通过。人工冒烟与 PC 手工检查缺少实测结果，本次 smoke 结果不足以支持 QA 交接。补齐当前构建的人工试玩和四项 PC 检查结果后，才能重新裁决。`qa.level: minimal` 下该检查为可选，`testing.strict.config` 适用于 `FAIL` 的门禁处理。

本次仅保存该报告。测试生成的单文件构建、结果文件、截图和运行日志已清理。Vitest 自动刷新了隔离目录内已有的依赖缓存。
