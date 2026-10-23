from __future__ import annotations
import shlex
from agentfit.models import UniversalCandidate

def install_command(c:UniversalCandidate)->str:
 if c.source=="mcp_registry":
  if c.install_hint.startswith("npm:"): return f"npm install -g {shlex.quote(c.install_hint[4:])}"
  if c.install_hint.startswith("pypi:"): return f"python -m pip install {shlex.quote(c.install_hint[5:])}"
  return "# Official MCP Registry entry found; configure it using the linked server documentation."
 if c.source=="npm": return f"npm install -g {shlex.quote(c.name)}"
 if c.source=="github":
  url=c.url[:-4] if c.url.endswith('.git') else c.url
  return f"git clone {shlex.quote(url+'.git')}"
 return "# No verified automatic installation recipe; follow the linked project's documentation."
