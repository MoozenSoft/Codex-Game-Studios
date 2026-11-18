已核对 cwd 与 Git 根，均为 `<app-probe>`。已读取当前 checkout 的 QA 角色 TOML、要求的运行文档及指定输入。

共享 helper 实际解析成功：`automation=collaborative`、`workflow=minimal`、`review_mode=solo`、`team.size=individual`。Git Bash 首次在沙箱内启动失败，经批准重试后退出码为 0。

## Test Case: QA-001 — 正常：合法事件递增

**分类**：Logic；证据目录规范：`tests/unit/[system]/`（输入未指定具体子目录）；门禁：BLOCKING。本轮产物仅为对话用例草案。

**Precondition**：计数器处于初始状态，值为 0。

**Steps**：

1. 发送一次合法事件 `L`。
2. 读取计数器值。

**Expected Result**：计数器值为 1。

**Pass Criteria**：读取值等于 1 则通过，否则失败。

## Test Case: QA-002 — 边界：初始零值

**分类**：Logic；证据目录规范：`tests/unit/[system]/`（输入未指定具体子目录）；门禁：BLOCKING。本轮产物仅为对话用例草案。

**Precondition**：建立新的计数器初始状态，尚未发送事件。

**Steps**：

1. 在发送任何事件前读取计数器值。

**Expected Result**：计数器值为 0。

**Pass Criteria**：读取值等于 0 则通过，否则失败。该用例仅验证明确规定的初始零值，不将零推定为最小值。

## Test Case: QA-003 — 非法：事件保持原值

**分类**：Logic；证据目录规范：`tests/unit/[system]/`（输入未指定具体子目录）；门禁：BLOCKING。本轮产物仅为对话用例草案。

**Precondition**：计数器处于初始状态，值为 0。

**Steps**：

1. 发送一次合法事件 `L`，读取并记录计数器值。
2. 发送一次非法事件 `I`。
3. 再次读取计数器值。

**Expected Result**：发送 `L` 后为 1；发送 `I` 后仍为 1。

**Pass Criteria**：两次读取值均等于 1 则通过，否则失败。

文件验证标记：`APP_ROLE_MEMORY_59a7c2`。

本轮未写文件、未再次委派、未运行游戏或测试。以上均为待执行用例，实际功能结果及模型继承未评估。
