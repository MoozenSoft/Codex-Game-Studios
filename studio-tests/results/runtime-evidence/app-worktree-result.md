# App 工作树隔离验收

日期：2026-11-17（Asia/Shanghai）  
结果：**PASS_WITH_NOTES**，限本轮终端 Git worktree 隔离检查。

- 原 checkout：`D:/Git/Codex-Game-Studios/.scratch/codex-capability-probe/app-web-acceptance`
- 原分支：`app-acceptance`
- 保留的新工作树：`D:/Git/Codex-Game-Studios/.scratch/codex-capability-probe/app-web-acceptance/.scratch/App 工作树 验收`
- HEAD：`6dd47426a2bf9cda5fac1fde3b0f1bcca8d184c5`
- tree：`993b8f1a02e87e2fbdb3962c0c7d63382471ac6a`
- 新工作树为 **detached HEAD**，与原 checkout 的 HEAD/tree 相同。

## 实际工具与写入

本轮允许工具范围内无可用原生工作树接口，按授权降级为 `git worktree add --detach`；没有调用 MCP、全局 Skills 或读取私有客户端数据，未选择或切换模型。

真实 Git Bash 由 `git --exec-path` 定位到 `D:\Program Files\Git\bin\bash.exe`。沙箱最初阻止 MSYS 初始化及 Git worktree 元数据写入；必要的具体命令通过正常提权后实际成功。Python 仅通过项目工具和 `python-run.sh` 使用已装 Python 3.12.10，未安装任何内容。

新工作树仅写入 `project.local.yaml` 与 `.scratch/app-worktree-marker.txt`；原 checkout 仅新增本报告及同名 JSON。Git worktree 管理元数据由 Git 创建。未提交、推送、修改框架/游戏，未写两份个人状态文件。

## 配置解析的实际 cwd 与输出

初轮调用的是原 checkout 的外部脚本 `D:/Git/Codex-Game-Studios/.scratch/codex-capability-probe/app-web-acceptance/.agents/scripts/yaml-helper.sh`；本次补充对照调用新工作树自己的脚本，两个入口分别记录。完整原始输出和退出码见 `app-worktree-result.json` 的 `commands`。

| 检查 | PowerShell 实际 cwd | Git Bash 的 pwd -P |
| --- | --- | --- |
| 原 checkout（前后两次） | `D:\Git\Codex-Game-Studios\.scratch\codex-capability-probe\app-web-acceptance` | `/d/Git/Codex-Game-Studios/.scratch/codex-capability-probe/app-web-acceptance` |
| 新工作树子目录 | `D:\Git\Codex-Game-Studios\.scratch\codex-capability-probe\app-web-acceptance\.scratch\App 工作树 验收\src` | `/d/Git/Codex-Game-Studios/.scratch/codex-capability-probe/app-web-acceptance/.scratch/App 工作树 验收/src` |

原 checkout 执行 `resolve_config --keys automation`，前后均退出 0：

```text
automation: collaborative (default)
```

从新工作树 `src` 执行 `--root .. resolve_config --keys automation`，退出 0：

```text
automation: guided (project.local.yaml)
```

本地配置按项目格式写为：

```yaml
modes:
  automation: guided
```

**入口归因更正：** 首次在新工作树 `src` 不带 `--root` 调用原 checkout 的外部脚本，实际返回 `automation: collaborative (default)`，原始输出保留；显式加 `--root ..` 后，该外部脚本读到 `guided (project.local.yaml)`。这是外部脚本的根定位结果。本次调用新工作树自己的脚本，不加 `--root` 即返回 `guided (project.local.yaml)`，退出 0，自身正常入口通过。此前“子目录自动向上寻根未通过”的表述归因过宽，现予更正；没有修改脚本。

## 补充：新工作树自身正常入口（不加 --root）

本次只补当前工作树自己的入口对照，未重复前轮其它验收。模型未切换。

