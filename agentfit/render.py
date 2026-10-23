from __future__ import annotations
from agentfit.models import Report

def render_report(report:Report,color:bool=True)->str:
 a=report.analysis; out=[f'Analyzing: "{report.task}"',""]
 out.append("Requirements graph:")
 for r in a.requirements:out.append(f"  • {r.label}  ({int(r.confidence*100)}% extraction confidence)")
 if a.client_hints:out.append("  Client hints: "+", ".join(a.client_hints))
 if a.platform_hints:out.append("  Platform hints: "+", ".join(a.platform_hints))
 out += ["","Recommended stack:"]
 chosen=[r for r in report.recommendations if r.recommended]
 if not chosen:out.append("  (no sufficiently strong matches)")
 for i,r in enumerate(chosen,1):
  c=r.candidate;out.append(f"  {i}. {c.name} — {c.score:.1f}/100  [{c.source}/{c.kind}]")
  if c.description:out.append("     "+c.description[:180])
  out.append("     covers: "+(", ".join(r.covers) or "best available match"));out.append("     why: "+r.reason);out.append("     "+c.url)
  comp=c.components;out.append("     score: "+" | ".join(f"{k} {v:g}" for k,v in comp.items()))
  for f in c.flags:out.append("     ⚠ "+f)
 skipped=[r for r in report.recommendations if not r.recommended][:8]
 if skipped:
  out += ["","Not selected:"]
  for r in skipped:out.append(f"  - {r.candidate.name}: {r.reason}")
 if report.errors:out += ["","Source warnings:"]+["  ⚠ "+x for x in report.errors]
 out += ["","Evidence policy: compatibility marked '?' is inferred, not verified. Review linked documentation before installing or granting permissions."]
 return "\n".join(out)
def print_report(report:Report,color:bool=True):print(render_report(report,color))
