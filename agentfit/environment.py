from __future__ import annotations
import os,platform,shutil

def detect_environment():
    tools={x:shutil.which(x) for x in ("git","node","npm","npx","python","python3","pip","pip3","uv","docker","code")}
    clients={
      "claude_code": bool(shutil.which("claude") or os.path.exists(os.path.expanduser("~/.claude"))),
      "codex": bool(shutil.which("codex") or os.path.exists(os.path.expanduser("~/.codex"))),
      "opencode": bool(shutil.which("opencode") or os.path.exists(os.path.expanduser("~/.config/opencode"))),
      "cursor": bool(shutil.which("cursor") or os.path.exists(os.path.expanduser("~/.cursor"))),
    }
    return {"os":platform.system().lower(),"arch":platform.machine().lower(),"python":platform.python_version(),"tools":{k:bool(v) for k,v in tools.items()},"clients":clients}
