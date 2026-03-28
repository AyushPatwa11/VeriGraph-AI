"""
Source Credibility Tracker
Tracks source history and calculates credibility scores
"""

from typing import Dict, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class SourceMetrics:
    """Tracks metrics for a single source"""
    domain: str
    accuracy_rate: float = 0.5
    verification_mentions: int = 0
    domain_authority: float = 0.5
    claim_count: int = 0
    last_updated: datetime = field(default_factory=datetime.now)
    
    def update(self, accurate: bool, mention: bool = False):
        """Update metrics based on verification result"""
        self.claim_count += 1
        self.accuracy_rate = (
            0.8 * self.accuracy_rate + 0.2 * (1.0 if accurate else 0.0)
        )
        if mention:
            self.verification_mentions += 1
        self.last_updated = datetime.now()


class SourceCredibilityManager:
    """
    Manages source credibility tracking and scoring.
    
    Credibility = 0.4*accuracy + 0.3*mentions + 0.2*authority + 0.1*freshness
    """

    # Pre-mapped domain authority scores
    DOMAIN_AUTHORITY_MAP = {
        "bbc.com": 0.95,
        "reuters.com": 0.95,
        "apnews.com": 0.95,
        "npr.org": 0.90,
        "theguardian.com": 0.90,
        "ft.com": 0.88,
        "economist.com": 0.85,
        "nyt.com": 0.85,
        "washingtonpost.com": 0.85,
        "cnn.com": 0.80,
        "aljazeera.com": 0.85,
        "wsj.com": 0.85,
        "guardian": 0.90,
        "bbc": 0.95,
        "twitter": 0.50,
        "facebook": 0.45,
        "reddit": 0.40,
        "blog": 0.35,
        "unknown": 0.50,
    }

    WEIGHTS = {
        "accuracy": 0.40,
        "mentions": 0.30,
        "authority": 0.20,
        "freshness": 0.10,
    }

    def __init__(self):
        self.sources: Dict[str, SourceMetrics] = {}

    def get_credibility_score(self, domain: str) -> float:
        """Calculate credibility score for a domain (0-1)"""
        
        if domain not in self.sources:
            authority = self._get_domain_authority(domain)
            self.sources[domain] = SourceMetrics(domain=domain)
            self.sources[domain].domain_authority = authority
        
        source = self.sources[domain]
        
        # Freshness score (higher = more recent)
        freshness_days = (datetime.now() - source.last_updated).days
        freshness_score = max(0.1, 1.0 - (freshness_days / 30))
        
        # Mentions score (normalized)
        mentions_score = min(1.0, source.verification_mentions / 10.0)
        
        # Final score
        score = (
            self.WEIGHTS["accuracy"] * source.accuracy_rate
            + self.WEIGHTS["mentions"] * mentions_score
            + self.WEIGHTS["authority"] * source.domain_authority
            + self.WEIGHTS["freshness"] * freshness_score
        )
        
        return round(max(0.1, min(1.0, score)), 3)

    def _get_domain_authority(self, domain: str) -> float:
        """Get authority score for a domain"""
        domain_lower = domain.lower()
        
        # Direct match
        if domain_lower in self.DOMAIN_AUTHORITY_MAP:
            return self.DOMAIN_AUTHORITY_MAP[domain_lower]
        
        # Substring match
        for known_domain, authority in self.DOMAIN_AUTHORITY_MAP.items():
            if known_domain in domain_lower:
                return authority
        
        # Default
        return 0.50

    def update_source(self, domain: str, accurate: bool, mention: bool = False):
        """Update source metrics based on verification result"""
        if domain not in self.sources:
            self.sources[domain] = SourceMetrics(domain=domain)
        
        self.sources[domain].update(accurate, mention)

    def get_all_sources(self) -> Dict[str, float]:
        """Get credibility scores for all tracked sources"""
        return {
            domain: self.get_credibility_score(domain)
            for domain in self.sources.keys()
        }

    def get_source_info(self, domain: str) -> Dict:
        """Get detailed info about a source"""
        if domain not in self.sources:
            return {"status": "unknown", "credibility": 0.5}
        
        source = self.sources[domain]
        return {
            "domain": domain,
            "credibility": self.get_credibility_score(domain),
            "accuracy_rate": round(source.accuracy_rate, 3),
            "mention_count": source.verification_mentions,
            "authority": round(source.domain_authority, 3),
            "claim_count": source.claim_count,
        }
