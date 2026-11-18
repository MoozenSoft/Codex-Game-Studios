当前 `src` 属于独立的 Git linked worktree，处于 **detached HEAD**。原 fixture 位于 `probe` 分支。两者的 HEAD 都是 `f56bab3c63f57504b0b9a73bd58426585412b53a`。

| Git 命令 | 审批重试后的实际输出 | 退出码 |
|---|---|---:|
| `git rev-parse --show-toplevel` | `<probe>/.scratch/CLI 全量 工作树` | `0` |
| `git rev-parse --git-dir` | `<probe>/.git/worktrees/CLI-全量-工作树` | `0` |
| `git rev-parse --git-common-dir` | `<probe>/.git` | `0` |

`git worktree list --porcelain` 输出了 `detached`，退出码为 `0`。`git symbolic-ref --quiet --short HEAD` 无输出，退出码为 `1`。

**配置实测**

- 当前工作树从 `src` 调用自身 `../.agents/scripts/yaml-helper.sh`，未传 `--root`，退出码为 `0`。输出为 `automation: guided (project.local.yaml)`、`rigor: minimal (default)`。`engine_row` 来自 `.agents/engines/engines.tsv`，报告 `engine=unset code_root=src(detected) test_root=unset asset_root=- run=- build=- test=- smoke=-`。
- 原 fixture `<probe>` 使用自身 helper，并将 `--root` 指向该目录，退出码为 `0`。实际输出为 `automation: collaborative (default)`。

**`git check-ignore -v` 实际退出码**

| 路径 | 从 `src` 直接检查 | 以工作树根目录为基准 |
|---|---:|---:|
| `project.local.yaml` | `0` | `0` |
| `production/session-state/active.md` | `1` | `0` |
| `production/agent-notes/qa-tester.md` | `1` | `1` |

根目录检查中，前两项分别命中 `.gitignore` 第 13 行和第 17 行，第三项没有命中。

**首次尝试失败**。默认沙箱中的 Git 命令均返回 `128`，报错为无法进入工作树根目录。两个 Git Bash 进程均返回 `-1073741502`，无输出。上面的结果来自审批后的只读重试。

**Hooks 信任状态为未评估**。没有收到相关客户端回执，本次路径测试未验证 hooks。全程未写入文件，未发生跨 checkout 写入，也未修改信任设置。
