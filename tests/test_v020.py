import pytest
from agentfit.extract import analyze_task
from agentfit.taxonomy import classify_kind
from agentfit.sources.github import search_github
from agentfit.sources.npm import search_npm
class Resp:
 def __init__(self,data,status=200):self.data=data;self.status_code=status
 def json(self):return self.data
def tags(q):return {r.tag for r in analyze_task(q).requirements}
def test_understands_github_mcp():assert {"mcp","github","issue-tracking","code-review"}<=tags("find the best MCP server to access GitHub issues and pull requests")
def test_understands_powerpoint_skill():assert {"presentation","agent-skill"}<=tags("I need a skill that can create PowerPoint presentations")
def test_understands_ios_port():assert {"ios","xcode","metal","cpp","mobile-development"}<=tags("port a C++ game to iOS using Xcode and Metal")
def test_understands_supabase_stripe():assert {"react-native","supabase","stripe","payments"}<=tags("build a React Native app with Supabase and Stripe")
def test_understands_ocr():assert "ocr" in tags("OCR scanned PDFs")
def test_classify_model_context_protocol_topic():assert classify_kind("x","",["model-context-protocol"])=="mcp_server"
def test_classify_command_line_topic():assert classify_kind("x","",["command-line"])=="cli_tool"
@pytest.mark.parametrize("payload",[None,[],{"items":None},{"items":[None,{}]}])
def test_github_malformed_never_crashes(monkeypatch,payload):
 monkeypatch.setattr("agentfit.sources.github.requests.get",lambda *a,**k:Resp(payload));assert isinstance(search_github("x","x"),list)
@pytest.mark.parametrize("payload",[None,[],{"objects":None},{"objects":[None,{}]}])
def test_npm_malformed_never_crashes(monkeypatch,payload):
 monkeypatch.setattr("agentfit.sources.npm.requests.get",lambda *a,**k:Resp(payload));assert isinstance(search_npm("x","x"),list)
