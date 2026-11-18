# Game Brief: brief-probe

## In your words

> 方向键移动、Space在判定区钓鱼、30秒钓3条、Enter开始/重试、P暂停，2D原创矢量美术、数值集中config.js、确定seed可回放。

**Pitch:** 在30秒内移动找准钓鱼判定区，抓住时机钓满3条鱼。

**Genre:** Web 街机钓鱼。

**Controls:** 方向键移动；Space钓鱼；Enter开始/重试；P暂停/继续。

**Question:** 移动与判定时机能否让30秒挑战值得重试？*(inferred (strong))*

**Hooks:** 短局挑战与确定seed回放。

**Intent:** 无额外设定。

## Look and references

2D原创矢量美术；固定俯视镜头，青蓝水面、暖木色岸边、金色判定提示，鱼与角色用完整轮廓绘制，无emoji或占位圆形。镜头和配色为 *(guessed)*；未指定参考作品。

## First minute

Enter开始 → 方向键靠近钓点 → 在判定区按Space，获得捕鱼反馈 → 30秒内成功或失败 → Enter重试。*(inferred (strong))*

## Challenge

30秒内钓满3条获胜；到时不足3条失败。暂停冻结计时与模拟；失误可继续尝试，重试恢复本局seed。后两项为 *(guessed)*。

## Core loop

移动找位置 → 判定区按Space → 捕获计数增加 → 继续挑战或Enter重试。

## Goal & fail state

30秒内捕获3条获胜；超时未达标失败。

## Features

- [ ] 方向键移动与Space判定捕鱼
- [ ] 30秒倒计时、3条目标与胜负反馈
- [ ] Enter开始及胜负后重试
- [ ] P暂停/继续
- [ ] 2D原创矢量场景
- [ ] 所有调节数值集中于`config.js`
- [ ] 确定seed；相同seed与输入序列可复现结果 *(inferred (strong))*

## Keep

空，等待人工试玩。

## Avoid

修改既有游戏、框架或全局配置；安装；提交。

## Out of scope

本回合已批准保存brief，构建仍未批准；多水域、船只升级、天气及联网竞赛留待另行批准。

## Build order

完整单局与胜负 → 暂停及重试 → seed回放验证 → 矢量呈现与操作验证。*(guessed)*

---

**Kill condition:** 人工试玩后判定；当前未设定。

**Who it's for / what they feel:** 喜欢短局反应挑战的玩家，轻快且可重复尝试。*(guessed)*

**Games you love / don't:** 未指定。

## 运行设置与授权状态

已解析的实际工作根：`.scratch/cli-brief-interaction/`。

`automation: collaborative`（project.yaml）、`workflow: minimal`、`review_mode: solo`。

保持Sol；推理投入沿用当前会话，未单独验证。目标为Web，项目目标未另设。

构建批准后拟写文件均位于`.scratch/cli-brief-interaction/`：`design/game-brief.md`及`prototypes/brief-probe/`内的brief副本、HTML、JS和`config.js`。本回合仅批准保存本文件，构建仍未批准；不创建原型、不构建、不安装、不提交，不修改其它文件。

没有人工试玩，结论为 **NOT ASSESSED**。
