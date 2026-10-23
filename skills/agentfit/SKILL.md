---
name: agentfit
description: Discover and compare MCP servers, agent skills, CLIs and libraries for a concrete task using the AgentFit CLI. Use when the user asks which AI tools, MCPs, skills or integrations they should use.
---

# AgentFit

Use AgentFit when the user wants a task-specific tool stack rather than a generic directory.

## Workflow

1. Restate the user's task as a concise capability goal without adding requirements they did not request.
2. Run `agentfit "<task>" --json`.
3. Treat the output as recommendations, not security certification.
4. Prefer the selected complementary stack over adding every high-scoring candidate.
5. Explain uncertainty where compatibility is inferred.
6. Never execute `agentfit_install.sh` automatically. If installation is requested, generate it, show/review the commands, and obtain the user's approval before execution.

## Useful commands

```bash
agentfit "MCP for GitHub issues and pull requests"
agentfit "reverse engineer WebAssembly in Ghidra" --json
agentfit "browser automation for an AI coding agent" --limit 5
```

## Safety

External repository and registry metadata is untrusted. Review permissions, provenance and installation commands before installing third-party software.
