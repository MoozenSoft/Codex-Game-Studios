# 个人配置与共享配置

游戏共享设置在 `project.yaml`，个人允许覆盖的键写入忽略的 `project.local.yaml`。具体键与优先级见 `config-resolution.md`；使用 `$project-settings` 或 `config-set.sh` 修改并核对来源。

Codex 项目共享配置在 `.codex/config.toml`，角色在 `.codex/agents/`，事件注册在 `.codex/hooks.json`。不要把上游客户端的 JSON 权限列表、statusLine 或隐式导入复制到这里。

个人 Codex 偏好通过当前客户端设置或其用户配置维护。本仓库不生成或改写用户全局配置，也不把协作模式当成权限开关。迁移或新 clone 时，先只读核对实际配置层和受信任目录，再审阅所需 hooks。

本地会话检查点、事件日志和角色记忆均已忽略。对本机工具路径的说明可写个人笔记；不会因为文件名叫 `AGENTS.local.md` 就自动加载。实际需要的额外规范必须由适用的 `AGENTS.md` 明确要求读取，且不得覆盖用户已有指令。
