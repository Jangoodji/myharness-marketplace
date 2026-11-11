"""프로젝트 자체 린터를 Edit · Write 뒤에 돌리는 PostToolUse Hook.

린트 규칙은 프로젝트마다 다르므로 플러그인에 넣지 않는다.
프로젝트에 `scripts/arch_lint.py` 가 있으면 그것을 실행하고, 없으면 아무것도 하지 않는다.
  - 프로젝트에 uv.lock 이 있으면 `uv run --project <프로젝트> python ...` 로,
    없으면 이 Hook 을 돌리는 python 으로 실행한다.
  - 린터가 exit 2 와 함께 stderr 에 남긴 수정 지침은 그대로 에이전트에게 전달된다.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

LINT_SCRIPT = Path("scripts") / "arch_lint.py"


def main() -> int:
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    sys.stdin.read()
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    script = root / LINT_SCRIPT
    if not script.is_file():
        return 0
    if (root / "uv.lock").is_file() and shutil.which("uv"):
        cmd = ["uv", "run", "--quiet", "--project", str(root), "python", str(script)]
    else:
        cmd = [sys.executable, str(script)]
    result = subprocess.run(cmd, cwd=root, capture_output=True, text=True, encoding="utf-8")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
