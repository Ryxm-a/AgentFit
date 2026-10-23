from __future__ import annotations
from dataclasses import dataclass, field
import requests
from agentfit.taxonomy import KIND_MCP_SERVER
API_URL="https://registry.modelcontextprotocol.io/v0.1/servers"; TIMEOUT=5
@dataclass
class MCPCandidate:
 name:str; url:str; description:str; version:str=""; updated_at:str=""; matched_tag:str="mcp"; source:str="mcp_registry"; kind:str=KIND_MCP_SERVER; flags:list[str]=field(default_factory=list); evidence:list[str]=field(default_factory=list); install_hint:str=""
def _err(tag,msg): return MCPCandidate("(MCP Registry error)","",msg,matched_tag=tag,flags=["source-error"])
def search_mcp_registry(query:str,tag:str,size:int=8):
 try:r=requests.get(API_URL,params={"search":query,"version":"latest","limit":size},headers={"Accept":"application/json","User-Agent":"agentfit"},timeout=TIMEOUT)
 except requests.RequestException as e:return [_err(tag,f"MCP Registry search failed: {e}")]
 if r.status_code!=200:return [_err(tag,f"MCP Registry returned HTTP {r.status_code}")]
 try:data=r.json()
 except (ValueError,TypeError):return [_err(tag,"MCP Registry returned malformed JSON")]
 if not isinstance(data,dict) or "servers" not in data or not isinstance(data.get("servers"),list):return [_err(tag,"MCP Registry returned an unexpected response shape")]
 out=[]
 for entry in data.get("servers",[]):
  if not isinstance(entry,dict):continue
  s=entry.get("server") if isinstance(entry.get("server"),dict) else entry; name=s.get("name") if isinstance(s.get("name"),str) else ""
  if not name:continue
  desc=s.get("description") if isinstance(s.get("description"),str) else ""; ver=s.get("version") if isinstance(s.get("version"),str) else ""; status=s.get("status") if isinstance(s.get("status"),str) else "active"
  repo=s.get("repository") if isinstance(s.get("repository"),dict) else {}; url=repo.get("url") if isinstance(repo.get("url"),str) else "https://registry.modelcontextprotocol.io/servers/"+name
  meta=entry.get("_meta") if isinstance(entry.get("_meta"),dict) else {}; updated=meta.get("updatedAt") or meta.get("updated_at") or ""; flags=[]
  if status=="deprecated":flags.append("deprecated")
  if status=="deleted":flags.append("deleted")
  packages=s.get("packages") if isinstance(s.get("packages"),list) else []; install=""
  for pkg in packages:
   if not isinstance(pkg,dict):continue
   ident=pkg.get("identifier") if isinstance(pkg.get("identifier"),str) else ""; typ=str(pkg.get("registryType") or pkg.get("registry_type") or "").lower()
   if ident and typ=="npm": install=f"npm:{ident}"; break
   if ident and typ in ("pypi","python"): install=f"pypi:{ident}"; break
  out.append(MCPCandidate(name,url,desc,ver,str(updated),tag,flags=flags,evidence=["Listed in the official MCP Registry",f"Registry lifecycle status: {status}"],install_hint=install))
 if data.get("servers") and not out:return [_err(tag,"MCP Registry response contained no valid server records")]
 return out
