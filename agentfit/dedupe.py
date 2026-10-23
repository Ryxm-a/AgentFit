from __future__ import annotations
from dataclasses import dataclass
from typing import Union
from urllib.parse import urlsplit, urlunsplit
from agentfit.sources.github import Candidate
from agentfit.sources.npm import NpmCandidate
AnyCandidate = Union[Candidate, NpmCandidate]
def _identity_keys(candidate):
    keys={f"name:{candidate.source}:{candidate.name.strip().lower()}"}; raw_url=getattr(candidate,"url","").strip()
    if raw_url:
        parts=urlsplit(raw_url); path=parts.path.rstrip("/")
        if path.endswith(".git"):path=path[:-4]
        keys.add(f"url:{urlunsplit((parts.scheme.lower(),parts.netloc.lower(),path.lower(),'',''))}")
    return keys
@dataclass
class Ranked:
    candidate:AnyCandidate; tag:str; recommended:bool; reason:str=""
def rank_and_dedupe(candidates,per_tag=1):
    by_tag={}
    for c in candidates:
        if getattr(c,"score",0)<0:continue
        by_tag.setdefault(c.matched_tag,[]).append(c)
    ranked=[]
    for tag,items in by_tag.items():
        items.sort(key=lambda c:c.score,reverse=True);seen=set();deduped=[]
        for c in items:
            keys=_identity_keys(c)
            if keys&seen:continue
            seen.update(keys);deduped.append(c)
        for i,c in enumerate(deduped):
            if i<per_tag:ranked.append(Ranked(c,tag,True))
            else:
                reasons=[]
                if "possibly abandoned (no push in 2+ years)" in getattr(c,"flags",[]):reasons.append("abandoned")
                if "archived by owner" in getattr(c,"flags",[]):reasons.append("archived")
                if not reasons:reasons.append(f"overlaps {deduped[0].name}")
                ranked.append(Ranked(c,tag,False,"; ".join(reasons)))
    return ranked
