# 游戏代码规范

使用引擎 API 前读取 `docs/engine-reference/<engine>/VERSION.md` 及对应模块参考，按项目固定版本核对签名。
公共 API 提供简明文档，游戏数值由数据文件配置，优先通过依赖注入保持可测试性。

架构文档要求按 `modes.workflow`：full 记录全部 ADR，standard 记录关键 ADR，minimal 可由 brief 与决策日志承载理由。
提交使用中文并关联已有故事或设计文档；项目根规范仍适用。

改动前使用 `.agents/scripts/rule-routing.py` 根据目标文件选择并读取玩法、UI、网络、AI、shader、数据等领域规则；其中的 glob 由脚本处理，不依赖客户端自动加载。
代码、shader 和 UI 的角色路由读取 `project.yaml` 的 `specialists`，缺少细分角色时使用 `specialists.code`。

Web/Godot 测试默认位于 `tests/`；其他引擎使用 `engine.test_root` 与引擎表解析。游戏机制先写测试，覆盖公式和边界。
可见变化需要运行并保留截图，解析通过不代表运行通过；交付证据位于 `production/qa/evidence/`。
