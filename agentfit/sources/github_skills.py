from __future__ import annotations
import os,requests
from dataclasses import dataclass,field
from agentfit.taxonomy import KIND_AGENT_SKILL
API='https://api.github.com/search/code'; TIMEOUT=12
@dataclass
class SkillCandidate:
 name:str; url:str; description:str='Agent Skill (SKILL.md)'; matched_tag:str='agent-skill'; source:str='github_skill'; kind:str=KIND_AGENT_SKILL; flags:list[str]=field(default_factory=list); evidence:list[str]=field(default_factory=list)
def _err(tag,msg):return SkillCandidate('(GitHub skill search error)','',msg,tag,flags=['source-error'])
def search_github_skills(query:str,tag:str,size:int=8):
 token=os.getenv('GITHUB_TOKEN')
 if not token:return []
 try:r=requests.get(API,params={'q':f'{query} filename:SKILL.md','per_page':size},headers={'Accept':'application/vnd.github+json','Authorization':f'Bearer {token}','User-Agent':'agentfit'},timeout=TIMEOUT)
 except requests.RequestException as e:return [_err(tag,f'GitHub Skill search failed: {e}')]
 if r.status_code!=200:return [_err(tag,f'GitHub Skill search returned HTTP {r.status_code}')]
 try:data=r.json()
 except (ValueError,TypeError):return [_err(tag,'GitHub Skill search returned malformed JSON')]
 if not isinstance(data,dict) or not isinstance(data.get('items',[]),list):return [_err(tag,'GitHub Skill search returned an unexpected response shape')]
 out=[]
 for x in data.get('items',[]):
  if not isinstance(x,dict):continue
  repo=x.get('repository') if isinstance(x.get('repository'),dict) else {}; full=repo.get('full_name'); html=x.get('html_url')
  if not isinstance(full,str) or not isinstance(html,str):continue
  path=x.get('path') if isinstance(x.get('path'),str) else 'SKILL.md'; out.append(SkillCandidate(f'{full}:{path}',html,matched_tag=tag,evidence=['GitHub code search found a SKILL.md file']))
 return out
