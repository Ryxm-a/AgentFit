<div align="center">

# AgentFit

### Tell it the job. Get the smallest useful AI tool stack.

**AgentFit turns a natural-language task into a requirements graph, searches real AI-tool ecosystems, ranks candidates with evidence, removes overlap, and recommends a compact stack you can actually review and install.**

[![CI](https://github.com/Ryxm-a/AgentFit/actions/workflows/ci.yml/badge.svg)](https://github.com/Ryxm-a/AgentFit/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-6f42c1)](pyproject.toml)

</div>

---

## The problem

The AI-agent ecosystem is exploding: MCP servers, agent skills, plugins, CLIs, libraries and overlapping integrations. Finding *a* tool is easy. Figuring out **which combination fits your exact task without installing five redundant tools** is not.

AgentFit is the recommendation layer between your goal and that ecosystem.

```text
Your task
   │
   ▼
Requirements graph
   │
   ├── Official MCP Registry
   ├── GitHub repositories
   ├── GitHub SKILL.md discovery
   └── npm
   │
   ▼
Normalize → score → deduplicate → optimize coverage
   │
   ▼
Smallest useful stack + evidence + compatibility + install plan
```

## Quick start

```bash
git clone https://github.com/Ryxm-a/AgentFit.git
cd AgentFit
python -m pip install .
```

Then ask for the job, not a package name:

```bash
agentfit "I need an MCP for GitHub issues and pull requests"
agentfit "reverse engineer WebAssembly in Ghidra"
agentfit "audit a WordPress plugin for vulnerabilities"
agentfit "create PowerPoint presentations with an agent skill"
agentfit "build a React Native app with Supabase and Stripe"
```

For higher GitHub API limits and authenticated `SKILL.md` discovery:

```bash
export GITHUB_TOKEN=your_token
```

PowerShell:

```powershell
$env:GITHUB_TOKEN="your_token"
```

## Why AgentFit is different

AgentFit does not simply sort search results by stars. It evaluates candidates across the dimensions that matter to an agent workflow:

| Signal | What AgentFit asks |
|---|---|
| **Task fit** | Does this actually solve the requested job? |
| **Requirement coverage** | How much of the requirements graph does it cover? |
| **Maintenance** | Is the project active or abandoned? |
| **Adoption** | Is there meaningful usage/community signal? |
| **Trust** | What provenance and risk signals are available? |
| **Documentation** | Can a user realistically understand and deploy it? |
| **Install confidence** | Is there a credible installation path? |
| **Context efficiency** | Does it add useful capability without needless overlap? |

The selector then prefers **complementary coverage**, rather than blindly returning one winner for every keyword.

## Discovery sources

**Official MCP Registry.** MCP results come from the official registry API. AgentFit understands lifecycle state, excludes deleted entries and penalizes deprecated ones.

**GitHub.** Repository discovery contributes maintenance, adoption and project metadata. With `GITHUB_TOKEN`, AgentFit additionally searches for repositories containing `SKILL.md`.

**npm.** npm search contributes package candidates and registry quality, maintenance and popularity signals.

**PyPI — intentionally not faked.** AgentFit does not claim general PyPI search support. PyPI's old automated XML-RPC search is disabled and the supported JSON API is project-by-name. The source boundary exists without pretending a nonexistent supported full-text API exists.

## Evidence, not false certainty

AgentFit distinguishes evidence from inference. A tool is not declared compatible with a client merely because `MCP` appears in its name. Uncertain compatibility is surfaced as uncertain.

Likewise, an official registry entry is stronger provenance than an arbitrary repository, but it is **not a security guarantee**. AgentFit is a recommender, not a trust oracle.

## Safe install plans

AgentFit can generate a reviewable install script. It **does not automatically execute third-party installation commands**.

```bash
agentfit "your task" -y
cat agentfit_install.sh
```

Untrusted package and repository identifiers are shell-quoted before being written to the generated script. You should still review source code, permissions and every command before execution.

## Resilient by design

External ecosystems fail in messy ways. AgentFit is designed so malformed records, unexpected JSON, source outages and rate limits become warnings instead of taking down the entire recommendation run.

If one source is unavailable, useful results from the remaining sources can still be ranked.

## CLI

```text
usage: agentfit [-h] [--limit N] [--no-npm] [--json] [--no-color] [-y] task
```

```bash
# Human-readable recommendations
agentfit "browser automation for an AI coding agent"

# Machine-readable output
agentfit "browser automation for an AI coding agent" --json

# Limit selected recommendations
agentfit "security review a Python project" --limit 5

# Write a reviewable installation script
agentfit "security review a Python project" -y
```

`--limit` must be at least `1`; invalid values are rejected.

## Architecture

```text
agentfit/
├── cli.py               CLI and argument validation
├── engine.py            scoring + coverage optimization
├── extract.py           task → requirements graph
├── taxonomy.py          capability vocabulary
├── models.py            normalized candidate/report models
├── score.py             legacy health scoring helpers
├── dedupe.py            identity + overlap handling
├── recommend.py         multi-source orchestration
├── compat.py            compatibility inference/evidence
├── environment.py       local environment detection
├── installer.py         safe reviewable install plan
├── render.py            human/JSON presentation
└── sources/
    ├── mcp_registry.py  official MCP Registry
    ├── github.py        GitHub repositories
    ├── github_skills.py SKILL.md discovery
    ├── npm.py           npm registry
    └── pypi.py          explicit Python-search boundary
```

## Development

```bash
git clone https://github.com/Ryxm-a/AgentFit.git
cd AgentFit
python -m pip install -e ".[dev]"
python -m pytest -q
```

The 1.0.0 release ships with **109 automated cases** spanning extraction/routing, source contracts, malformed upstream responses, MCP lifecycle handling, ranking, deduplication and shell-injection regression coverage.

CI runs the suite across Python 3.9–3.13 on every push and pull request.

## Design principles

1. **Recommend less, better.** More tools are not automatically a better stack.
2. **Never manufacture certainty.** Inference and evidence are different things.
3. **Degrade gracefully.** One broken registry should not break the product.
4. **Do not invent integrations.** Unsupported APIs are called unsupported.
5. **Installation is a trust boundary.** Generate for review; do not silently execute.
6. **Keep sources replaceable.** Ecosystems change; source adapters should be swappable.

## Roadmap

AgentFit 1.0 establishes the task-to-stack engine and live discovery architecture. Future directions include additional stable registries, richer semantic ranking, ecosystem-specific install adapters, signed provenance, benchmark datasets and an interactive UI/API built on the same engine.

See [VISION_STATUS.md](VISION_STATUS.md) for the implementation boundary and engineering notes.

## Contributing

Bug reports, new source adapters, taxonomy improvements, ranking benchmarks and adversarial test cases are especially welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

For security issues, follow [SECURITY.md](SECURITY.md) rather than opening a public issue.

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

**Stop collecting tools. Build the right stack.**

</div>
