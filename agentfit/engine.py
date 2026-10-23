from __future__ import annotations
import math,re
from datetime import datetime,timezone
from urllib.parse import urlsplit,urlunsplit
from agentfit.models import UniversalCandidate,Recommendation
from agentfit.taxonomy import KIND_MCP_SERVER,KIND_AGENT_SKILL,KIND_CLI_TOOL,KIND_LIBRARY
TOKEN=re.compile(r"[a-z0-9+#.]+")
SYN={"mcp":{"mcp","model","context","protocol","server"},"github":{"github","git"},"browser-automation":{"browser","automation","playwright","puppeteer"},"presentation":{"presentation","powerpoint","pptx","slides"},"agent-skill":{"skill","skills","agent","skill.md"},"security":{"security","secure","audit"},"vulnerability-scanning":{"vulnerability","vulnerabilities","vuln","scanner","scanning","security"},"reverse-engineering":{"reverse","engineering","decompiler","disassembler","ghidra"},"webassembly":{"webassembly","wasm"},"ocr":{"ocr","optical","character","recognition"}}
def toks(s):return set(TOKEN.findall((s or "").lower()))
def relevance(c,reqs):
 blob=toks(c.name+" "+c.description+" "+" ".join(c.topics)); scores={}
 for r in reqs:
  target=toks(r.label+" "+" ".join(r.search_terms))|SYN.get(r.tag,set()); inter=len(blob&target); base=inter/max(len(target),1)
  if r.tag in c.matched_tags: base=max(base,.42)
  scores[r.tag]=min(1.,base*1.6)*r.confidence
 return scores
def _days(s):
 try:return (datetime.now(timezone.utc)-datetime.fromisoformat(s.replace("Z","+00:00"))).days
 except Exception:return None
def score(c,reqs):
 rel=relevance(c,reqs); task=min(30.,30*max(rel.values(),default=0)); coverage=min(15.,15*sum(1 for v in rel.values() if v>=.28)/max(1,min(3,len(reqs))))
 maint=5.; pop=3.; trust=7.; docs=5.; install=3.; overhead=4.
 if c.source=="mcp_registry":
  trust=10.; docs=7.; install=7. if c.install_hint else 4.; maint=8.; pop=5.
  if "deprecated" in c.flags: maint=2.; trust=6.
 elif c.source=="github":
  pop=min(10.,math.log10((c.stars or 0)+1)*2.2); d=_days(c.updated_at); maint=10 if d is not None and d<=90 else 7 if d is not None and d<=365 else 3 if d is not None and d<=730 else 1
  if "archived" in c.flags: maint=0; trust-=2
 elif c.source=="npm":
  pop=min(10.,(c.popularity or 0)*10); maint=min(10.,(c.maintenance or 0)*10); docs=min(5.,(c.quality or 0)*5)
 if c.kind=="unknown": trust-=1; install-=1
 if c.kind in (KIND_MCP_SERVER,KIND_AGENT_SKILL): overhead=3
 c.components={"task_fit":round(task,1),"coverage":round(coverage,1),"maintenance":round(maint,1),"adoption":round(pop,1),"trust":round(max(0,trust),1),"documentation":round(docs,1),"installation":round(install,1),"context_efficiency":round(overhead,1)}
 c.score=round(sum(c.components.values()),1); return rel
def identity(c):
 keys={f"{c.source}:{c.name.lower().strip()}"}
 if c.url:
  p=urlsplit(c.url); path=p.path.rstrip('/'); path=path[:-4] if path.endswith('.git') else path; keys.add(urlunsplit((p.scheme.lower(),p.netloc.lower(),path.lower(),'', '')))
 return keys
def select(cands,reqs,limit=8):
 uniq=[]; seen=set()
 for c in sorted(cands,key=lambda x:-x.score):
  k=identity(c)
  if k&seen:continue
  seen|=k;uniq.append(c)
 covered=set(); out=[]
 for c in uniq:
  rel=relevance(c,reqs); cv=[t for t,v in rel.items() if v>=.28]; new=[t for t in cv if t not in covered]
  recommended=bool(new) and c.score>=25 and len([x for x in out if x.recommended])<limit
  if recommended: covered.update(new); reason="adds coverage for "+", ".join(new)
  elif cv: reason="overlaps stronger selected tools for "+", ".join(cv)
  else: reason="weak task fit"
  out.append(Recommendation(c,recommended,reason,cv))
 if uniq and not any(x.recommended for x in out) and uniq[0].score>=20: out[0].recommended=True;out[0].reason="best available match; verify fit"
 return out
