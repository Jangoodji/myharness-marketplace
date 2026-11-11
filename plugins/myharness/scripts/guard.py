"""위험한 명령과 비밀 파일 읽기를 실행 전에 막는 PreToolUse Hook.

막는 것
  - Bash · PowerShell: rm -rf, Remove-Item -Recurse -Force, rmdir /s
  - Bash · PowerShell: git push --force / -f
  - Read: .env, .env.* (.env.example · .env.sample · .env.template 은 허용)

Hook 입력(JSON, stdin)의 tool_name 과 tool_input 을 검사하고,
막을 때는 exit 2 와 함께 이유를 stderr 로 돌려준다.
"""
import json
import re
import sys
from pathlib import PurePath

COMMAND_RULES = [
    (r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f|\brm\s+-[a-zA-Z]*f[a-zA-Z]*r",
     "rm -rf 는 막혀 있습니다. 지울 파일을 사람에게 확인받으세요."),
    (r"(?i)\bRemove-Item\b(?=.*-Recurse)(?=.*-Force)|\brmdir\s+/s\b",
     "재귀 강제 삭제는 막혀 있습니다. 지울 파일을 사람에게 확인받으세요."),
    (r"\bgit\s+push\b.*(--force\b|\s-f\b)",
     "git push --force 는 막혀 있습니다. 일반 push 를 쓰세요."),
]

SECRET_FILE = re.compile(r"^\.env(\..+)?$")
SECRET_ALLOWED = {".env.example", ".env.sample", ".env.template"}


def check_command(command: str) -> str | None:
    for pattern, reason in COMMAND_RULES:
        if re.search(pattern, command):
            return f"[guard] 차단: {command}\n이유: {reason}"
    return None


def check_read(file_path: str) -> str | None:
    name = PurePath(file_path.replace("\\", "/")).name
    if SECRET_FILE.match(name) and name not in SECRET_ALLOWED:
        return f"[guard] 차단: {file_path}\n이유: .env 파일은 읽지 않습니다. 필요한 값은 사람에게 물어보세요."
    return None


def main() -> int:
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    tool_input = data.get("tool_input") or {}
    if data.get("tool_name") == "Read":
        message = check_read(tool_input.get("file_path", ""))
    else:
        message = check_command(tool_input.get("command", ""))
    if message:
        print(message, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
