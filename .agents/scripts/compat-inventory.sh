#!/usr/bin/env bash
# 输出 Codex 原生文件的结构事实；不作领域通过裁决。
HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/yaml-helper.sh"
_yaml_helper_resolve_python || { echo "NOT ASSESSED: 缺少Python" >&2; exit 2; }
exec "$_yaml_helper_python" "$HERE/studio-inspect.py" compat "$@"
