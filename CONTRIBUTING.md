# Contributing to AgentFit

Thanks for helping improve AgentFit. The most valuable contributions make recommendations more accurate, explainable, resilient, or safe.

## Development setup

```bash
python -m pip install -e ".[dev]"
python -m pytest -q
```

## Good contributions

- New source adapters backed by stable, documented interfaces.
- Better task/capability extraction with regression tests.
- Ranking improvements demonstrated against realistic examples.
- Deduplication and identity-resolution fixes.
- Malformed-response, timeout and adversarial fixtures.
- Compatibility evidence improvements.
- Documentation that makes limitations clearer.

## Pull requests

Keep changes focused. Add or update tests for behavioral changes. Do not weaken an existing regression test merely to make a change pass. Source adapters must fail gracefully when upstream services are unavailable or malformed.

For recommendation logic, explain why the change improves task fit rather than only popularity. For install behavior, treat all external identifiers and metadata as untrusted input.

## Adding a source

A source should normalize external data into AgentFit's candidate model and preserve provenance. Avoid leaking source-specific assumptions into the ranking engine. If an ecosystem does not expose a stable supported API, document that boundary instead of presenting scraping as authoritative integration.

## Security

Do not open public issues for vulnerabilities that could put users at risk. Follow `SECURITY.md`.
