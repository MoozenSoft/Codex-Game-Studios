#!/usr/bin/env bash
# 保存 Codex 实际提供的图片文件路径；无路径时明确返回未评估。
HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/yaml-helper.sh"
if ! _yaml_helper_resolve_python; then
  printf 'not_assessed\t缺少可运行的 Python 3\n'
  exit 3
fi
exec "$_yaml_helper_python" "$HERE/references-save.py" "$@"
