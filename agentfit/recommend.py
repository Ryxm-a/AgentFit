from __future__ import annotations
from agentfit.extract import analyze_task
from agentfit.models import Report,UniversalCandidate
from agentfit.taxonomy import GITHUB_TOPIC_HINTS
from agentfit.sources.github import search_github
from agentfit.sources.npm import search_npm
from agentfit.sources.mcp_registry import search_mcp_registry
from agentfit.sources.github_skills import search_github_skills
from agentfit.engine import score,select
from agentfit.compat import compatibility
from agentfit.environment import detect_environment

def _gh(x):
 flags=[]
 if x.archived:flags.append("archived")
 return UniversalCandidate(x.name,x.url,x.description,"github",x.kind,updated_at=x.pushed_at,stars=x.stars,topics=x.topics,matched_tags=[x.matched_tag],evidence=[f"GitHub search matched {x.matched_tag}",f"{x.stars} GitHub stars"],flags=flags)
def _skill(x):return UniversalCandidate(x.name,x.url,x.description,"github_skill",x.kind,matched_tags=[x.matched_tag],evidence=x.evidence,flags=x.flags)
def _mcp(x):return UniversalCandidate(x.name,x.url,x.description,"mcp_registry",x.kind,x.version,x.updated_at,matched_tags=[x.matched_tag],install_hint=x.install_hint,evidence=x.evidence,flags=x.flags)
def _npm(x):return UniversalCandidate(x.name,x.url,x.description,"npm",x.kind,x.version,x.date,quality=x.quality,maintenance=x.maintenance,popularity=x.popularity,matched_tags=[x.matched_tag],evidence=[f"npm search matched {x.matched_tag}"])
def build_report(task:str,per_tag:int=1,use_npm:bool=True,max_stack:int=8)->Report:
 analysis=analyze_task(task); errors=[]; candidates=[]; sources=[]
 if not analysis.requirements:return Report(task,analysis,[],["Could not extract useful requirements from the task."],[])
 if "mcp" in analysis.ecosystem_hints or any(r.tag=="mcp" for r in analysis.requirements):
  mcp_reqs=[r for r in analysis.requirements if r.tag!="mcp"] or [r for r in analysis.requirements if r.tag=="mcp"]
  for mr in mcp_reqs[:3]:
   for x in search_mcp_registry(mr.search_terms[0],mr.tag):
    if "source-error" in x.flags: errors.append(x.description)
    elif "deleted" not in x.flags: candidates.append(_mcp(x)); sources.append("mcp_registry")
 if "skill" in analysis.ecosystem_hints or any(r.tag=="agent-skill" for r in analysis.requirements):
  skill_reqs=[r for r in analysis.requirements if r.tag!="agent-skill"] or [r for r in analysis.requirements if r.tag=="agent-skill"]
  for sr in skill_reqs[:3]:
   for x in search_github_skills(sr.search_terms[0],sr.tag):
    if "source-error" in x.flags: errors.append(x.description)
    else: candidates.append(_skill(x)); sources.append("github_skill")
 for req in analysis.requirements:
  for term in req.search_terms[:2]:
   quals=GITHUB_TOPIC_HINTS.get(req.tag); gh=search_github(term,req.tag,quals); good=[x for x in gh if "source-error" not in x.flags]
   if quals and not good: gh=search_github(term,req.tag,None)
   for x in gh:
    if "source-error" in x.flags: errors.append(x.description)
    else:candidates.append(_gh(x)); sources.append("github")
   if use_npm:
    for x in search_npm(term,req.tag):
     if "source-error" in x.flags:errors.append(x.description)
     else:candidates.append(_npm(x));sources.append("npm")
 merged={}
 from agentfit.engine import identity
 for c in candidates:
  key=sorted(identity(c))[0]
  if key in merged:
   m=merged[key];m.matched_tags=list(dict.fromkeys(m.matched_tags+c.matched_tags));m.evidence=list(dict.fromkeys(m.evidence+c.evidence))
  else:merged[key]=c
 candidates=list(merged.values())
 for c in candidates:c.compatibility=compatibility(c.kind);score(c,analysis.requirements)
 recs=select(candidates,analysis.requirements,max_stack)
 return Report(task,analysis,recs,list(dict.fromkeys(errors)),sorted(set(sources)),detect_environment())
