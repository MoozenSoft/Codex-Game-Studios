# 贡献规范

本项目只适配 Codex。先读取根 AGENTS.md 和目标目录规范，中文讨论、注释、提交标题及 PR 描述，不添加 AI 工具或模型署名尾注。

Skills 只维护在 `.agents/skills/<name>/SKILL.md`，角色规范只维护在 `.codex/agents/<name>.toml`。
保留游戏开发领域规则；工具和配置必须有 Codex 可执行机制，不能仅替换名称。
新入口同步 catalog、行为规范、公共引用和运行矩阵；客户端能力与角色权限使用实际可用 schema，不能从正文推断硬权限。

先写能捕获具体故障的测试并观察失败，再实现；脚本测试检查实际输出、状态与产物。仅改普通文档无需镜像文字测试。
完整检查先在开发虚拟环境安装 `studio-tests/requirements.txt`，再执行 unittest、`studio-tests/validate-yaml.py` 与 validate-framework。记录真实 Codex 场景和未评估项，不能将静态检查当成运行验收。
同一已测 tree 在基线未变的整合中复用测试结果，遇到具体新风险只补必要验证。

PR 描述说明问题、最终行为、验证和限制；提交范围明确，保留用户既有改动。不要推送或发布未经当前会话授权的内容。
