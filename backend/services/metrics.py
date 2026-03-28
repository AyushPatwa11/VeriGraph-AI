"""
Metrics Tracking for VeriGraph
- Request counting
- Cache performance
- Inference timing
- Accuracy tracking
"""

from typing import Dict, List, Any
from datetime import datetime
from dataclasses import dataclass, field
import statistics


@dataclass
class RequestMetrics:
    """Metrics for a single request"""
    request_id: str
    query: str
    timestamp: datetime = field(default_factory=datetime.now)
    inference_ms: float = 0.0
    cache_hit: bool = False
    source_credibility_avg: float = 0.5
    final_score: int = 0
    confidence: float = 0.5
    error: bool = False


class MetricsCollector:
    """Collect system-wide metrics for monitoring"""

    def __init__(self):
        self.requests: List[RequestMetrics] = []
        self.groundtruth: Dict[str, str] = {}
        self.start_time = datetime.now()

    def record_request(
        self,
        request_id: str,
        query: str,
        inference_ms: float = 0.0,
        cache_hit: bool = False,
        source_credibility: float = 0.5,
        final_score: int = 0,
        confidence: float = 0.5,
        error: bool = False,
    ):
        """Record metrics for a single request"""
        metric = RequestMetrics(
            request_id=request_id,
            query=query,
            inference_ms=inference_ms,
            cache_hit=cache_hit,
            source_credibility_avg=source_credibility,
            final_score=final_score,
            confidence=confidence,
            error=error,
        )
        self.requests.append(metric)

    def record_groundtruth(self, query: str, actual_verdict: str):
        """Record ground truth for accuracy tracking"""
        self.groundtruth[query] = actual_verdict

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        if not self.requests:
            return {}
        
        # Inference times (excluding cache hits)
        inference_times = [
            r.inference_ms for r in self.requests if not r.cache_hit
        ]
        
        cache_hits = sum(1 for r in self.requests if r.cache_hit)
        errors = sum(1 for r in self.requests if r.error)
        confidences = [r.confidence for r in self.requests]
        scores = [r.final_score for r in self.requests]
        
        return {
            "total_requests": len(self.requests),
            "avg_inference_ms": round(
                statistics.mean(inference_times) if inference_times else 0, 2
            ),
            "max_inference_ms": round(
                max(inference_times) if inference_times else 0, 2
            ),
            "cache_hit_rate": round(cache_hits / len(self.requests), 3),
            "error_rate": round(errors / len(self.requests), 3),
            "average_confidence": round(statistics.mean(confidences), 3),
            "average_score": round(statistics.mean(scores), 1),
        }

    def get_accuracy(self) -> Dict[str, Any]:
        """Get accuracy statistics vs ground truth"""
        if not self.groundtruth or not self.requests:
            return {"status": "No ground truth data yet"}
        
        correct = 0
        total = 0
        
        for request in self.requests:
            if request.query in self.groundtruth:
                total += 1
                predicted_verdict = "true" if request.final_score < 40 else "false"
                if predicted_verdict == self.groundtruth[request.query]:
                    correct += 1
        
        if total == 0:
            return {"status": "No matching ground truth data"}
        
        accuracy = correct / total
        return {
            "accuracy": round(accuracy, 3),
            "correct": correct,
            "total": total,
        }

    def get_system_stats(self) -> Dict[str, Any]:
        """Get overall system statistics"""
        uptime_seconds = (datetime.now() - self.start_time).total_seconds()
        uptime_hours = uptime_seconds / 3600
        request_rate = len(self.requests) / max(uptime_hours, 0.01)
        
        return {
            "uptime_seconds": int(uptime_seconds),
            "uptime_hours": round(uptime_hours, 2),
            "total_requests": len(self.requests),
            "request_rate_per_hour": round(request_rate, 2),
            "start_time": self.start_time.isoformat(),
            "current_time": datetime.now().isoformat(),
        }

    def get_full_report(self) -> Dict[str, Any]:
        """Get comprehensive metrics report"""
        return {
            "system": self.get_system_stats(),
            "performance": self.get_performance_stats(),
            "accuracy": self.get_accuracy(),
        }

    def reset(self):
        """Clear all metrics"""
        self.requests.clear()
        self.groundtruth.clear()
        self.start_time = datetime.now()
