# 环境要求与排查

| 依赖 | 用途与边界 |
| --- | --- |
| Codex CLI / Windows App | 共用项目 Skills、角色及 hooks；当前实测版本见 `studio-tests/results/codex-capabilities.md` |
| Git 与 Bash | 共享 Bash/awk 工具；Windows 使用 Git for Windows 自带 Bash |
| Python 3.11+ | TOML 解析、JSON 与框架校验；只使用标准库 |
| 浏览器 | Web 原型的实际输入、截图与行为验证；缺失时标记未评估 |
| Node.js | Web 工程的依赖安装、构建和测试；以随模板锁定的版本要求为准 |
| 原生引擎 | 仅在选择对应引擎时需要；项目配置固定版本，编辑器验收单列 |

## Windows

在项目根运行 Git 与 Codex。PowerShell 包装脚本被拒绝时可用 `codex.cmd`；不要修改机器执行策略作为迁移步骤。hooks 的 Windows 启动命令通过 Git 的实际安装位置找到 Git Bash，再由 `run.sh` 选择实际 Python。
Skills 的 Bash 代码块也必须使用实际 Git Bash；PowerShell 中的裸 `bash` 可能命中系统 WSL。按 [codex-runtime.md](codex-runtime.md) 的命令解析安装位置，再传入原脚本及参数。

有些机器的 `python` 或 `py` 指向 Python Install Manager，探测会触发联网或自更新。框架优先选择已经安装的解释器，跳过已知安装器和系统别名；可通过 `CGS_PYTHON` 指定解释器的完整路径。指定无效时明确失败，不退回另一个解释器冒充成功。无需为验收运行 `py list` 或安装新的 Python。

## 信任和权限

项目与 hooks 按客户端正常入口审阅。权限来自当前 Codex 环境，角色文档与协作模式均不扩大 sandbox 权限。工具未提供、hook 未信任、依赖缺失或 GUI 无法操作时，报告具体未评估项；禁止绕过信任状态。

## 游戏运行

先以项目固定的引擎版本检查。Web 工程按锁文件安装依赖；未经已有任务授权不要全局安装工具。截图与自动输入分开记录；人工试玩不由 headless 测试替代。需要运行窗口但环境拒绝时，保留失败输出，只对必要的具体启动申请授权。

Linux CI 的配置与本地 Windows 实测分开记录；未运行的远端 CI 或原生引擎不记为通过。
