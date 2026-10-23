from __future__ import annotations
from dataclasses import dataclass,field
import requests
from agentfit.taxonomy import classify_kind
API_URL="https://registry.npmjs.org/-/v1/search"; TIMEOUT=12
@dataclass
class NpmCandidate:
 name:str; url:str; description:str; version:str; score:float; maintenance:float; popularity:float; quality:float; date:str; matched_tag:str=""; source:str="npm"; flags:list[str]=field(default_factory=list); kind:str="unknown"
def _err(tag,msg):return NpmCandidate("(npm search error)","",msg,"",-1,0,0,0,"",tag,flags=["source-error"])
def search_npm(query:str,tag:str,size:int=8):
 try:r=requests.get(API_URL,params={"text":query,"size":size},timeout=TIMEOUT)
 except requests.RequestException as e:return [_err(tag,f"npm search failed: {e}")]
 if r.status_code!=200:return [_err(tag,f"npm search returned HTTP {r.status_code}")]
 try:data=r.json()
 except (ValueError,TypeError):return [_err(tag,"npm returned malformed JSON")]
 if not isinstance(data,dict) or not isinstance(data.get("objects",[]),list):return [_err(tag,"npm returned an unexpected response shape")]
 out=[]
 for obj in data.get("objects",[]):
  if not isinstance(obj,dict):continue
  pkg=obj.get("package") if isinstance(obj.get("package"),dict) else {}; sc=obj.get("score") if isinstance(obj.get("score"),dict) else {}; det=sc.get("detail") if isinstance(sc.get("detail"),dict) else {}; name=pkg.get("name")
  if not isinstance(name,str) or not name:continue
  links=pkg.get("links") if isinstance(pkg.get("links"),dict) else {}; url=links.get("npm") if isinstance(links.get("npm"),str) else f"https://www.npmjs.com/package/{name}"
  def f(v): return float(v) if isinstance(v,(int,float)) and not isinstance(v,bool) else 0.
  desc=pkg.get("description") if isinstance(pkg.get("description"),str) else ""
  out.append(NpmCandidate(name,url,desc,str(pkg.get("version") or ""),f(sc.get("final")),f(det.get("maintenance")),f(det.get("popularity")),f(det.get("quality")),pkg.get("date") if isinstance(pkg.get("date"),str) else "",tag,kind=classify_kind(name,desc,[])))
 return out
_error_candidate = _err
