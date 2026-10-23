from __future__ import annotations
from agentfit.taxonomy import KIND_MCP_SERVER,KIND_AGENT_SKILL,KIND_CLI_TOOL,KIND_LIBRARY,KIND_PLUGIN
CLIENTS=("claude_code","codex","cursor","opencode")
def compatibility(kind):
 if kind==KIND_MCP_SERVER:return {x:"? MCP-capable client; verify transport/config" for x in CLIENTS}
 if kind==KIND_AGENT_SKILL:return {"claude_code":"? likely Agent Skill","codex":"? skill formats vary","cursor":"? skill formats vary","opencode":"? skill formats vary"}
 if kind in (KIND_CLI_TOOL,KIND_LIBRARY):return {x:"✓ via shell/code integration" for x in CLIENTS}
 if kind==KIND_PLUGIN:return {x:"? client-specific plugin; verify" for x in CLIENTS}
 return {x:"? unverified" for x in CLIENTS}
