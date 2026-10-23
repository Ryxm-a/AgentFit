from __future__ import annotations
import math
from datetime import datetime,timezone
STALE_DAYS=365*2
def _days_since(iso_date):
    if not iso_date:return None
    try:dt=datetime.fromisoformat(iso_date.replace("Z","+00:00"))
    except ValueError:return None
    return (datetime.now(timezone.utc)-dt).days
def _looks_like_inflated_stars(c):
    if c.stars<10000:return False
    return c.forks/max(c.stars,1)<.003 and c.open_issues==0
def score_github(c):
    if "source-error" in c.flags:return -1.
    if _looks_like_inflated_stars(c):c.flags.append("stars disproportionate to forks/issues — possible star-farming, verify manually")
    popularity=math.log10(c.stars+1)*22;age=_days_since(c.pushed_at);recency=0.
    if age is not None:
        if age<=30:recency=20
        elif age<=180:recency=14
        elif age<=365:recency=8
        elif age<=STALE_DAYS:recency=3
        else:c.flags.append("possibly abandoned (no push in 2+ years)")
    if c.archived:c.flags.append("archived by owner")
    penalty=0.
    if c.stars>0 and c.open_issues/max(c.stars,1)>.5:penalty=5;c.flags.append("high open-issue ratio relative to stars")
    total=popularity+recency-penalty
    if c.archived:total*=.25
    if any("star-farming" in x for x in c.flags):total*=.15
    return round(max(total,0.),1)
def score_npm(c):
    if "source-error" in c.flags:return -1.
    age=_days_since(c.date)
    if age is not None and age>STALE_DAYS:c.flags.append("possibly abandoned (no publish in 2+ years)")
    return round(c.score*80,1)
