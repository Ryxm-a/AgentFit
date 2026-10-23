# AgentFitBench

AgentFitBench is a transparent benchmark scaffold for measuring whether a tool recommender returns **useful, non-redundant, defensible stacks** rather than merely popular search results.

The benchmark intentionally ships tasks and metrics before publishing a headline score. Ground-truth judgments need human review; we will not manufacture an accuracy number.

## Metrics

- **Top-3 relevance:** at least one genuinely useful candidate in the first three.
- **Requirement coverage:** fraction of task requirements covered by the selected stack.
- **Redundancy:** selected candidates whose capability is already covered without meaningful added value.
- **Abandonment rate:** selected projects with clear stale/archive signals.
- **Compatibility precision:** compatibility claims supported by evidence.
- **Source resilience:** whether useful output survives one source failing.

## Running

```bash
python benchmarks/run.py
```

This produces JSONL reports in `benchmarks/results/`. Human labels can then be added separately for reproducible comparisons.
