from datetime import datetime,timedelta,timezone
from agentfit.score import score_github
from agentfit.sources.github import Candidate
def _candidate(**o):
 b=dict(name="example/repo",url="https://github.com/example/repo",description="desc",stars=100,forks=10,open_issues=5,pushed_at=datetime.now(timezone.utc).isoformat(),archived=False,topics=["mcp-server"],kind="mcp_server",matched_tag="security");b.update(o);return Candidate(**b)
def test_recent_popular_repo_scores_higher_than_stale_one():
 r=_candidate(stars=500);s=_candidate(stars=500,pushed_at=(datetime.now(timezone.utc)-timedelta(days=1000)).isoformat());assert score_github(r)>score_github(s);assert "possibly abandoned (no push in 2+ years)" in s.flags
def test_archived_repo_is_flagged_and_penalized():
 a=_candidate(archived=True);n=_candidate();assert score_github(a)<score_github(n);assert "archived by owner" in a.flags
def test_source_error_candidate_scores_negative():assert score_github(_candidate(flags=["source-error"]))==-1.
def test_huge_stars_with_no_forks_or_issues_is_flagged_and_penalized():
 s=_candidate(stars=300000,forks=5,open_issues=0);o=_candidate(stars=300000,forks=20000,open_issues=500);assert score_github(s)<score_github(o);assert any("star-farming" in f for f in s.flags)
