# 受控项目输入

`python studio-tests/fixtures/projects/prepare-modes.py --output <不存在的目录>` 生成九个相互隔离的项目配置和请求，覆盖三种模式、授权复用、必要问题空回答与四个保留协作阶段的工作流。

生成器只建立输入，不运行模型或把 expected 写成通过结论。真实执行结果见 `studio-tests/results/runtime-evidence/mode-matrix-result.md`；原轮两份规格保存、七例等待必要回答，不能称九例所有后续步骤均完成。

普通脚本/事件/配置测试用临时项目创建输入，不把生成游戏代码放入框架模板。显式 Story 的正反向输入与结果保留在 `runtime-evidence/core-story/`。
