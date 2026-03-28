from fastapi import APIRouter, Header, HTTPException
from datetime import datetime
import sys

from schemas.contracts import AnalyzeRequest, AnalyzeResponse
from services.orchestrator import Orchestrator
from services.scraper import ScraperService
from services.propagation_metrics import PropagationMetrics

router = APIRouter(prefix="/api", tags=["analysis"])
orchestrator = Orchestrator()
scraper = ScraperService()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(payload: AnalyzeRequest, x_request_id: str | None = Header(default=None)) -> AnalyzeResponse:
    query = payload.query.strip()
    if len(query) < 4:
        raise HTTPException(status_code=400, detail="Query must be at least 4 characters.")

    try:
        return await orchestrator.analyze(query)
    except HTTPException:
        raise
    except Exception as exc:
        # Print full traceback for debugging
        import traceback
        traceback.print_exc(file=sys.stderr)
        req_id = x_request_id or "n/a"
        error_msg = f"Analysis failed for request {req_id}: {str(exc)}"
        print(f"ERROR: {error_msg}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=error_msg) from exc


@router.post("/propagation/analyze-spread")
async def analyze_spread(payload: AnalyzeRequest) -> dict:
    """
    Analyze how a claim spreads across multiple sources (Facebook, News, GDELT, Telegram, CommonCrawl).
    
    Returns comprehensive propagation metrics including:
    - Total reach (sum of all engagement)
    - Platform breakdown (engagement by source)
    - Timeline analysis (spread over 24h, 7d, 30d)
    - Top spreaders (accounts with highest engagement)
    - Virality metrics (viral coefficient, doubling time, growth rate)
    """
    query = payload.query.strip()
    if len(query) < 4:
        raise HTTPException(status_code=400, detail="Query must be at least 4 characters.")
    
    try:
        # Collect posts from all 5 sources
        posts = await scraper.collect(query)
        
        if not posts:
            return {
                'query': query,
                'status': 'no_results',
                'message': 'No posts found for this claim across all sources',
                'analysis': None
            }
        
        # Calculate all metrics
        analysis = PropagationMetrics.analyze_spread(posts)
        
        return {
            'query': query,
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'total_posts_analyzed': len(posts),
            'analysis': analysis,
            'posts': posts
        }
    except HTTPException:
        raise
    except Exception as exc:
        import traceback
        traceback.print_exc(file=sys.stderr)
        error_msg = f"Propagation analysis failed: {str(exc)}"
        print(f"ERROR: {error_msg}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=error_msg) from exc


@router.get("/propagation/metrics/{metric_type}")
async def get_metric(metric_type: str, query: str) -> dict:
    """
    Get specific propagation metric for a claim.
    
    Args:
        metric_type: One of 'total_reach', 'platform_breakdown', 'timeline', 'top_spreaders', 'virality'
        query: The claim/query to analyze
    
    Returns:
        Specific metric data requested
    """
    if len(query) < 4:
        raise HTTPException(status_code=400, detail="Query must be at least 4 characters.")
    
    valid_metrics = ['total_reach', 'platform_breakdown', 'timeline', 'top_spreaders', 'virality']
    if metric_type not in valid_metrics:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid metric_type. Must be one of: {', '.join(valid_metrics)}"
        )
    
    try:
        # Collect posts from all sources
        posts = await scraper.collect(query)
        
        if not posts:
            return {
                'metric': metric_type,
                'query': query,
                'status': 'no_results',
                'data': None
            }
        
        # Get specific metric
        if metric_type == 'total_reach':
            metric_data = PropagationMetrics.calculate_total_reach(posts)
        elif metric_type == 'platform_breakdown':
            metric_data = PropagationMetrics.breakdown_by_platform(posts)
        elif metric_type == 'timeline':
            metric_data = PropagationMetrics.calculate_timeline(posts)
        elif metric_type == 'top_spreaders':
            metric_data = PropagationMetrics.identify_top_spreaders(posts)
        elif metric_type == 'virality':
            metric_data = PropagationMetrics.calculate_viral_coefficient(posts)
        else:
            raise ValueError(f"Unknown metric type: {metric_type}")
        
        return {
            'metric': metric_type,
            'query': query,
            'status': 'success',
            'data': metric_data
        }
    except HTTPException:
        raise
    except Exception as exc:
        import traceback
        traceback.print_exc(file=sys.stderr)
        error_msg = f"Failed to get {metric_type}: {str(exc)}"
        print(f"ERROR: {error_msg}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=error_msg) from exc

