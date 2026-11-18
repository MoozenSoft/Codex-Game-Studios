# 真实浏览器回归

此目录的测试与普通框架70项检查分开，必须提供已经安装的实际浏览器，缺环境不能当作通过，也不会自动下载安装。

在开发虚拟环境中设置 `CGS_TEST_BASH`、`CGS_TEST_BROWSER` 为实际可执行文件，再运行：

```text
python -m unittest discover -s studio-tests/browser -p 'test_*.py' -v
```

`test_import_runner.py` 用最小HTML分别覆盖已有手动测试hook和普通RAF游戏。前者包含resize清空canvas的真实条件；导入模式不应把游戏停在manual状态。原缺陷先复现黑图，修复后两例都通过实际Chrome绘制，不以进程退出0替代画面结果。

当前两例在ASCII临时目录执行，不能据此宣称浏览器所有中文/空格路径已验证。App原项目的实际黑图、对照复现和后续接续结果分别保存，不覆盖首轮失败。
