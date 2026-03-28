# VeriGraph API Documentation

## Overview

The VeriGraph API provides endpoints for claim verification, batch processing, cache management, and metrics tracking. All endpoints return JSON responses and support standard HTTP methods.

**Base URL**: `http://localhost:5000` (development) or `https://your-domain.com` (production)

**API Version**: 1.0.0

## Authentication

Currently, the API does not require authentication. For production:

```bash
# Coming soon: API key authentication
# Authorization: Bearer <your-api-key>
```

## Response Format

All responses follow a consistent JSON format:

```json
{
  "status": "success|error",
  "data": {},
  "timestamp": "2024-01-01T12:00:00",
  "request_id": "abc123"
}
```

## Error Handling

Error responses include a descriptive error message:

```json
{
  "error": "Invalid request",
  "details": "Query cannot be empty",
  "status_code": 400
}
```

### HTTP Status Codes

- `200 OK`: Successful request
- `400 Bad Request`: Invalid request format or parameters
- `401 Unauthorized`: Authentication required (future)
- `404 Not Found`: Endpoint not found
- `500 Internal Server Error`: Server error

## Endpoints

### Health & Status

#### GET /health

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "VeriGraph AI Backend",
  "version": "1.0.0",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### GET /status

Get detailed service status and metrics.

**Response:**
```json
{
  "service_status": "running",
  "metrics": {
    "uptime_seconds": 3600,
    "total_requests": 150,
    "avg_inference_ms": 2500,
    "cache_hit_rate": 0.32,
    "error_rate": 0.01
  }
}
```

### Claim Verification

#### POST /api/verify

Verify a single claim and return a credibility score.

**Request:**
```bash
curl -X POST http://localhost:5000/api/verify \
  -H "Content-Type: application/json" \
  -d '{
    "query": "The Earth is round",
    "sources": ["google.com", "wikipedia.org"],
    "use_cache": true
  }'
```

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| query | string | Yes | The claim to verify |
| sources | array | No | List of source URLs to check against |
| use_cache | boolean | No | Use cached results (default: true) |

**Response:**
```json
{
  "request_id": "abc123",
  "cached": false,
  "verdict_score": 15,
  "confidence": 0.92,
  "verdict": "TRUE",
  "sources": [
    {
      "title": "Earth - Wikipedia",
      "url": "https://en.wikipedia.org/wiki/Earth",
      "credibility": 0.95,
      "relevance": 0.88
    }
  ],
  "analysis": "The claim that the Earth is round is supported by overwhelming scientific evidence. Satellite imagery, gravity, and centuries of astronomical observations confirm this.",
  "sub_claims": [
    {
      "claim": "Earth has a spherical shape",
      "verdict_score": 10,
      "confidence": 0.95
    }
  ],
  "timestamp": "2024-01-01T12:00:00Z",
  "inference_time": 2500
}
```

**Verdict Score Interpretation:**
- `0-40`: **TRUE** - Claim is supported by evidence
- `40-60`: **UNCERTAIN** - Mixed or inconclusive evidence
- `60-100`: **FALSE** - Claim contradicted by evidence

**Status Codes:**
- `200`: Verification successful
- `400`: Invalid request (missing/empty query)
- `500`: Server error during verification

#### POST /api/batch-verify

Verify multiple claims in a single batch request.

**Request:**
```bash
curl -X POST http://localhost:5000/api/batch-verify \
  -H "Content-Type: application/json" \
  -d '{
    "queries": [
      "The Earth is round",
      "Water boils at 100°C",
      "The moon is made of cheese"
    ],
    "use_cache": true
  }'
```

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| queries | array | Yes | List of claims to verify |
| use_cache | boolean | No | Use cached results (default: true) |

**Response:**
```json
{
  "batch_id": "xyz789",
  "total": 3,
  "processed": 3,
  "timestamp": "2024-01-01T12:00:00Z",
  "results": [
    {
      "query": "The Earth is round",
      "verdict_score": 15,
      "confidence": 0.92,
      "verdict": "TRUE",
      "cached": false
    },
    {
      "query": "Water boils at 100°C",
      "verdict_score": 35,
      "confidence": 0.88,
      "verdict": "TRUE",
      "cached": true
    },
    {
      "query": "The moon is made of cheese",
      "verdict_score": 99,
      "confidence": 0.99,
      "verdict": "FALSE",
      "cached": false
    }
  ]
}
```

### Cache Management

#### GET /api/cache/status

Get cache statistics.

**Response:**
```json
{
  "size": 256,
  "max_size": 1000,
  "hits": 1243,
  "misses": 487,
  "hit_rate": 0.718,
  "memory_usage_mb": 125.5
}
```

#### POST /api/cache/clear

Clear the entire cache.

**Response:**
```json
{
  "message": "Cache cleared",
  "cleared_entries": 256
}
```

### Metrics & Monitoring

#### GET /api/metrics

Get comprehensive metrics report.

