from __future__ import annotations
import json
from pathlib import Path
from dataclasses import asdict
from agentfit.recommend import build_report

ROOT=Path(__file__).parent
tasks=json.loads((ROOT/"tasks.json").read_text(encoding="utf-8"))
outdir=ROOT/"results";outdir.mkdir(exist_ok=True)
outfile=outdir/"latest.jsonl"
with outfile.open("w",encoding="utf-8") as f:
    for item in tasks:
        report=build_report(item["task"])
        row={"id":item["id"],"domain":item["domain"],"report":asdict(report)}
        f.write(json.dumps(row)+"\n")
        print(f'{item["id"]}: {sum(x.recommended for x in report.recommendations)} selected')
print(f"Wrote {outfile}")
