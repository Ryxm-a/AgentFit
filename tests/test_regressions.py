import json,shlex,pytest
from agentfit.cli import build_parser,main
from agentfit.installer import install_command
from agentfit.recommend import build_report
from agentfit.sources.github import Candidate,_error_candidate as github_error
from agentfit.sources.npm import NpmCandidate,_error_candidate as npm_error
from agentfit.taxonomy import KIND_MCP_SERVER
def gh(name="owner/repo",tag="security",**kw):
 b=dict(name=name,url=f"https://github.com/{name}",description="tool",stars=10,forks=2,open_issues=1,pushed_at="2099-01-01T00:00:00Z",archived=False,topics=[],kind="unknown",matched_tag=tag);b.update(kw);return Candidate(**b)
def npm(name="safe-package",tag="security"):return NpmCandidate(name=name,url=f"https://www.npmjs.com/package/{name}",description="tool",version="1.0.0",score=.8,maintenance=.8,popularity=.8,quality=.8,date="2099-01-01T00:00:00Z",matched_tag=tag)
@pytest.mark.parametrize("value",["0","-1","-999"])
def test_limit_must_be_positive(value):
 with pytest.raises(SystemExit):build_parser().parse_args(["security audit","--limit",value])
def test_source_errors_are_never_ranked(monkeypatch):
 monkeypatch.setattr("agentfit.recommend.search_github",lambda *a,**k:[github_error(a[1] if len(a)>1 else "security","boom gh")]);monkeypatch.setattr("agentfit.recommend.search_npm",lambda *a,**k:[npm_error(a[1] if len(a)>1 else "security","boom npm")]);r=build_report("security audit");assert r.ranked==[] and r.errors
def test_npm_install_command_shell_quotes_untrusted_name():
 name="pkg; touch /tmp/PWNED";cmd=install_command(npm(name));assert cmd==f"npm install -g {shlex.quote(name)}"
def test_github_install_command_shell_quotes_untrusted_url_and_mcp_name():
 c=gh(name="owner/repo;echo PWN",kind=KIND_MCP_SERVER);c.url="https://github.com/owner/repo;echo PWN";cmd=install_command(c);assert f"git clone {shlex.quote(c.url+'.git')}" in cmd and "&&" not in cmd
def test_json_cli_never_serializes_source_error_as_recommendation(monkeypatch,capsys):
 monkeypatch.setattr("agentfit.recommend.search_github",lambda *a,**k:[github_error("security","offline")]);monkeypatch.setattr("agentfit.recommend.search_npm",lambda *a,**k:[]);assert main(["security audit","--json"])==0;p=json.loads(capsys.readouterr().out);assert p["recommendations"]==[] and p["errors"]
