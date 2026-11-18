# Codex-Game-Studios Agent 开发规范

本文件是 Codex-Game-Studios 仓库内各类 AI Agent 的通用开发规范（Single Source of Truth）。修改源码、工具链、文档和构建配置时均应遵守。

## 沟通与文档语言

- **中文优先，专业术语可使用英文。**
- 讨论、分析、设计说明、代码评审和项目文档优先使用简体中文；必要时保留专业术语。
- 从上游迁移的专业职责、工作步骤和领域参考保留英文原文，不压缩翻译；客户端专属工具、路径、授权和生命周期约定按 Codex 用英文定点适配，记录原句、替换内容及原因。以来源哈希和差异记录追溯，不在仓库重复保存整份角色原文，也不把不适用的旧指令整篇注入角色运行配置。
- 代码注释使用简体中文，专业术语可保留英文。注释应简明，说明原因或约束，不复述代码。
- 代码标识符、命名空间、API、命令行参数、文件路径及约定的配置键保持其原有拼写，不要为翻译而更名。

## 提交与协作

- **提交信息与 PR 描述同样使用中文**：只保留标题与中文说明体，标题也使用中文。
- **不添加任何 AI 工具或模型署名尾注**，包括 `Co-Authored-By:`、`Generated-with:`、`Signed-off-by:` 等；工具自带的署名默认值和计划模板均不得覆盖本规则。

## 项目及仓库

- **Codex-Game-Studios 基于 Claude-Code-Game-Studios 改造**，是面向游戏开发的 Agent 协作与工作流框架。
- **本项目只适配 Codex**。框架入口、Skills、Agent 协作、工具调用、配置和验证均以 Codex 为目标，不维护 Claude Code 或其他 Agent 客户端的兼容层。
- 本地工作目录以当前 checkout 为准，远程仓库以当前 Git 配置为准。
- 上游 `.claude/`、`CLAUDE.md` 与专用命令已退役；来源哈希、迁移目标与退役理由保存在 `studio-tests/migration-inventory.json`，历史资料不作为当前运行入口。

## 开发原则

- 保留上游有价值的游戏开发流程与领域规则，将 Claude 专用约定迁移为 Codex 可执行的机制；不能仅替换名称或目录就宣称适配完成。
- 迁移功能时同步更新相关文档、配置、引用和测试；区分静态检查与实际运行验证，明确记录尚未迁移或未验证的能力。

## Agent 工作方式

- 委派前读取 `.codex/agents/<role>.toml`。角色声明模型家族时，按 `.agents/docs/model-tiers.md` 解析当前可用型号并显式传入。未声明家族的角色使用会话默认值。Skill 选模也遵循同一规则。
- 统一通过 **Codex** 工作，使用当前环境提供的本地文件、终端及已连接工具。
- 共享 Agent Skills 的唯一规范目录为 `.agents/skills/`；新增及维护均在此目录进行。

## 工作入口与验收

- 游戏工作流从 `$start`、`$prototype` 或 `$next-step` 进入；有同名插件时核对加载的是本项目 `.agents/skills/<name>/SKILL.md`。
- 项目角色位于 `.codex/agents/`，委派合同与能力降级见 `.agents/docs/codex-runtime.md`。实际工具未提供的接口不得编造调用成功。
- 默认 `collaborative`，支持 `guided` 与 `autonomous`；按 `.agents/docs/automation-modes.md` 执行并复用本会话已有授权。
- Python 工具通过 `bash .agents/scripts/python-run.sh <脚本及参数>` 选择真实解释器。Windows PowerShell 按 codex-runtime.md 定位实际 Git Bash，不裸调用 WSL 的 bash 或 Python 安装器别名。
- 交付前运行 `bash .agents/scripts/python-run.sh .agents/scripts/validate-framework.py --scope all --format json`；框架完整迁移验收加 `--stage complete`。必要失败或必要检查无法执行时不能关闭相应故事或阶段，普通编辑可继续修复。
- 检查点由工作流写入 `production/session-state/active.md`。是否收到恢复内容以当前客户端实际事件为准；未信任 hooks、缺工具或未执行的检查明确报告。

## 领域规则与公共工具

- 修改游戏代码、数据、场景、设计或框架工作流前，运行 `bash .agents/scripts/python-run.sh .agents/scripts/rule-routing.py <目标路径...>` 并读取输出的领域规则；跨引擎 glob 不依赖客户端自动加载。
- 项目设置通过 `.agents/scripts/yaml-helper.sh resolve_config --keys ...` 显式读取，取值顺序和来源见 `.agents/docs/config-resolution.md`。
- `.agents/docs/`、`engines/`、`genres/` 保留共享领域资源；未完成迁移的工作流以 `studio-tests/migration-inventory.json` 状态为准，不能因目标文件已存在就宣称运行通过。
