# Codex 游戏工作室快速开始

先阅读根目录 `README.md` 和 `AGENTS.md`。本框架只适配 Codex，Skills 唯一目录为 `.agents/skills/`，角色定义位于 `.codex/agents/`。

## 环境与首次启动

安装 Git（Windows 包含 Git Bash）、Python 3.11+ 和 Codex。当前客户端实测起点为 CLI 0.169.0、Windows App 26.1111.2228.0；较低版本未承诺。Web grow 使用 Node.js 与模板锁文件中的依赖；原型路径不要求先安装完整工程依赖。

CLI 在仓库根运行 `codex`；若 PowerShell 的包装脚本被执行策略拒绝，可运行 `codex.cmd`，不要因此修改全局执行策略。App 创建本地项目时选择当前仓库根目录，然后打开新会话。已有会话可能仍持有先前的角色列表，修改角色或项目根后用新会话复测。

通过客户端正常入口审阅项目和 `.codex/hooks.json`。确认命令、目录和效果后只允许所需项目 hooks。注册存在或静态校验通过不证明它们已执行；验收状态见 `studio-tests/runtime-matrix.json`。

## 开始游戏

- 首次使用：`$start`。
- 有游戏想法：`$prototype`，从简短需求形成 brief 与浏览器原型。
- 试玩后修改：向 `$prototype` 提供具体反馈；完成真实试玩前不自动判定 PROCEED。
- 保留并发展原型：按 `$prototype` 的 grow 路径迁入 Web 工程。
- 需要完整工作室流程：`$setup-engine`、设计与架构、`$create-epics`、`$create-stories`、`$story-readiness`，再显式调用 `$dev-story` 和 `$story-done`。
- 不确定下一步：`$next-step`；检查配置：`$project-settings`。

默认模式为 `collaborative`，另有 `guided` 和 `autonomous`。模式区别及已有授权复用见 `.agents/docs/automation-modes.md`。游戏配置保存在 `project.yaml`，支持的个人覆盖保存在忽略的 `project.local.yaml`。

## 校验与恢复

执行 `python .agents/scripts/validate-framework.py --scope all --format json` 查看当前批次；完整迁移检查另加 `--stage complete`。必要失败退出 1，必要检查无法执行退出 2；可选未评估明确报告。

检查点位于 `production/session-state/active.md`，由工作流显式保存；SessionStart 注入恢复内容。事件日志不保存用户原文或完整命令，也不替代任务检查点。

原生引擎的规则、角色和模板属于迁移范围；真实 Godot、Unity、Unreal 编辑器运行及构建状态必须以具体证据为准，不由文件存在推断。
