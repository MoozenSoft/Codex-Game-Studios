# 工作室框架测试规范

这里测试框架的 Skills、角色和公共脚本，与框架生成的游戏测试分开。
`catalog.yaml` 的 `spec` 和 `category` 是行为规范定位依据，角色规范目录层级与 rubric 类别可以不同。

正式 Skills 位于 `.agents/skills/`，角色的唯一规范定义位于 `.codex/agents/`。
测试引用的共享资料位于 `.agents/docs/`；根 AGENTS 和目标子目录 AGENTS 的规范同时适用。

行为 fixture 默认使用 `modes.rigor: minimal`、`modes.automation: collaborative`；案例显式设置优先，本地文件只有案例明确需要时才创建。
默认值案例不注入上述设置。记录行为受某个模式影响时，说明 fixture 使用的模式，不能用默认值变化改变验收含义。

自动化入口为 `python -m unittest discover -s studio-tests/automated -p 'test_*.py' -v`；Windows 测试通过 `CGS_TEST_BASH` 指定 Git Bash 可执行文件。
来源清单区分 pending、active、retired；中间阶段只要求 active 组件的必需依赖闭合，最终阶段要求所有迁移记录处置完成。
静态、脚本、真实 Codex 运行和人工试玩分别记证；没有执行的场景不能改成 passed。真实探测保留输入、版本、结果与证据路径。

测试应执行实际脚本、检查输出和产物，避免仅搜索实现文本。测试产物使用临时目录，正式模板不混入测试游戏、用户凭据或私人会话内容。
