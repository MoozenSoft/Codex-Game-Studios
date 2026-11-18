# Codex 迁移与后续更新

本次迁移覆盖当前仓库本身及从本仓库新建游戏项目，不提供任意已定制上游项目的通用自动升级器、冲突合并或无损升级承诺。
迁移过程和每项来源处置见 `studio-tests/migration-inventory.json`，实现方案见 `docs/superpowers/plans/2026-11-16-codex-adaptation.md`。

## 运行机制变化

- 根与目录 AGENTS.md 取代旧客户端入口；不依赖 @ 自动导入。
- 75 个正式 Skills 位于 .agents/skills；旧名 help、settings、changelog 退役，分别使用 next-step、project-settings、write-changelog。
- 49 个角色改为 Codex 原生 TOML，模型与推理强度默认继承父会话；原 tools、maxTurns、memory、isolation 字段不能按名称视为等价权限。
- 配置解析顺序与 rigor 展开保留，三种协作模式保留且默认 collaborative。
- hooks 使用 Codex 事件、实际 patch 输入和正常信任流程；Notification/statusLine 无完整对应项时明确退役。
- .worktreeinclude 不作为 Codex 配置。个人配置和工作树规则见 .agents/docs/worktree-setup.md。

## 已有定制项目

先保留自己的分支、配置、游戏代码与检查点，再按文件核对迁移差异。人工处理自定义 Skills、角色、引擎命令和私有设置，不能把上游权限 JSON 直接复制进 TOML。
项目值仍保存在 project.yaml；个人白名单值位于 project.local.yaml。源框架 v1 配置转换脚本只处理游戏配置数据，不提供旧客户端运行兼容层。
旧实现和许可可从 Git 历史追溯；不要因框架升级覆盖用户游戏或误把新 AGENTS.md 判成已有游戏代码。
