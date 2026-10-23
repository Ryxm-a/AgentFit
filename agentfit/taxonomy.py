from __future__ import annotations
CAPABILITY_LEXICON = {
 "ghidra":["ghidra","reverse-engineering"], "reverse engineer":["reverse-engineering","binary-analysis"],
 "reverse engineering":["reverse-engineering","binary-analysis"], "decompile":["reverse-engineering","binary-analysis"],
 "disassemble":["reverse-engineering","binary-analysis"], "webassembly":["webassembly","binary-analysis"], "wasm":["webassembly","binary-analysis"],
 "malware":["malware-analysis","security"], "ctf":["binary-analysis","security"], "wordpress":["wordpress","security"],
 "vulnerability":["security","vulnerability-scanning"], "vulnerabilities":["security","vulnerability-scanning"], "security audit":["security","vulnerability-scanning"], "pentest":["security","vulnerability-scanning"],
 "semgrep":["static-analysis","security"], "codeql":["static-analysis","security"], "browser automation":["browser-automation"], "playwright":["browser-automation","testing"],
 "scrape":["web-scraping"], "scraping":["web-scraping"], "crawler":["web-scraping"], "github":["github"], "issues":["issue-tracking"], "pull requests":["code-review"],
 "mcp":["mcp"], "model context protocol":["mcp"], "skill":["agent-skill"], "plugin":["plugin"], "agent":["agent-tooling"],
 "powerpoint":["presentation"], "pptx":["presentation"], "presentation":["presentation"], "pdf":["pdf"], "ocr":["ocr"], "excel":["spreadsheet"], "spreadsheet":["spreadsheet"],
 "database":["database"], "postgres":["postgres","database"], "supabase":["supabase","database"], "sqlite":["sqlite","database"], "stripe":["payments","stripe"],
 "react native":["react-native","mobile-development"], "ios":["ios","mobile-development"], "xcode":["xcode","ios"], "metal":["metal","graphics"], "c++":["cpp"],
 "android":["android","mobile-development"], "docker":["containers"], "kubernetes":["containers","orchestration"], "terraform":["infrastructure-as-code"], "aws":["cloud-aws"],
 "slack":["messaging-slack"], "notion":["productivity-notion"], "jira":["project-management-jira"], "google drive":["storage-gdrive"], "gmail":["email-gmail"], "calendar":["calendar"],
 "python":["python"], "typescript":["typescript"], "javascript":["javascript"], "rust":["rust"], "cli":["cli"], "command line":["cli"],
}
LABELS = {x:x.replace("-"," ").title() for vals in CAPABILITY_LEXICON.values() for x in vals}
STRONG_TAGS={"reverse-engineering","binary-analysis","webassembly","security","vulnerability-scanning","browser-automation","github","mcp","agent-skill","presentation","ocr","ios","xcode","supabase","stripe"}
GITHUB_TOPIC_HINTS={"mcp":["topic:mcp-server"],"agent-skill":["topic:agent-skills"],"reverse-engineering":["topic:reverse-engineering"],"binary-analysis":["topic:binary-analysis"],"webassembly":["topic:webassembly"],"security":["topic:security"],"browser-automation":["topic:browser-automation"]}
KIND_MCP_SERVER="mcp_server"; KIND_AGENT_SKILL="agent_skill"; KIND_PLUGIN="plugin"; KIND_CLI_TOOL="cli_tool"; KIND_LIBRARY="library"; KIND_UNKNOWN="unknown"

def classify_kind(name:str, description:str="", topics:list[str]|None=None)->str:
    topics=[str(t).lower() for t in (topics or [])]
    blob=f"{name} {description} {' '.join(topics)}".lower()
    if any(x in topics for x in ("mcp","mcp-server","model-context-protocol","modelcontextprotocol")) or "model context protocol" in blob or "mcp server" in blob:return KIND_MCP_SERVER
    if any(x in topics for x in ("agent-skill","agent-skills","claude-skill","claude-skills")) or "skill.md" in blob:return KIND_AGENT_SKILL
    if "plugin" in topics or " plugin " in f" {blob} ": return KIND_PLUGIN
    if any(x in topics for x in ("cli","command-line","command-line-tool")) or name.lower().endswith("-cli") or " cli " in f" {blob} ": return KIND_CLI_TOOL
    if any(x in topics for x in ("library","sdk","framework")): return KIND_LIBRARY
    return KIND_UNKNOWN
