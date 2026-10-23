from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import subprocess,textwrap
W,H=1280,720; OUT=Path("media"); OUT.mkdir(exist_ok=True)
REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"; BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; MONO="/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BG=(9,14,28); WHITE=(242,246,255); MUT=(157,170,202); BLUE=(62,170,255); PUR=(144,92,255); GREEN=(76,222,155); RED=(255,104,120)
def f(n,b=False,m=False): return ImageFont.truetype(MONO if m else BOLD if b else REG,n)
def base():
 im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
 for y in range(H): d.line((0,y,W,y),fill=(9,14+int(6*y/H),28+int(15*y/H)))
 return im,d
def rr(d,b,fill=(16,25,45),outline=(47,65,99)): d.rounded_rectangle(b,18,fill=fill,outline=outline,width=2)
def title(d,a,b=""): d.text((70,55),a,font=f(46,1),fill=WHITE); d.text((72,115),b,font=f(22),fill=MUT)
def term(d,lines,y=190,h=400):
 rr(d,(70,y,W-70,y+h)); d.rectangle((70,y,W-70,y+48),fill=(18,27,46))
 for i,c in enumerate(((255,95,86),(255,189,46),(39,201,63))): d.ellipse((92+i*28,y+16,108+i*28,y+32),fill=c)
 yy=y+70
 for t,c in lines:
  for line in textwrap.wrap(t,88) or [""]: d.text((100,yy),line,font=f(21,m=1),fill=c); yy+=34
def scene(name,seconds,draw,narr):
 im,d=base(); draw(d); p=OUT/(name+".png"); im.save(p); scenes.append((p,seconds,narr))
scenes=[]
scene("01-hook",7,lambda d:(d.text((70,130),"Too many AI tools.",font=f(64,1),fill=WHITE),d.text((70,220),"Which ones actually fit the job?",font=f(45,1),fill=BLUE),d.text((70,345),"MCP servers  •  Agent Skills  •  CLIs  •  libraries",font=f(25),fill=MUT),d.text((70,510),"AgentFit turns the job into the stack.",font=f(34,1),fill=GREEN)),"AI tooling is exploding. Finding a tool is easy. Finding the smallest useful stack for a specific job is not.")
scene("02-brand",7,lambda d:(d.text((640,175),"AgentFit",font=f(86,1),fill=WHITE,anchor="mm"),d.text((640,280),"Tell it the job. Get the right stack.",font=f(34,1),fill=BLUE,anchor="mm"),d.text((640,390),"DISCOVER  →  RANK  →  DEDUPE  →  EXPLAIN",font=f(25,m=1),fill=PUR,anchor="mm"),d.text((640,510),"Open source • Python • review-first installs",font=f(23),fill=MUT,anchor="mm")),"AgentFit is an open source recommendation engine for MCPs, agent skills, command line tools and libraries.")
scene("03-setup",10,lambda d:(title(d,"Setup takes three commands","Clone it, install it, ask for a job."),term(d,[("$ git clone https://github.com/Ryxm-a/AgentFit.git",WHITE),("$ cd AgentFit",WHITE),("$ python -m pip install .",GREEN),("",WHITE),("$ agentfit --help",BLUE)])),"Setup is straightforward. Clone the repository, install the Python package, and the AgentFit command is ready. There is no catalog to learn before you can ask a question.")
scene("04-task",10,lambda d:(title(d,"Describe the job in normal language","AgentFit extracts requirements instead of expecting package names."),term(d,[('$ agentfit "reverse engineer WebAssembly in Ghidra"',GREEN),("",WHITE),("Requirements graph",BLUE),("  • reverse engineering",WHITE),("  • WebAssembly",WHITE),("  • Ghidra",WHITE),("  • binary analysis",WHITE)])),"Instead of searching by package name, describe what you actually need. AgentFit converts the request into a requirements graph, preserving the important technologies and capabilities.")
def sources(d):
 title(d,"Search live ecosystems","Multiple sources feed one normalized candidate model.")
 for x,l in zip((105,385,665,945),("Official MCP\nRegistry","GitHub\nrepositories","SKILL.md\ndiscovery","npm")): rr(d,(x,235,x+220,350)); d.multiline_text((x+110,292),l,font=f(22,1),fill=WHITE,anchor="mm",align="center")
 d.text((640,430),"↓",font=f(55,1),fill=BLUE,anchor="mm"); rr(d,(330,500,950,610),fill=(25,25,60),outline=(105,91,210)); d.text((640,535),"NORMALIZE  •  SCORE  •  DEDUPLICATE",font=f(24,1,m=1),fill=WHITE,anchor="mm"); d.text((640,575),"source failures are isolated instead of crashing the whole run",font=f(19),fill=MUT,anchor="mm")
