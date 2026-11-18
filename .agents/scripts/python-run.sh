#!/usr/bin/env bash
# 复用解释器选择，不执行可能自动安装的 python/py 别名。
HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/yaml-helper.sh"
if ! _yaml_helper_resolve_python; then
  echo 'Python 检查未评估：缺少 Python 3.11+ 实际解释器，请设置 CGS_PYTHON。' >&2
  exit 2
fi
exec "$_yaml_helper_python" "$@"
