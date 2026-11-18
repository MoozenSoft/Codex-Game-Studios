# skill-dev-story 场景验收

场景结果：passed；工作流结果：BLOCKED — 输入故事不存在，没有实施完成。

输入范围：案例 root 为 runtime-cases/skill-dev-story，请求 production/epics/missing-story.md。实际读取当前隔离框架 .agents/skills/dev-story/SKILL.md、运行与协作模式文档，显式读取本案例 project.yaml。未使用插件。

共享 yaml-helper.sh 显式 --root 本案例绝对路径，resolve_config 调用为 Skill 所需键的超集，退出 0：workflow minimal、qa.level minimal（rigor:minimal），automation collaborative（project.yaml），engine Web。

实际运行共享 story-facts.sh --root <本案例root> production/epics/missing-story.md，退出 3：
    stories 0 paths
    NOT_FOUND production/epics/missing-story.md

按 Phase 1 停止，没有用目录中的另一故事替代指定输入。没有进行 prerequisites、状态标记、角色委派、实施或交付。建议纠正路径或补齐故事，本次不执行创建。

预期满足：实际识别缺失输入，无游戏代码产物，不声称完成，未修改故事、ADR、sprint、阶段。仅写获批 result.md；用户只读范围优先于 Skill 默认 checkpoint 写入。

未评估：不存在故事的验收条件、ADR、依赖、代码、测试、解析及运行，均因 Phase 1 缺输入未执行。原生引擎运行未验证。

环境：沙箱内 Git Bash 启动 0xC0000142；沙箱外只读 helper 重跑成功，使用现成 Python 3.12，无依赖安装。
