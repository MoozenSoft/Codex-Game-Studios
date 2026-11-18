# skill-project-settings 场景验收

场景结果：passed；设置操作：REJECTED（个人白名单拒绝）。

输入范围：root 为 runtime-cases/skill-project-settings，请求 --local engine.name=Godot。读取当前 .agents/skills/project-settings/SKILL.md、配置解析与运行约定，显式读取本案例 project.yaml，原值 Web。未使用插件。

配置解析共享 yaml-helper.sh 显式 --root 本案例，退出 0：automation collaborative（project.yaml），minimal / solo / individual（rigor:minimal），engine Web（project.yaml）。

实际按 Set-local Phase 5.1，在写入前运行共享 yaml-helper.sh --root <本案例绝对root> is_locally_overridable engine.name。输出 1，退出 1。这是白名单查询拒绝，不是启动失败。

结论：engine.name cannot be locally overridden — it's a project-wide setting.
在此停止；未转而修改共享配置。若将来需要更改共享引擎，须另行明确范围，本轮不执行。

预期满足：拒绝非白名单覆盖；project.yaml 保持 Web，未创建 project.local.yaml，仅写本获批报告，没有重复询问授权或修改框架。

未评估：后续枚举验证、known-key 查询、实际写入、Godot 版本与构建设置因前置拒绝未执行；不称完整设置流水线通过。原生引擎运行未验证。

环境：沙箱内 Bash 启动失败，沙箱外只读 helper 成功，无依赖安装。
