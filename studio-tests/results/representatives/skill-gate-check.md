# skill-gate-check 场景验收

场景结果：not_assessed（完整自动扫描受限）；已评估的阶段裁决：FAIL，不能进入 Systems Design。正确拒绝推进及阶段不变已验证，完整 helper 集成未通过验收。

## 输入范围与模式

root 为 runtime-cases/skill-gate-check，显式读取本案例 project.yaml。实际应用当前隔离框架 .agents/skills/gate-check/SKILL.md、Concept→Systems Design 定义及 2b/3/4/5/6/7 参考流程、运行/协作模式与 director-gates 规则，未使用插件。
用户已指定 Concept 缺产物并要求只读检查下一阶段，沿用该授权，无重复阶段选择或写入询问。
共享 yaml-helper.sh 显式 --root 本案例绝对路径，退出 0：workflow full / qa.level full / review_mode full / team.size studio（rigor:full），automation collaborative、project.stage Concept（project.yaml）；performance.enforce warn、system_overrides none。

## 实际工具与结果

共享 artifact-check.sh --phase concept <本案例绝对root> 实际退出 1：
    artifact-check: catalog not found at <本案例root>/.agents/docs/workflow-catalog.yaml

脚本将 catalog 与被查项目根绑定；共享 catalog 实际在当前隔离框架。没有复制框架到案例、改脚本或改扫隔离框架的游戏产物来制造成功。因此自动 catalog 扫描及其 NO_CHECK 统计未评估；此限制保留为 suite not_assessed。

另以本案例为 workdir 实际 Test-Path / Python 路径盘点、rg 搜索与文件内容复核（成功读取命令退出 0），直接核对当前 gate 的三个必需项：

| 当前阶段必需项 | 观察 |
| --- | --- |
| design/gdd/game-concept.md 有内容 | 不存在 |
| 概念文档或 game-pillars.md 定义 pillars | 两文档均不存在；design 搜索也无 pillars |
| Visual Identity Anchor，一条视觉规则与至少两原则 | 概念文档缺失，brief 无替代视觉方向 |

必需产物 0/3。现有 brief 仅写基础伤害倍率计算，combat GDD 的三节不能替代 full 概念文档。推荐 prototype / PROCEED 报告缺失，只列建议，不升级为必需项。
质量输入：概念审阅、完整核心循环、受众、视觉规则未有证据，均未确认通过。没有开展试玩、性能测试或替用户回答人工问题。当前 Concept gate 不要求未来阶段的代码测试或性能产物。

## 真实角色评审与回收

实际使用项目角色绑定，全部 Sol，均已回收；受三个子代理并发槽限制，分批执行，无共享文件并发写入。

| 角色及门禁 | 实际裁决 | 核心依据 |
| --- | --- | --- |
| creative-director / CD-PHASE-GATE | NOT READY | 缺概念、核心幻想、pillars、视觉锚点 |
| technical-director / TD-PHASE-GATE | NOT READY | 缺当前概念依据，不能可靠建立整体可行性 |
| producer / PR-PHASE-GATE | NOT READY | 范围与设计方向不完整，存在返工风险 |
| art-director / AD-PHASE-GATE | NOT READY | 无视觉规则及两支持原则 |

各角色读取其 TOML / gate 定义和本案例配置，以 --root 解析退出 0，均全程只读；没有由父代理模拟独立意见。架构、ADR 和完整 art bible 按 not expected before Pre-Production；sprint/capacity 按 not expected before Production，未列为本次阻塞。未来产物缺失没有被误算。

## Chain-of-Verification

1. 是否把建议当阻塞？prototype 仅建议；三个当前 required 缺项才是阻塞。
2. [TOOL ACTION] 概念与 pillars 真缺失？重跑本案例 Test-Path，两个均 False。
3. [TOOL ACTION] brief 可替代 full 概念/视觉方向？重读 brief 和 combat，并搜索 pillars/visual identity/核心循环/受众，未找到相应内容。
4. 是否漏报工具故障？保留 catalog 定位失败与自动扫描未评估。
5. 是否误要求未来产物或错误改阶段？四角色按目标阶段限定，重读 project.yaml 仍 Concept，stage.txt 不存在。

Chain-of-Verification: 5 questions checked — 阶段 FAIL unchanged；完整自动流程仍 not_assessed。

## 预期是否满足与未评估

拒绝进入下一阶段、指出缺项、保持 stage 的预期满足；完整自动 artifact 扫描未满足，不能宣称整个框架门禁执行无缺口。未自动修复、运行原型、改阶段或保存 gate-checks，只写此获批报告。
未评估：catalog 自动扫描、人工体验确认、整体概念可行性、视觉身份一致性及原生引擎运行。原生引擎运行未验证。
后续仅建议：补概念、pillars、视觉锚点后重新审查；本轮不执行。