scene("05-sources",10,sources,"AgentFit searches live ecosystems, including the official MCP Registry, GitHub repositories, authenticated Skill files, and npm. Results are normalized, scored, and deduplicated. One broken source does not have to destroy the entire recommendation run.")
def score(d):
 title(d,"Ranking is more than popularity","The selector prefers complementary coverage, not five copies of the same capability.")
 y=190
 for lab,val in (("Task fit",30),("Requirement coverage",15),("Maintenance",13),("Adoption",10),("Trust",12),("Documentation",8),("Install confidence",7),("Context efficiency",5)):
  d.text((105,y),lab,font=f(21),fill=WHITE); d.rounded_rectangle((390,y+3,390+val*17,y+25),10,fill=BLUE if val>10 else PUR); d.text((940,y),str(val),font=f(19,m=1),fill=MUT); y+=55
scene("06-score",10,score,"Candidates are not simply sorted by stars. AgentFit combines task fit, requirement coverage, maintenance, adoption, trust, documentation, installation confidence, and context efficiency, then favors tools that add complementary capability.")
def results(d):
 title(d,"The output explains the recommendation","Evidence and uncertainty stay visible."); rr(d,(70,180,1210,600)); d.text((105,215),"RECOMMENDED STACK",font=f(24,1,m=1),fill=GREEN)
 y=275
 for n,a,b in (("1","Best-fit candidate","covers: WebAssembly • reverse engineering"),("2","Complementary candidate","adds: Ghidra integration"),("3","Optional candidate","adds workflow capability without duplicate coverage")):
  d.rounded_rectangle((105,y,160,y+48),12,fill=(30,53,80)); d.text((132,y+24),n,font=f(22,1),fill=WHITE,anchor="mm"); d.text((190,y),a,font=f(23,1),fill=WHITE); d.text((190,y+30),b,font=f(18),fill=MUT); y+=90
 d.text((105,555),"Scores are live-data dependent; evidence matters more than a permanent winner.",font=f(18),fill=MUT)
scene("07-results",10,results,"The final stack is compact and explainable. AgentFit shows why each recommendation was selected, what it covers, compatibility inference, and source evidence. Because the ecosystem changes, the project does not pretend yesterday's winner is permanent.")
scene("08-safe",9,lambda d:(title(d,"Installation stays review-first","AgentFit generates commands. It does not silently execute third-party code."),term(d,[('$ agentfit "browser automation for an AI coding agent" -y',GREEN),("",WHITE),("Wrote: agentfit_install.sh",BLUE),("# Review this file before running it.",RED),("",WHITE),("$ cat agentfit_install.sh",WHITE),("set -euo pipefail",MUT),("# generated, safely quoted install commands",MUT)])),"When you ask for an install plan, AgentFit writes a reviewable shell script with safely quoted commands. It deliberately does not silently execute third party code. You stay in control.")
def uses(d):
 title(d,"One interface, many jobs","Use the same workflow across very different domains.")
 for i,(a,b) in enumerate((("SECURITY","audit a WordPress plugin"),("DEV TOOLS","GitHub issues and pull requests"),("DOCUMENTS","OCR scanned PDFs"),("MOBILE","C++ game to iOS"),("DEVOPS","debug Kubernetes"),("AGENTS","browser automation"))):
  x=70+(i%3)*390;y=180+(i//3)*190;rr(d,(x,y,x+350,y+145));d.text((x+25,y+25),a,font=f(18,1,m=1),fill=PUR);d.text((x+25,y+67),b,font=f(22,1),fill=WHITE)
scene("09-uses",9,uses,"The same interface works across security research, developer tooling, document workflows, mobile development, DevOps, and agent automation. The task is the input; the ecosystem is the search space.")
scene("10-end",8,lambda d:(d.text((640,160),"AgentFit",font=f(82,1),fill=WHITE,anchor="mm"),d.text((640,275),"Stop collecting tools.",font=f(42,1),fill=WHITE,anchor="mm"),d.text((640,330),"Build the right stack.",font=f(42,1),fill=GREEN,anchor="mm"),rr(d,(255,420,1025,505)),d.text((640,462),"github.com/Ryxm-a/AgentFit",font=f(29,1,m=1),fill=WHITE,anchor="mm"),d.text((640,570),"MIT licensed  •  contributions welcome",font=f(21),fill=MUT,anchor="mm")),"AgentFit is open source and MIT licensed. Try it on a real task, break the recommendations, and help make AI tool discovery measurable. Stop collecting tools. Build the right stack.")
voice=" ".join(x[2] for x in scenes)
subprocess.run(["espeak","-s","158","-v","en-us","-w",str(OUT/"voice.wav"),voice],check=True)
with (OUT/"concat.txt").open("w") as h:
 for p,d,_ in scenes: h.write(f"file '{p.resolve()}'\nduration {d}\n")
 h.write(f"file '{scenes[-1][0].resolve()}'\n")
subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(OUT/"concat.txt"),"-i",str(OUT/"voice.wav"),"-vf","fps=24,format=yuv420p","-c:v","libx264","-crf","20","-c:a","aac","-b:a","96k","-shortest","-movflags","+faststart",str(OUT/"agentfit-demo.mp4")],check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(OUT/"agentfit-demo.mp4"),"-t","24","-vf","fps=8,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer","-loop","0",str(OUT/"agentfit-preview.gif")],check=True)
Image.open(scenes[1][0]).save(OUT/"agentfit-thumbnail.png")
