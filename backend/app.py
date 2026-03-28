"""
VeriGraph Flask API Application
Main entry point for the backend service
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.exceptions import BadRequest
import logging
from datetime import datetime
import os

from services.verification import VerificationEngine
from services.cache import CacheManager
from services.metrics import MetricsCollector
from utils import generate_request_id

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize core services
verification_engine = VerificationEngine()
cache_manager = CacheManager()
metrics_collector = MetricsCollector()


@app.before_request
def log_request():
    """Log incoming requests"""
    logger.info(f"Request: {request.method} {request.path}")


@app.after_request
def log_response(response):
    """Log response status"""
    logger.info(f"Response: {response.status_code}")
    return response


# ============================================================================
# HEALTH CHECK ENDPOINTS
# ============================================================================

@app.route("/health", methods=["GET"])
def health_check():
    """Check API health status"""
    return jsonify({
        "status": "healthy",
        "service": "VeriGraph AI Backend",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
    }), 200


@app.route("/status", methods=["GET"])
def status():
    """Get detailed service status"""
    try:
        metrics = metrics_collector.get_system_stats()
        performance = metrics_collector.get_performance_stats()
        
        return jsonify({
            "service_status": "running",
            "metrics": {
                **metrics,
                **performance,
            }
        }), 200
    except Exception as e:
        logger.error(f"Status check error: {str(e)}")
        return jsonify({"error": "Could not retrieve status"}), 500


# ============================================================================
# VERIFICATION ENDPOINTS
# ============================================================================

@app.route("/api/verify", methods=["POST"])
def verify_claim():
    """
    Verify a claim and return a credibility score
    
    Request JSON:
    {
        "query": "The earth is flat",
        "sources": ["google.com", "wikipedia.org"],
        "use_cache": true
    }
    
    Response JSON:
    {
        "request_id": "abc123",
        "verdict_score": 8,
        "confidence": 0.87,
        "sources": [],
        "analysis": "...",
        "timestamp": "..."
    }
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        query = data.get("query", "").strip()
        sources = data.get("sources", [])
        use_cache = data.get("use_cache", True)
        
        if not query:
            return jsonify({"error": "Query cannot be empty"}), 400
        
        request_id = generate_request_id()
        logger.info(f"Processing verification request {request_id}: {query[:50]}...")
        
        # Check cache first
        cache_hit = False
        if use_cache:
            cached_result = cache_manager.get(query)
            if cached_result:
                cache_hit = True
                logger.info(f"Cache hit for request {request_id}")
                metrics_collector.record_request(
                    request_id=request_id,
                    query=query,
                    cache_hit=True,
                    final_score=cached_result["verdict_score"],
                    confidence=cached_result["confidence"],
                )
                return jsonify({
                    "request_id": request_id,
                    "cached": True,
                    **cached_result,
                }), 200
        
        # Run verification
        result = verification_engine.verify(query, sources)
        
        # Cache result
        if use_cache:
            cache_manager.set(query, result)
        
        # Record metrics
        metrics_collector.record_request(
            request_id=request_id,
            query=query,
            inference_ms=result.get("inference_time", 0),
            cache_hit=False,
            final_score=result.get("verdict_score", 50),
            confidence=result.get("confidence", 0.5),
        )
        
        return jsonify({
            "request_id": request_id,
            "cached": False,
            **result,
        }), 200
    
    except BadRequest:
        return jsonify({"error": "Invalid request format"}), 400
    except Exception as e:
        logger.error(f"Verification error: {str(e)}")
        metrics_collector.record_request(
            request_id=request_id if 'request_id' in locals() else "unknown",
            query=query if 'query' in locals() else "",
            error=True,
        )
        return jsonify({"error": "Verification failed", "details": str(e)}), 500


@app.route("/api/batch-verify", methods=["POST"])
def batch_verify():
    """
    Verify multiple claims in a batch
    
    Request JSON:
    {
        "queries": ["claim1", "claim2", "claim3"],
        "use_cache": true
    }
    
    Response JSON:
    {
        "batch_id": "xyz789",
        "results": [
            {"query": "claim1", "verdict_score": 45, ...},
            ...
        ]
    }
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        queries = data.get("queries", [])
        use_cache = data.get("use_cache", True)
        
        if not isinstance(queries, list) or not queries:
            return jsonify({"error": "Queries must be a non-empty list"}), 400
        
        batch_id = generate_request_id()
        logger.info(f"Processing batch {batch_id} with {len(queries)} queries")
        
        results = []
        for query in queries:
            if not query.strip():
                continue
            
            if use_cache:
                cached = cache_manager.get(query)
                if cached:
                    results.append({
                        "query": query,
                        "cached": True,
                        **cached,
                    })
                    continue
            
            result = verification_engine.verify(query)
            
            if use_cache:
                cache_manager.set(query, result)
            
            results.append({
                "query": query,
                "cached": False,
                **result,
            })
        
        return jsonify({
            "batch_id": batch_id,
            "total": len(queries),
            "processed": len(results),
            "results": results,
        }), 200
    
    except Exception as e:
        logger.error(f"Batch verification error: {str(e)}")
        return jsonify({"error": "Batch verification failed", "details": str(e)}), 500


# ============================================================================
# CACHE MANAGEMENT ENDPOINTS
# ============================================================================

@app.route("/api/cache/status", methods=["GET"])
def cache_status():
    """Get cache statistics"""
    stats = cache_manager.get_stats()
    return jsonify(stats), 200


@app.route("/api/cache/clear", methods=["POST"])
def clear_cache():
    """Clear the entire cache"""
    cache_manager.clear()
    logger.info("Cache cleared")
    return jsonify({"message": "Cache cleared"}), 200


# ============================================================================
# METRICS ENDPOINTS
# ============================================================================

@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    """Get comprehensive metrics report"""
    report = metrics_collector.get_full_report()
    return jsonify(report), 200


@app.route("/api/metrics/reset", methods=["POST"])
def reset_metrics():
    """Reset all metrics"""
    metrics_collector.reset()
    logger.info("Metrics reset")
    return jsonify({"message": "Metrics reset"}), 200


@app.route("/api/metrics/groundtruth", methods=["POST"])
def add_groundtruth():
    """
    Add ground truth data for accuracy tracking
    
    Request JSON:
    {
        "query": "Claim text",
        "verdict": "true" or "false"
    }
    """
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400
        
        data = request.get_json()
        query = data.get("query", "").strip()
        verdict = data.get("verdict", "").strip().lower()
        
        if not query or verdict not in ["true", "false"]:
            return jsonify({"error": "Invalid query or verdict"}), 400
        
        metrics_collector.record_groundtruth(query, verdict)
        return jsonify({"message": "Ground truth recorded"}), 200
    
    except Exception as e:
        logger.error(f"Error recording ground truth: {str(e)}")
        return jsonify({"error": "Could not record ground truth"}), 500


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    logger.error(f"Server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500


# ============================================================================
# APPLICATION STARTUP
# ============================================================================

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_ENV", "development") == "development"
    logger.info(f"Starting VeriGraph API server (debug={debug_mode})")
    
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=debug_mode,
        use_reloader=debug_mode,
    )
