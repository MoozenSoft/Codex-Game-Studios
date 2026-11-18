# dusk-fish 核心原型验收

日期：2026-11-16。功能与官方脚本验收 **PASS**；环境约束 **CONCERNS**；人工试玩结论 **NOT ASSESSED**，未作 PROCEED 决定。

使用本仓库 `.agents/skills/prototype/SKILL.md`，执行普通 Web One-shot 1→2→3，未走 spike。配置实际解析为 collaborative / minimal / solo；沿用用户已批准 brief 和写入范围，无重复确认、无子代理。先保存 `design/game-brief.md`，再执行 starter 创建与构建；Feature 完成标记已同步至原型 brief 副本。

产物：

- [批准的 brief](prototype-input.md)
- `prototypes/dusk-fish/index.html`（本地验收路径，未随证据归档），直接用 Chrome 打开。
- `prototypes/dusk-fish/config.js`（本地验收路径，未随证据归档）
- [交接卡](prototype/handover.md)
- [官方检查记录](prototype/check-run.yaml)
- [实际运行截图](prototype/play.png)、[角色截图](prototype/figures.png)

实际运行结果：

- Node 语法检查通过；使用已有 Chrome 157 和 Python 3.12，Git Bash 需沙箱外执行才能启动。
- `one-shot-new.sh dusk-fish` 成功；`one-shot-check.sh --keys "Enter ArrowRight:1.5 Space wait:1"` 共运行两次；`page-shot.sh ... --query scene=figures` 成功；`--checklist`、`--record boots=pass shot=pass outlines=pass` 最终退出 0。
- 官方记录 boots、shot、outlines、brief-words、emoji、nearest-game 六项全部 pass；brief checklist **12/12**。已亲自查看最终 play、figures 与胜利截图。无 crash/error/nonfinite/uncaught；输入响应 changed；检测文字均在画面内且对比度超过 10:1。
- `one-shot-run.sh` 定向日志：`win-run.tsv` 在 t=4.1、score=3 进入 results；`loss-retry.tsv` 在 t=30 进入 over，Enter 后重置。`win-retry.tsv` 证明胜利后 Enter 也重置。
- `pause.tsv` 从第 37 到 190 步保持 t=0.58、phase=0.38；`resume.tsv` 证明恢复后继续推进。四方向移动已运行，右移半秒使 x 从 400 到 490。
- seed=721、相同输入两次独立运行的 screen hash 均为 `86d1a29a`；`pause.png`、`replay.png` 的 SHA-256 均为 `d24afc348c7b6dce4687b31b1f2bcabb5fff87e475a77efb05957f0789c2e71b`。
- 固定步进、GAME_CLOCK 与 window.game 的 scene/state/press/hold/step 保留；玩法和绘图数值集中于 config.js，游戏无网络资源依赖。

修复与限制：

- 初轮证据表在截图生成前被扫描，随后路径格式也未被 helper 接受；最终改为相对游戏文件夹的 `evidence/play.png` 与 `index.html:行号`，官方记录通过。暂停测试最初误用 `P`，改为运行器要求的 `KeyP` 后验证通过。未修改框架或检查脚本。
- **环境异常：** 查找运行时时执行 `py list`，PyManager 意外输出 `Python install manager was successfully updated to 26.0.`。该自动副作用违反本次禁止自动安装的边界，因此环境约束记为 CONCERNS；未核验目录外实际变化，也未尝试回滚或进一步修改它。后续全部直接使用现有 `%LOCALAPPDATA%/Python/pythoncore-3.12-64/python.exe`，没有安装 Python 运行时、npm 或浏览器依赖。
- 未提交、未打 tag、未 grow；没有主动修改框架、hook 定义或账号设置。既有工作区文件保留。
- 未评估：人工试玩、乐趣与主观难度、长时间游玩、跨浏览器与不同 seed 的广泛覆盖。官方运行器的 loop/beat/margin 附加遥测未实现，不能据此声称已验证玩法质量；无音效需求，本次无音频验证。

证据目录：`prototypes/dusk-fish/evidence/`。构建从官方时间 20:31:03 至最终浏览器小检查 20:35:22，4 分 19 秒；记录整理时间另计。
