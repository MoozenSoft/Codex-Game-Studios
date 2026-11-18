# 导入截图路径最小复现

结论：BLOCKED。相同原型、seed、输入和步数，仅增加 door 使用的 --hookless 后，Chrome 输出黑屏；helper 退出码仍为 0。未修改框架或游戏来规避此问题。

在 app-web-acceptance / app-acceptance 执行：

```powershell
$gitExec = git --exec-path
$gitRoot = Split-Path (Split-Path (Split-Path $gitExec.Trim()))
$bashPath = Join-Path $gitRoot 'bin/bash.exe'
$env:CGS_PYTHON = 'C:/Users/xingxing/AppData/Local/Python/pythoncore-3.12-64/python.exe'
$env:PAGE_SHOT_BROWSER = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
& $bashPath '.agents/scripts/one-shot-run.sh' 'prototypes/app-dusk-fish' 'production/qa/evidence/app-acceptance/repro-normal.png' --seed 721 --log Enter --stop 120 --limit 60
& $bashPath '.agents/scripts/one-shot-run.sh' 'prototypes/app-dusk-fish' 'production/qa/evidence/app-acceptance/repro-hookless.png' --seed 721 --log Enter --stop 120 --limit 60 --hookless
```

本次两条命令实际均退出 0，完整参数与退出码见 commands.jsonl。

| 模式 | 实际观察 | 截图 |
|---|---|---|
| 正常 hook | scene=play，state.t=1.98，screen=449e1d2a drawn，uncaught=0 | repro-normal.png |
| --hookless | scene=hookless，state={}，screen=c9d0dc5 blank，frametime none，uncaught=0 | repro-hookless.png |

两张图片均已实际打开查看，后一张为全黑。对应完整日志为 repro-normal.log、repro-hookless.log。

定位到的调用关系：

- .agents/scripts/door-in.sh:114 对所有导入游戏固定使用 one-shot-run.sh --hookless。
- .agents/scripts/one-shot-run.sh:160 总是加入 manual=1，:169 在 hookless 模式额外加入 hookless=1。
- .agents/scripts/one-shot-driver.js:625 选择 hookless || window.game，即存在真实 window.game 时仍优先使用合成 hook。
- prototypes/app-dusk-fish/index.html:210 在 manual=1 时只绘制一帧，不启动本身的帧循环；正常 hook 可调用它的 game.step，而 hookless 路径未使用该入口。

上面的分支关系由源码核对，黑屏与空状态由真实 Chrome 复现。画布最终何时被重置未另加插桩分析；不把这一细节写成已证实根因。

完整 door 路径也已实际执行：四个基线时点 first/start/play-10s/play-30s 均为同一 blank 哈希 c9d0dc5，errors=0，door helper 退出 0。该结果不能支持导入交接通过。

受影响阶段已停止；60 秒 change、Grow、R 迭代及 N Story 均未开始。修复框架不在本次授权范围。