**Response:**
```json
{
  "system": {
    "uptime_seconds": 86400,
    "uptime_hours": 24.0,
    "total_requests": 5000,
    "request_rate_per_hour": 208.33,
    "start_time": "2024-01-01T00:00:00Z",
    "current_time": "2024-01-02T00:00:00Z"
  },
  "performance": {
    "total_requests": 5000,
    "avg_inference_ms": 2350.5,
    "max_inference_ms": 8500.0,
    "cache_hit_rate": 0.624,
    "error_rate": 0.008,
    "average_confidence": 0.845,
    "average_score": 45.2
  },
  "accuracy": {
    "accuracy": 0.876,
    "correct": 131,
    "total": 150
  }
}
```

#### POST /api/metrics/reset

Reset all metrics to initial state.

**Response:**
```json
{
  "message": "Metrics reset",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### POST /api/metrics/groundtruth

Record ground truth data for accuracy tracking.

**Request:**
```bash
curl -X POST http://localhost:5000/api/metrics/groundtruth \
  -H "Content-Type: application/json" \
  -d '{
    "query": "The Earth is round",
    "verdict": "true"
  }'
```

**Parameters:**
| Name | Type | Required | Description |
|------|------|----------|-------------|
| query | string | Yes | The claim |
| verdict | string | Yes | Ground truth verdict ("true" or "false") |

**Response:**
```json
{
  "message": "Ground truth recorded",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## Code Examples

### Python

```python
import requests
import json

BASE_URL = "http://localhost:5000"

def verify_claim(query, sources=None):
    """Verify a single claim"""
    payload = {
        "query": query,
        "sources": sources or [],
        "use_cache": True
    }
    
    response = requests.post(
        f"{BASE_URL}/api/verify",
        json=payload,
        timeout=30
    )
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Verification failed: {response.text}")

# Usage
result = verify_claim("The Earth is round")
print(f"Verdict: {result['verdict']}")
print(f"Confidence: {result['confidence']}")
print(f"Analysis: {result['analysis']}")
```

### JavaScript

```javascript
const BASE_URL = 'http://localhost:5000';

async function verifyClaim(query, sources = []) {
  const payload = {
    query: query,
    sources: sources,
    use_cache: true
  };

  try {
    const response = await fetch(`${BASE_URL}/api/verify`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Verification failed:', error);
    throw error;
  }
}

// Usage
verifyClaim('The Earth is round').then(result => {
  console.log(`Verdict: ${result.verdict}`);
  console.log(`Confidence: ${result.confidence}`);
});
```

### cURL

```bash
# Simple verification
curl -X POST http://localhost:5000/api/verify \
  -H "Content-Type: application/json" \
  -d '{
    "query": "The Earth is round",
    "use_cache": true
  }' | jq

# Batch verification
curl -X POST http://localhost:5000/api/batch-verify \
  -H "Content-Type: application/json" \
  -d '{
    "queries": ["Claim 1", "Claim 2", "Claim 3"],
    "use_cache": true
  }' | jq

# Get metrics
curl http://localhost:5000/api/metrics | jq
```

## Rate Limiting

Currently, the API supports unlimited requests. In production, rate limiting will be implemented:

```
- 100 requests per minute per IP
- 10,000 requests per hour per API key
```

## Pagination

Currently not implemented. Large batch responses may be limited to 100 items.

## Best Practices

1. **Use Caching**: Enable `use_cache: true` for better performance
2. **Batch Requests**: Use batch endpoint for multiple verifications
3. **Handle Errors**: Always check HTTP status codes
4. **Monitor Metrics**: Use `/api/metrics` to track performance
5. **Set Timeouts**: Use reasonable timeouts (30-120 seconds)
6. **Cache Results**: Store results locally to avoid reprocessing

## API Versioning

Current version: **v1**

Future versions will be available at:
- `/api/v2/verify`
- `/api/v2/batch-verify`

## Performance Tips

### Latency

- **Cache Hit**: ~50ms
- **Cold Start**: ~2000ms
- **Batch (10 items)**: ~15-20 seconds

### Optimization

1. Use GPU when available
2. Enable Redis caching
3. Increase worker count
4. Use batch verification for multiple claims

## Troubleshooting

### Slow Responses

```bash
# Check metrics
curl http://localhost:5000/api/metrics

# Check system status
curl http://localhost:5000/status
```

### Cache Issues

```bash
# Clear cache if stale
curl -X POST http://localhost:5000/api/cache/clear

# Check cache hits
curl http://localhost:5000/api/cache/status
```

### Error Responses

```bash
# Detailed error
curl -X POST http://localhost:5000/api/verify \
  -H "Content-Type: application/json" \
  -d '{
    "query": "",
    "use_cache": false
  }' | jq
```

## Support & Feedback

- **Issues**: Report bugs on GitHub
- **Questions**: Check documentation
- **Feedback**: Use feature request templates

---

**API Status**: ✅ Active and Stable  
**Last Updated**: 2024-01-01  
**Support Level**: Production Ready
