`APP_AUDIT_458B4A0_RECOVERY_a42d`（仅取自启动上下文）

- `Get-Location` 与 `git rev-parse --show-toplevel` 均确认根目录为 `<app-probe>`。
- 使用指定 Git Bash、当前 checkout 的 helper 和指定 `--root` 查询成功，退出码 `0`；沙箱启动失败后已走正常审批。
- `engine: Web (project.yaml)`
- `engine_values: name=Web(project.yaml) version=unset language=unset`
- 派生根：`code_root=src`、`test_root=tests`、`asset_root=assets`；来源为 `.agents/engines/engines.tsv`。
- 本地 `engine.name` 不允许覆盖共享配置，已被忽略；提示移入 `project.yaml` 或删除。

两项 modified 工具 hooks 仍需用户正常审阅；本次工具执行不能证明它们已触发。全程未写文件、构建、安装、委派、提交或修改信任。