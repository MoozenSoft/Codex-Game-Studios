# 类别代表场景

15个场景覆盖9类 Skill、6类角色。original-suite-results.json 保留实际首轮14通过、1未评估；summary.json 另外记录 gate 共享catalog修复后的补扫，不覆盖原始结论。

来源输入可用 `python studio-tests/fixtures/prepare-representatives.py --output <空目录>` 重建。原始 ADR fixture 故意只有非标准的 Status 行，正式状态为未知并应阻断实施；普通列表 AC 的计数和人工文本判断分别记录。Godot场景仅为给定参考下的片段咨询，工程配置和编辑器运行不能据此判定通过。

所有报告均为真实 Codex 执行者产生。Python Install Manager 自动副作用和 Git Bash 启动限制继续保留在原报告；后续测试改用已安装解释器，未自动安装运行时。目录中的通过状态不写回 catalog 历史 last_spec 日期。
