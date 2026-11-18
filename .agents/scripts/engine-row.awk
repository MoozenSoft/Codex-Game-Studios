# 从 .agents/engines/engines.tsv 读取引擎行或指定列，所有调用者共用此表。
# 用法：awk -F'\t' -v engine="Godot" -v col=code_root -f engine-row.awk engines.tsv
# col 为空时输出完整 TSV 行；未知列、引擎或空单元格（-）输出空字符串。
# 引擎名称忽略大小写，unreal 前缀匹配 Unreal 行，保留既有引擎名称兼容行为。
# 调用者必须提供 -F'\t'，避免 Bash IFS 合并空字段；兼容 CRLF 与 BWK awk。

function lc(s) { return tolower(s) }
BEGIN { want = lc(engine); sub(/^[ \t]+/, "", want); sub(/[ \t]+$/, "", want) }
{ gsub(/\r/, "") }
NR == 1 { for (i = 1; i <= NF; i++) if ($i == col) c = i; next }
/^#/ || $0 == "" { next }
want == "" { exit }
{
  row = lc($1)
  if (want != row && !(row == "unreal" && index(want, "unreal") == 1)) next
  if (col == "") { print; exit }
  if (c && $c != "-" && $c != "") print $c
  exit
}