- 实际 PowerShell cwd：`D:\Git\Codex-Game-Studios\.scratch\codex-capability-probe\app-web-acceptance\.scratch\App 工作树 验收\src`
- Git Bash 的 `pwd -P`：`/d/Git/Codex-Game-Studios/.scratch/codex-capability-probe/app-web-acceptance/.scratch/App 工作树 验收/src`
- 真实 Git Bash：`D:\Program Files\Git\bin\bash.exe`
- 脚本绝对路径：`D:/Git/Codex-Game-Studios/.scratch/codex-capability-probe/app-web-acceptance/.scratch/App 工作树 验收/.agents/scripts/yaml-helper.sh`
- 调用参数：`../.agents/scripts/yaml-helper.sh resolve_config --keys automation`，没有 `--root`。
- 实际退出码：`0`；预期匹配：**PASS**。

完整命令原始输出：

```text
POWERSHELL_CWD=D:\Git\Codex-Game-Studios\.scratch\codex-capability-probe\app-web-acceptance\.scratch\App 工作树 验收\src
GIT_BASH=D:\Program Files\Git\bin\bash.exe
HELPER_ABSOLUTE=D:\Git\Codex-Game-Studios\.scratch\codex-capability-probe\app-web-acceptance\.scratch\App 工作树 验收\.agents\scripts\yaml-helper.sh
COMMAND=bash ../.agents/scripts/yaml-helper.sh resolve_config --keys automation
/d/Git/Codex-Game-Studios/.scratch/codex-capability-probe/app-web-acceptance/.scratch/App 工作树 验收/src
automation: guided (project.local.yaml)
CONFIG_EXIT=0
```

该对照确认新工作树自身脚本的正常入口结果为 **guided (project.local.yaml)**。此前原 checkout 外部脚本不带 `--root` 的 `collaborative (default)` 原始输出完整保留在 JSON 的 `new_config_implicit_root`，不据此判断自身入口失败。

补记的 `post_report_verification.normal_entry_followup` 仅核验报告补记：JSON 可解析、新对照与实际输出一致、原有 8 条命令记录保留、Markdown 归因已修正。本次沿用前轮隔离证据，没有重跑其余验收；只更新这两份既有报告，不新增文件或修改原型、框架、配置，未提交。

## 隔离核对

两边分别实际执行 `git check-ignore -v -- project.local.yaml production/session-state/active.md production/agent-memory/probe.md`，均退出 0，原始输出一致：

```text
.gitignore:13:project.local.yaml	project.local.yaml
.gitignore:17:production/session-state/	production/session-state/active.md
.gitignore:15:production/agent-memory/	production/agent-memory/probe.md
```

- 新工作树 `git symbolic-ref -q HEAD` 退出 1，符合 detached 状态；status 无输出，普通及 cached diff 均退出 0。
- 新工作树被忽略的文件实际只有 `project.local.yaml` 和 `.scratch/app-worktree-marker.txt`。
- 原 checkout 的隔离标记实际不存在；`project.local.yaml` 前后均不存在，配置仍来自 default。
- 报告写入前，原 checkout 的 **1,076 个既有文件/缺失路径记录**逐项比较存在性、长度与 SHA-256，差异为 0；Git status、原有 diff、分支、HEAD、tree 均保持。
- 原有 `.agents/scripts/one-shot-run.sh` 修改与历史证据保留，旧 `production/session-state/active.md` 哈希不变；未写 `production/agent-memory/probe.md`。新工作树两份个人状态文件均不存在。
- 新工作树是当前 HEAD 的受跟踪快照，原 checkout 的未提交修改和未跟踪历史证据没有被复制。

## 未评估与停止边界

创建命令使用单次 `-c core.hooksPath` 禁用 Git hooks，未改持久 Git 配置。**新工作树 hooks 未重新信任、未测试**；配置脚本检查未新增信任。原生 App 工作树工具未测试。

本轮没有重复游戏测试、框架全量测试，也未评估人工试玩、体验/乐趣或原生引擎，不作 PROCEED/发布判断。工作树保留作证据，到此停止。

报告写入后的最终复核：排除本轮两份报告后，1,076 个既有文件/缺失路径记录仍完全一致；Git status、原有 diff、分支、HEAD 与 tree 均保持。原 checkout 实际只新增这两份报告。
