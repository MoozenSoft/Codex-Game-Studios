**Web 自动回归通过。18 项测试全部通过，必要失败 0 项。** 两条命令均在 Git Bash 受限启动失败后，经审批重试成功。

| 测试 | 总数 | 通过 | 失败 | 退出码 |
|---|---:|---:|---:|---:|
| Vitest | 6 | 6 | 0 | `0` |
| Playwright | 12 | 12 | 0 | `0` |

辅助脚本报告 `ran=yes`、`zero_tests=no`、`e2e_build=ok`、`e2e_browser=started`，两部分均未超时，判定规则为 `web:pass`。[测试日志](/<probe>/.scratch/cli-full-20261118/game-tests.log)

Headless Chrome 执行 `Enter wait:0.2` 后，场景在第 1 步从 `title` 切换到 `play`。第 2 步仍在 `play`，游戏时间从 `0` 推进到 `0.02` 秒，得分为 `0`。浏览器输出 `drawn` 和 `uncaught=0`，无 `crash` 或 `error` 记录。已查看 1280×720 截图，钓鱼场景与 HUD 均可见。本次运行未采集到帧耗时样本。[截图 game-input.png](/<probe>/.scratch/cli-full-20261118/game-input.png)

人工试玩、游戏乐趣和操作手感均未评估。
