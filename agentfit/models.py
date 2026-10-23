from __future__ import annotations
from dataclasses import dataclass, field

@dataclass
class Requirement:
    tag: str
    label: str
    confidence: float
    search_terms: list[str] = field(default_factory=list)
    category: str = "capability"

@dataclass
class TaskAnalysis:
    task: str
    requirements: list[Requirement]
    ecosystem_hints: list[str] = field(default_factory=list)
    platform_hints: list[str] = field(default_factory=list)
    client_hints: list[str] = field(default_factory=list)

@dataclass
class UniversalCandidate:
    name: str
    url: str
    description: str = ""
    source: str = "unknown"
    kind: str = "unknown"
    version: str = ""
    updated_at: str = ""
    stars: int | None = None
    downloads: int | None = None
    quality: float | None = None
    maintenance: float | None = None
    popularity: float | None = None
    topics: list[str] = field(default_factory=list)
    matched_tags: list[str] = field(default_factory=list)
    install_hint: str = ""
    evidence: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)
    compatibility: dict[str, str] = field(default_factory=dict)
    components: dict[str, float] = field(default_factory=dict)
    score: float = 0.0

@dataclass
class Recommendation:
    candidate: UniversalCandidate
    recommended: bool
    reason: str
    covers: list[str] = field(default_factory=list)

@dataclass
class Report:
    task: str
    analysis: TaskAnalysis
    recommendations: list[Recommendation]
    errors: list[str]
    sources_used: list[str] = field(default_factory=list)
    environment: dict = field(default_factory=dict)

    @property
    def ranked(self):
        return self.recommendations
