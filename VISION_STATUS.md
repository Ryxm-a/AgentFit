# AgentFit 1.0 — Vision status

AgentFit 1.0 implements the complete *honest* version of the original product vision: task understanding, requirements graphs, multi-source discovery, normalized candidates, evidence, fit/coverage/health/trust scoring, deduplication, conflict-aware stack selection, compatibility labels, environment detection, and reviewable safe install plans.

## First-class discovery
- Official MCP Registry v0.1 API.
- GitHub repository discovery.
- npm registry discovery.
- GitHub `SKILL.md` code discovery when `GITHUB_TOKEN` is available.

## Enrichment / boundaries
- PyPI is not presented as a search source because PyPI's supported APIs do not provide general full-text project search.
- Third-party skill directories are not treated as canonical registries.
- Compatibility marked `?` is inference, never represented as verified fact.
- Generated install scripts are review-only; AgentFit never silently executes third-party code.

## Verification
- 100+ automated cases covering legacy behavior, routing, malformed upstream data, official MCP lifecycle states, shell injection quoting, scoring bounds, and source failures.
- All Python modules compile.
