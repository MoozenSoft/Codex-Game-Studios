"""识别模板远端，仅输出分类，不读取或修改 Git 配置。"""

import re
import sys
from urllib.parse import urlsplit


TEMPLATES = {"moozensoft/codex-game-studios", "donchitos/claude-code-game-studios"}


def classify(url):
    if not url.strip():
        return "UNKNOWN"
    value = url.strip()
    scp = re.fullmatch(r"(?:[^/@:]+@)?github\.com:([^?#]+)", value, re.I)
    if scp:
        repository = scp.group(1)
    else:
        try:
            parsed = urlsplit(value)
        except ValueError:
            return "OTHER"
        if parsed.scheme.lower() not in {"https", "http", "ssh", "git"} or parsed.hostname != "github.com":
            return "OTHER"
        repository = parsed.path.lstrip("/")
    repository = repository.rstrip("/").lower()
    if repository.endswith(".git"):
        repository = repository[:-4]
    return "TEMPLATE" if repository in TEMPLATES else "OTHER"


if __name__ == "__main__":
    print(classify(sys.argv[1] if len(sys.argv) > 1 else ""))
