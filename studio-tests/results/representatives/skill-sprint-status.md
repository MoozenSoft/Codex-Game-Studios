# skill-sprint-status 场景验收

场景结果：passed。输入范围：root 为 runtime-cases/skill-sprint-status 的 project.yaml、production/sprint-status.yaml 与存在的 EPIC-001-S01 故事。实际读取当前 .agents/skills/sprint-status/SKILL.md 和运行约定；未使用插件。
共享 yaml-helper.sh 显式 --root 本案例，退出 0：workflow minimal、story_granularity coarse（rigor:minimal）、automation collaborative（project.yaml）。

按用户明确指定的 YAML 范围汇总。没有 sprint markdown 计划，未让 minimal 的无 sprint 分支替换该指定输入；单位为 feature-sized 故事。

| Story | YAML 原始状态 | Owner / Priority / Blocker |
| --- | --- | --- |
| EPIC-001-S01 | Done | 未提供 |
| EPIC-001-S02 | In Progress | 未提供 |
| EPIC-001-S03 | TODO | 未提供 |

登记进度：Done 1/3（33.3%），进行中 1 项，待开始 1 项。这是登记统计，不代表完成证据已验证。In Progress 没有计为完成。

实际读取 YAML；以案例为 workdir 搜索故事日期，没有时间戳。S02/S03 未提供对应故事文件；S01 文件为 TODO，与 YAML Done 冲突，原样报告、不改写。综合读取命令退出 1（production/sprints 不存在）；YAML 已成功读取，不能把综合退出码报作全流程通过。

未评估：无起止日期、目标，Days Remaining / burndown 为 unknown；S02 无对应文件和时间戳，stale 天数不可计算；无优先级，Must Have 风险不可判断。原生引擎运行未验证。

唯一建议：核对 S01 的 Done 证据与故事状态冲突。没有修改 sprint、故事或阶段，仅写本报告。
