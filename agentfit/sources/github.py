from __future__ import annotations
import os
from dataclasses import dataclass, field
import requests
from agentfit.taxonomy import classify_kind
API_URL="https://api.github.com/search/repositories"; TIMEOUT=12
@dataclass
class Candidate:
 name:str; url:str; description:str; stars:int; forks:int; open_issues:int; pushed_at:str; archived:bool
 topics:list[str]=field(default_factory=list); kind:str="unknown"; source:str="github"; matched_tag:str=""; score:float=0.; flags:list[str]=field(default_factory=list)
def _headers():
 h={"Accept":"application/vnd.github+json","User-Agent":"agentfit"}; t=os.getenv("GITHUB_TOKEN")
 if t:h["Authorization"]=f"Bearer {t}"
 return h
def _err(tag,msg): return Candidate("(github search error)","",msg,0,0,0,"",False,matched_tag=tag,score=-1,flags=["source-error"])
def search_github(query:str,tag:str,extra_qualifiers:list[str]|None=None,per_page:int=8):
 q=query+(" "+" ".join(extra_qualifiers) if extra_qualifiers else "")
 try:r=requests.get(API_URL,params={"q":q,"sort":"stars","order":"desc","per_page":per_page},headers=_headers(),timeout=TIMEOUT)
 except requests.RequestException as e:return [_err(tag,f"GitHub search failed: {e}")]
 if r.status_code==403:return [_err(tag,"GitHub rate limit hit — set GITHUB_TOKEN to raise it.")]
 if r.status_code!=200:return [_err(tag,f"GitHub search returned HTTP {r.status_code}")]
 try:data=r.json()
 except (ValueError,TypeError):return [_err(tag,"GitHub returned malformed JSON")]
 if not isinstance(data,dict) or not isinstance(data.get("items",[]),list):return [_err(tag,"GitHub returned an unexpected response shape")]
 out=[]
 for item in data.get("items",[]):
  if not isinstance(item,dict):continue
  name=item.get("full_name"); url=item.get("html_url")
  if not isinstance(name,str) or not name or not isinstance(url,str) or not url:continue
  topics=item.get("topics") if isinstance(item.get("topics"),list) else []; desc=item.get("description") if isinstance(item.get("description"),str) else ""
  def num(k):
   v=item.get(k,0); return v if isinstance(v,int) and not isinstance(v,bool) else 0
  out.append(Candidate(name,url,desc,num("stargazers_count"),num("forks_count"),num("open_issues_count"),item.get("pushed_at") if isinstance(item.get("pushed_at"),str) else "",bool(item.get("archived",False)),[str(x) for x in topics],classify_kind(name,desc,topics),matched_tag=tag))
 return out
_error_candidate = _err
