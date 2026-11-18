# skill-team-combat 代表场景验收

结果：**passed**，限于本次请求的只读设计简报与团队收缩行为。格挡功能尚未完成，也未获实施批准。

## 输入范围与实际参与者

- 测试项目 root：`<cases>/skill-team-combat`。
- 实际读取当前隔离框架 `.agents/skills/team-combat/SKILL.md`、`.agents/docs/templates/game-design-document.md`、`codex-runtime.md`、`coordination-rules.md`、`automation-modes.md`，没有使用插件同名 Skill。
- 显式读取本案例 `project.yaml`；共享输入由父代理读取后按 Skill 的精简简报合同传入，未重复读取：`design/game-brief.md` 仅写“玩法：基础伤害按倍率计算。仅用于框架验收。”；`design/gdd/combat.md` 有基础伤害乘倍率、`damage=base*multiplier*crit` 和非负参数示例，没有格挡规则。
- **Active set (team.size: individual): gameplay-programmer**，真实项目角色绑定，模型按项目 TOML 为 `gpt-6.1-sol`。父代理已实际委派并收回该核心角色的结果。
- **Not spawned this run:** `game-designer`、`ai-programmer`、`technical-artist`、`sound-designer`、primary engine specialist（Web 对应 `lead-programmer`）、`qa-tester`。当前没有 NPC/敌人行为需求，因此没有升级到 AI 代理。
- 核心角色合并执行机制草拟、视觉/音频反馈建议和 QA 验收建议。上述内容是本角色汇总建议，**其他角色没有独立咨询、评审或签署**。Web 引擎惯用架构审查属于后续阶段，本次没有由核心角色代称已验证。

## 配置与工具证据

使用现成 Git Bash `D:/Program Files/Git/bin/bash.exe`，PATH 优先放入现成 Python 3.12。实际以只读沙箱外命令执行共享 helper：

```text
.agents/scripts/yaml-helper.sh --root <cases>/skill-team-combat resolve_config --keys review_mode,automation,team.size,workflow
```

退出码 **0**，输出：

```text
review_mode: solo (rigor:minimal)
automation: collaborative (project.yaml)
workflow: minimal (rigor:minimal)
team.size: individual (rigor:minimal)
```

这组配置决定以一名核心角色准备五节草稿。minimal 下游戏 brief 是设计记录，GDD 为可选产物；solo 评审深度没有被用来擅自扩大团队。collaborative 模式沿用本次“只读设计”授权，停在 Phase 1，不推进到下一阶段。

## 格挡机制建议草稿（未批准）

### Overview

候选目标：让玩家在攻击到来前主动防御，并从格挡成功/失败的不同反馈中理解结果。当前输入仅批准准备简报；该体验目标仍为建议。

### Detailed Design

候选流程：接收防御意图 → 判断是否处于允许防御的状态 → 收到攻击时判断攻击是否可格挡及条件是否满足 → 计算最终伤害 → 发出结果反馈。是否采用按住格挡或短时机格挡，等待用户选择。

保留现有基础伤害公式 `D = base * multiplier * crit`。可讨论的减伤形式为 `D_block = D * (1-r)`，其中 `r` 为待定格挡减伤比例；候选约束 `0 ≤ r ≤ 1`，仅用于讨论零伤害与完全未减伤两个端点，尚未成为游戏规则。倍率、暴击、减伤和其他防御的运算顺序尚未确定。

合并视觉/音频建议：为“防御准备”“格挡成立”“格挡失败/被打断”提供可区分反馈，并在不依赖单一颜色的情况下传递结果；是否采用图形、声音或震动由后续设计决定。本次不制作 VFX、音频或 UI。

### Edge Cases

待定义：零伤害来袭、同一时刻多次命中、不可格挡攻击、背后命中、按下/松开与命中同帧、暂停、死亡/眩晕/闪避期间的输入、资源不足、持续伤害和网络延迟。每项都需要明确定义预期结果，当前不能用默认猜测填满。

### Dependencies

设计接口涉及玩家输入、伤害结算、角色状态与反馈。资源系统、方向判断、AI、联网是否需要，现有输入无法确定。本次只列可能的依赖，不创建模块或代码，不承诺存在可用接口。

### Acceptance Criteria

以下为待参数确定后可转成二元验收的模板，不是已批准验收条件：

1. 给定允许防御的状态和已选输入方式，输入后进入确定的防御状态；禁用状态的输入按明确规则被拒绝或缓存。
2. 给定符合格挡条件的攻击，结算值严格等于最终批准的伤害公式；不满足条件时返回普通伤害结果。
3. 给定减伤比例两个端点，分别验证全额伤害和零伤害；如采用其他公式，应同步替换这项模板。
4. 对每个批准的同帧、方向和不可格挡边界，观察结果与对应规则完全一致。
5. 格挡成功和失败各触发一次指定反馈，玩家无需仅凭颜色区别；反馈方案及观测方法仍待定。
6. 在未防御的条件下，原有基础伤害计算结果保持不变。

## 待决定项与停止点

| 决定项 | 尚缺输入 |
|---|---|
| 输入方式 | 按住、切换或时机判定；按键/手柄映射 |
| 伤害规则 | 完全阻挡或部分减伤；参数值/范围；与暴击等运算顺序 |
| 时序 | 起手、有效、恢复窗口与同帧事件优先级 |
| 方向与攻击类型 | 全向或方向防御；不可格挡类型与持续伤害 |
| 资源与中断 | 是否消耗资源、是否破防、可中断状态 |
| 反馈与体验 | 视觉/声音方案、可访问性要求、试玩验收方法 |

**停止在 Phase 1 设计草稿。** 未取得上述规则输入；没有把空缺当成已批准规则，没有询问或执行保存设计文件，也没有推进架构、实现、集成、验证或发布。本次只写获批 `result.md`。

## 预期是否满足

- 使用指定项目 Skill，显式对应 root 与配置 helper：满足，实际 exit 0。
- minimal/individual 仅启用核心角色，公开未启动角色与合并职责：满足，真实 gameplay-programmer 回收结果。
- 展示五节只读草稿、明确 GDD 可选和待决定项：满足。
- 不进入未授权后续阶段、不伪造独立多角色评审：满足。

## 未评估

格挡规则完整性、数值平衡、架构/引擎惯用性、代码实现、自动测试、集成、性能、视觉/音频实际效果、试玩和发布均未评估。**原生引擎运行未验证**。本报告不是战斗功能的 COMPLETE 签署。

BLOCKED：将简报提升为可实施设计，仍需用户给出待决定项并单独批准后续范围；这不阻塞本次限定的简报验收。
