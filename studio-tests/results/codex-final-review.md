# Codex 迁移最终评审与处理

日期：2026-11-17。独立评审使用全新 Sol 上下文，范围 `7655fef..5cd40e4`，只读主 checkout，没有派生代理。原判定：With fixes，Critical 0、Important 3、Minor 2。按 executing-plans 做一次修复，不进行第二轮代理评审。

## Important

1. **必要失败可被旧关闭分支覆盖。** `story-done` Phase 7、CONTRACT 和行为规格仍允许 BLOCKED / NOT ASSESSED 后选择 close-anyway 并写 Complete，违背 Q9。修复为四状态关闭资格表；必要失败/未知为 DENY，不显示关闭选项，不写 Story/Epic/sprint 完成状态。真正需求变更先更新要求再重新验收；范围内已有批准继续复用。
2. **grow 丢失经典 script 的顶层绑定。** 原 `config-source.js` 被当 ES module 导入，顶层变量/函数成为模块私有。修复为经典 script 加载器，原配置在浏览器全局词法环境执行，JSON 仍提供集中可调参数；TypeScript 拆分后删除过渡加载器。
3. **归档 blob 不符合原始清单。** 139项中4份 JSON 的 CRLF 首次暂存时被转为 LF，之后普通 add 未刷新缓存。用限定路径的 `git add --renormalize` 重新纳入原始字节；覆盖所有原始归档和两个工作树报告，不改清单掩盖差异。

## 修复验证

- 三项均先观察到回归失败：关闭资格合同缺失、Node 和真实 Chrome 报 `ART is not defined`、139项 Git blob 审计有4项不匹配。
- 关闭合同、顶层 `var/let/const` 与函数、原始归档字节回归均转绿。原有 window 属性及 JSON 调参用例继续通过。
- 真实 CLI 压力用例在 autonomous 下执行必要单元测试，0通过/1失败，收到旧关闭回复后实际 BLOCKED / DENY；父会话核对 Story/Epic/sprint 仍为 In Progress，源值仍为3。模型目录刷新曾超时，但该回合实际完成，未把环境提示删除或改写为无异常。
- 真实 Chrome 已单独验证生成的配置加载器；此前导入绘制的两个真实 Chrome 回归保留。无需重跑完整游戏模型矩阵。
- 最终框架73/73（44.249s），YAML17/Skill75、TOML50、变更Bash语法及stage complete均通过。139项原始归档的暂存区blob审计通过；提交后再按HEAD复核，数据校验不重跑游戏模型矩阵。

## 延期 Minor

- `start` 仍仅识别上游模板 origin，本项目模板地址不会触发相同提醒。未自动更改远端，也没有自动推送路径；本轮按 Minor 延期。
- `dev-story` 的交接说明仍有“story-done 不运行测试”的旧句。实际关闭使用新资格门禁与必要运行结果合同；该处说明准确性按 Minor 延期。

## 未判断范围的裁决

- 原生引擎编辑器/构建/游戏运行按 Q7 后补，本次只声明规则、配置、脚本与角色迁移；代价是不能据此承诺编辑器兼容性。
- 人工体验、手感与乐趣仍未评估，不从自动截图推出 PROCEED；代价是仍需人实际试玩。
- PreCompact 实际触发、远端 CI、全部未单独实跑分支保留未评估；代价是这些路径的运行可靠性尚无完整证据。
- 辅助守卫保持有限规则检查器定位，不能代替客户端权限/沙箱；代价是复杂命令可能不被规则识别。
