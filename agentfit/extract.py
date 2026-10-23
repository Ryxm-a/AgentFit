from __future__ import annotations
import re
from agentfit.models import Requirement, TaskAnalysis
from agentfit.taxonomy import CAPABILITY_LEXICON, LABELS, STRONG_TAGS
STOP={"a","an","the","i","want","to","for","of","on","in","with","and","or","my","this","that","is","are","be","it","do","does","help","me","please","can","you","using","use","about","into","from","some","any","need","would","like","find","best","build","create","make"}
WORD=re.compile(r"[a-zA-Z][a-zA-Z0-9+#.\-]{2,}")

def analyze_task(task:str, limit:int=10)->TaskAnalysis:
    low=task.lower(); hits={}
    for phrase in sorted(CAPABILITY_LEXICON,key=len,reverse=True):
        if phrase in low:
            for tag in CAPABILITY_LEXICON[phrase]: hits[tag]=max(hits.get(tag,0),.95 if tag in STRONG_TAGS else .8)
    reqs=[Requirement(t,LABELS.get(t,t),c,[t.replace("-"," ")]) for t,c in hits.items()]
    if not reqs:
        words=[]
        for w in WORD.findall(low):
            if w not in STOP and w not in words: words.append(w)
        if words:
            phrase=" ".join(words[:5]); reqs=[Requirement("general:"+"-".join(words[:5]),phrase.title(),.45,[phrase],"freeform")]
    for r in reqs:
        context=[]
        if "mcp" in low and r.tag!="mcp": context.append("mcp")
        if "skill" in low and r.tag!="agent-skill": context.append("agent skill")
        r.search_terms=list(dict.fromkeys(r.search_terms + [f"{x} {r.search_terms[0]}" for x in context]))
    clients=[x for x in ("claude code","codex","cursor","opencode","vscode") if x in low]
    platforms=[x for x in ("windows","linux","macos","ios","android") if x in low]
    ecosystems=[x for x in ("mcp","skill","plugin","npm","pypi","github") if x in low]
    return TaskAnalysis(task, sorted(reqs,key=lambda r:-r.confidence)[:limit], ecosystems, platforms, clients)

def extract_capabilities(task:str,limit:int=6):
    from types import SimpleNamespace
    return [SimpleNamespace(tag=r.tag,confidence=r.confidence,search_terms=r.search_terms) for r in analyze_task(task,limit).requirements]
