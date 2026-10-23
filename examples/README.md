# AgentFit examples

These examples are deliberately expressed as tasks rather than package names. Live recommendations depend on current registry data, so this repository does not hard-code a supposedly permanent winner.

| Goal | Try this |
|---|---|
| Reverse engineering | `agentfit "reverse engineer WebAssembly in Ghidra"` |
| Security research | `agentfit "audit a WordPress plugin for vulnerabilities"` |
| GitHub automation | `agentfit "MCP for GitHub issues and pull requests"` |
| Presentations | `agentfit "agent skill for creating PowerPoint presentations"` |
| Mobile | `agentfit "port a C++ game to iOS with Xcode and Metal"` |
| Full stack | `agentfit "React Native app with Supabase and Stripe"` |
| Document work | `agentfit "OCR scanned PDFs and extract structured data"` |
| DevOps | `agentfit "debug Kubernetes workloads and inspect logs"` |

## JSON automation

```bash
agentfit "security review a Python project" --json > agentfit-report.json
```

This makes AgentFit usable as a discovery component in another agent, CI job or UI without scraping terminal output.
