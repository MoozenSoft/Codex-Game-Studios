# Game Brief: dusk-fish

## In your words
这是工作室框架的已授权端到端验收，在当前隔离项目中使用本仓库 .agents/skills/prototype/SKILL.md（不要使用其他插件同名Skill）完成普通Web原型路径，不能走spike绕过流程。固定需求与已批准决定：游戏名 dusk-fish，2D原创矢量钓鱼，方向键移动渔夫，Space在移动判定条落入区域时收鱼，30秒内钓到3条赢，超时输；Enter开始/重试，P暂停。图形需绘制渔夫、池塘、鱼与HUD，不能用emoji替代。全部数值在config.js中；保留原型starter固定步进与window.game测试钩子，确定seed可回放。此次测试已批准这份具体brief，以及 design/game-brief.md、prototypes/dusk-fish/、production/qa/evidence/ 中的创建、修改和脚本/浏览器验证，collaborative模式复用已有授权，不再询问这些已定决定。先保存brief，再按原型Skill构建和运行脚本检查、查看截图、修复实际问题并形成handover；没有人试玩，不能声称PROCEED。不得修改框架本身、hook定义、账号设置或目录外文件；不要grow或安装npm（后续另一步验证），不要提交。最后保存简短验收报告到 production/qa/evidence/core-prototype-result.md 并返回路径、实际运行结果与未评估项。浏览器已存在Chrome，Git Bash为D:/Program Files/Git/bin/bash.exe；如默认python只有安装管理器，使用本机已有Python运行时，不能自动下载安装。


After play: 这是一条明确标注为自动验收输入的反馈，不是人工试玩。把单局时长从30秒改为45秒，保留3条鱼目标和其它操作。

本轮授权：此前“不 grow、不安装 npm、不提交”仅属上一轮边界；本轮允许隔离项目 grow、锁文件 npm ci、测试及限定路径提交。人工试玩仍未评估。

**Pitch:** 黄昏池畔移动渔夫，抓准判定条时机，在四十五秒内收获三条鱼。
**Genre:** arcade fishing。
**Controls:** 方向键移动；Space 收鱼；Enter 开始/重试；P 暂停/继续。
**Question:** 移动与定时收鱼能否构成完整、清楚、可重试的短局？*(inferred (strong))*
**Hooks:** 暮色水面上的鱼影、移动判定条与三鱼倒计时。
**Intent:** 本次无人试玩；乐趣与难度未评估。

## Look and references
- Look: 2D原创矢量钓鱼；靛蓝暮色、青绿池水、杏色渔夫与金色判定区；渔夫有草帽、身体、手臂与钓竿，鱼有尾鳍、背鳍与眼睛；每个形象手绘，无 emoji 或单一圆形替身。配色与造型细节 *(guessed)*。
- View: 2D 固定俯视镜头；池畔木栈道和可游动的鱼影。*(guessed)*

## First minute
Enter 离开标题后，方向键沿池畔栈道移动，观察循环判定条，Space 在金色区域内收鱼；三条后进入胜利结果，或四十五秒到时失败，Enter 立即重试。

## Challenge
开局即需瞄准时机；每条鱼后判定条加快，失误有短暂收线冷却但不扣已获鱼，失败清空本局重新开始。加速与冷却细节 *(guessed)*。

## Core loop
- 沿池畔移动渔夫，调整钓竿与落点。
- 看判定条并按 Space，成功增加渔获，失误等待短暂冷却。
- 达到三鱼获胜或到时失败，Enter 重试。

## Goal & fail state
- 45 秒内钓到 3 条赢；超时输。暂停冻结本局与判定条。

## Features
- [x] 绘制 2D 原创矢量渔夫、池塘、鱼与 HUD，无 emoji。
- [x] 方向键移动渔夫，Space 在判定条区域内收鱼。
- [x] 45 秒倒计时、3 条胜利与超时失败。
- [x] Enter 开始/重试，P 暂停/继续，显示操作与结果。
- [x] config.js 集中数值，固定步进、seed 回放及 window.game 钩子。

## Your systems
- 移动、判定条、收鱼 · in the slice
- 倒计时、胜负、暂停和重试 · in the slice
- 固定步进、确定 seed 与测试钩子 · in the slice

## Keep

## Avoid
- 不用 emoji 替代图形；不复制现有游戏素材或界面。
- 不走 spike；不修改框架、hook 或账号设置；不 push；所有操作限于当前隔离目录。

## Out of scope
- 多水域、生涯与装备升级：grow it（本次不执行）。
- 天气、船、多人服务：add it as a feature（本次不执行）。
- 人工试玩与 PROCEED/PIVOT/KILL 判断：等待实际试玩。

## Build order
1. 保存 brief；用 starter 构建开始、移动、判定收鱼、限时胜负、暂停与重试完整短局。
2. 绘制暮色池畔和角色，保留集中配置与确定性钩子。
3. 执行脚本检查，查看 play/figures 截图，修复实际问题并交接。

**Kill condition:** 人工试玩后才能评估是否放弃。*(inferred (strong))*
**Who it's for / what they feel:** 喜欢短局时机挑战的单人玩家。*(guessed)*
**Games you love / don't:** 未提供；无外部参考图片。
