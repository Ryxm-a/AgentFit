# Launch kit

## One-line pitch

**AgentFit — tell it the job, get the smallest useful AI tool stack.**

## GitHub / social launch

There are more MCP servers, agent skills and AI developer tools than anyone can reasonably evaluate by hand.

I built **AgentFit** to answer a different question:

> Not “what tools exist?” — **which tools fit this exact job, and which ones are redundant?**

AgentFit turns a natural-language task into requirements, searches live ecosystems, scores candidates using task fit + coverage + maintenance + trust signals, removes overlap, and returns a compact stack with evidence.

Try:

```bash
agentfit "MCP for GitHub issues and pull requests"
agentfit "reverse engineer WebAssembly in Ghidra"
agentfit "audit a WordPress plugin for vulnerabilities"
```

It is open source and intentionally treats generated install commands as reviewable output rather than silently executing third-party code.

Feedback I especially want: tasks where AgentFit recommends the wrong stack.

## Show HN title

`Show HN: AgentFit – tell it your task, get the right MCPs and agent skills`

## Reddit title

`I built AgentFit because AI tool directories tell me what exists, not what I should actually install`

## Short social post

`There are too many MCPs, agent skills and AI dev tools to evaluate manually. I built AgentFit: describe the job → requirements graph → live discovery → ranked, deduplicated stack. Open source.`

## Demo recording recipe

Record a real terminal session; do not animate fabricated scores.

1. Start with a clean terminal.
2. Run `agentfit "MCP for GitHub issues and pull requests"`.
3. Pause briefly on the requirements graph.
4. Show the selected stack and skipped overlap.
5. Run a second visually different query such as `agentfit "reverse engineer WebAssembly in Ghidra"`.
6. End on the repository URL.

Keep the clip under ~25 seconds and crop tightly around the terminal.
