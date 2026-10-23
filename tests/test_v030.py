import pytest
from unittest.mock import patch
from agentfit.extract import analyze_task
from agentfit.sources.mcp_registry import search_mcp_registry
from agentfit.models import UniversalCandidate
from agentfit.installer import install_command
from agentfit.engine import score
CASES=[
("GitHub MCP for issues and pull requests",{"github","mcp","issue-tracking","code-review"}),("PowerPoint presentation skill",{"presentation","agent-skill"}),("OCR a PDF",{"ocr","pdf"}),("React Native Supabase Stripe",{"react-native","supabase","stripe"}),("reverse engineer wasm in Ghidra",{"ghidra","webassembly","reverse-engineering"}),("security audit WordPress vulnerabilities",{"wordpress","security","vulnerability-scanning"}),("Playwright browser automation testing",{"browser-automation","testing"}),("iOS Xcode Metal C++",{"ios","xcode","metal","cpp"}),("Android app",{"android","mobile-development"}),("Postgres database",{"postgres","database"}),("Docker Kubernetes",{"containers","orchestration"}),("Terraform AWS",{"infrastructure-as-code","cloud-aws"}),("Slack plugin",{"messaging-slack","plugin"}),("Gmail calendar",{"email-gmail","calendar"}),("Python CLI",{"python","cli"})]
@pytest.mark.parametrize("task,expected",CASES)
def test_routing_matrix(task,expected):assert expected<={x.tag for x in analyze_task(task).requirements}
class Resp:
 def __init__(self,data,status=200):self.data=data;self.status_code=status
 def json(self):return self.data
@pytest.mark.parametrize("payload",[None,[],{},{"servers":None},{"servers":[None,1,"x",{}]}])
def test_mcp_malformed_shapes(payload):
 with patch("agentfit.sources.mcp_registry.requests.get",return_value=Resp(payload)):
  r=search_mcp_registry("x","mcp");assert isinstance(r,list) and r
def test_mcp_valid_and_install():
 payload={"servers":[{"server":{"name":"io.github.x/tool","description":"GitHub helper","version":"1.2.3","status":"active","repository":{"url":"https://github.com/x/tool"},"packages":[{"registryType":"npm","identifier":"@x/tool"}]},"_meta":{"updatedAt":"2026-10-20T00:00:00Z"}}]}
 with patch("agentfit.sources.mcp_registry.requests.get",return_value=Resp(payload)):
  x=search_mcp_registry("tool","mcp")[0];assert x.install_hint=="npm:@x/tool";assert "official MCP Registry" in x.evidence[0];c=UniversalCandidate(x.name,x.url,x.description,x.source,x.kind,install_hint=x.install_hint);assert install_command(c)=="npm install -g @x/tool"
def test_mcp_deleted_flag():
 with patch("agentfit.sources.mcp_registry.requests.get",return_value=Resp({"servers":[{"server":{"name":"x/y","status":"deleted"}}]})):assert "deleted" in search_mcp_registry("x","mcp")[0].flags
@pytest.mark.parametrize("bad",["x; touch /tmp/pwn","x && whoami","x$(id)","x`id`","x name","x'quote"])
def test_mcp_install_shell_quotes(bad):
 c=UniversalCandidate("x","","","mcp_registry","mcp_server",install_hint="npm:"+bad);cmd=install_command(c);assert cmd.startswith("npm install -g ");assert cmd!="npm install -g "+bad or bad.isalnum()
@pytest.mark.parametrize("source,kind",[("mcp_registry","mcp_server"),("github","cli_tool"),("npm","library")])
def test_scores_are_bounded(source,kind):
 c=UniversalCandidate("tool","https://example.invalid","useful tool",source,kind,matched_tags=["security"]);req=analyze_task("security audit vulnerabilities").requirements;score(c,req);assert 0<=c.score<=100;assert all(0<=v<=30 for v in c.components.values())
MORE=[("wasm","webassembly"),("ghidra","ghidra"),("decompile","reverse-engineering"),("malware","malware-analysis"),("ctf","binary-analysis"),("wordpress","wordpress"),("vulnerability","vulnerability-scanning"),("semgrep","static-analysis"),("codeql","static-analysis"),("scraping","web-scraping"),("github","github"),("issues","issue-tracking"),("pull requests","code-review"),("mcp","mcp"),("skill","agent-skill"),("plugin","plugin"),("powerpoint","presentation"),("pdf","pdf"),("excel","spreadsheet"),("database","database"),("sqlite","sqlite"),("stripe","stripe"),("react native","react-native"),("ios","ios"),("xcode","xcode"),("metal","metal"),("c++","cpp"),("android","android"),("docker","containers"),("kubernetes","orchestration"),("terraform","infrastructure-as-code"),("aws","cloud-aws"),("slack","messaging-slack"),("notion","productivity-notion"),("jira","project-management-jira"),("google drive","storage-gdrive"),("gmail","email-gmail"),("calendar","calendar"),("python","python"),("typescript","typescript"),("javascript","javascript"),("rust","rust"),("command line","cli")]
@pytest.mark.parametrize("phrase,tag",MORE)
def test_lexicon_routes(phrase,tag):assert tag in {x.tag for x in analyze_task("I need "+phrase).requirements}
