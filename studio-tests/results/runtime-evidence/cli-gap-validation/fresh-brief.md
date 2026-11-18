# Game Brief: Signal Tiles

**In your words**
> 想做一个叫 Signal Tiles 的最小原创网页小游戏。Enter 开始，Space 每次点亮三个信号格中的下一格，全亮后立即显示胜利，R 重置，计分确定。两块深蓝面板和青色灯，无外部资源。

**Pitch / Genre:** 原创单屏键盘小游戏：用三次按键依次点亮信号格，第三格亮起时立即获胜。
**Question / Hooks:** 不读长说明，玩家能否在第一轮就看懂每次按键的进展，以及第三格亮起为何意味着胜利？ *(guessed)*

**Look and references:** 两块深蓝面板和青色信号灯。固定 2D 单屏：一块显示按键提示、分数和状态，另一块横排三个方形信号格。无外部素材或参考作品。 *(面板分工与布局：provisional)*

**First minute / Core loop**
- 待机时三格全暗、分数为 `0`；按 `Enter` 开始。
- 每次单独按下 `Space`，从左到右点亮下一格并加 `1` 分；长按不连发。 *(计分与长按规则：provisional)*
- 第三格亮起的同时显示「胜利」，分数锁定为 `3`；任意阶段按 `R` 都回到待机、熄灭三格并清零。 *(锁分与重置细节：provisional)*

**Challenge / Goal & fail state:** 点亮三格即通关。不设计时、随机或失败惩罚；这轮只验证输入反馈是否清楚。 *(provisional)*
**Features:** ☐ 开始与重置　☐ 三格顺序点亮及固定计分　☐ 即时胜利显示　☐ 双面板离线页面
**Keep / Avoid / Out of scope:** `Keep` 待试玩填写。不引入外部资源，不做额外关卡、排行榜或发布。
**Build order:** 先实现并核对待机 → 开始 → 三次点亮 → 胜利 → 重置，再完成面板样式并本地试玩。若试玩者仍看不懂进展或胜利反馈，先调整反馈，不加新机制。 *(guessed)*

**实际设置：** 指定 Git Bash 的配置 helper 经沙箱外审批重试成功，返回 `review_mode: solo`、`automation: collaborative`、`workflow: minimal`。项目未配置引擎，本次走 `--path html`；`project.goal` 未解析出值。模型与推理投入沿用当前会话，未单独验证。
**批准后拟写入：** `design/game-brief.md`、`prototypes/signal-tiles/brief.md`、`prototypes/signal-tiles/index.html`、`prototypes/signal-tiles/config.js`，以及本地试玩证据。

**状态：未批准构建。** 本回合只展示 brief；未写文件、未构建、未试玩、未发布，也未改动主仓库。

1. **Build it** — 批准按此 brief 在隔离目录构建
2. **Change something** — 先修改 brief
3. **Stop** — 不继续

你想在同一线程里选哪一项？
