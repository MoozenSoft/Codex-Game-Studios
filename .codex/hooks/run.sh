#!/usr/bin/env bash
# 生命周期入口只查找真实 Python；缺少依赖时返回未评估，不启动安装管理器。
HERE="$(cd "$(dirname "$0")" && pwd)"
source "$HERE/../../.agents/scripts/yaml-helper.sh"
# 显式测试根目录与处理器一致；客户端默认使用当前 hook 所属 checkout。
_YH_EXPLICIT_ROOT="$(cd "$HERE/../.." && pwd)"
_cgs_root_next=0
for _cgs_arg in "$@"; do
  if [ "$_cgs_root_next" = 1 ]; then
    _YH_EXPLICIT_ROOT="$_cgs_arg"
    _cgs_root_next=0
  elif [ "$_cgs_arg" = --root ]; then
    _cgs_root_next=1
  fi
done
if ! _yaml_helper_resolve_python; then
  echo 'Codex hook 未评估：缺少 Python 3.11+ 实际解释器，可设置 CGS_PYTHON。' >&2
  exit 2
fi
export CGS_SESSION_STATE=on
if ! session_state_enabled; then export CGS_SESSION_STATE=off; fi
exec "$_yaml_helper_python" "$HERE/dispatch.py" "$@"
