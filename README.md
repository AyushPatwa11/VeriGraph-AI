# 📋 VeriGraph AI - Complete Documentation

**VeriGraph AI** is a comprehensive propaganda detection and claim verification system that analyzes how misinformation spreads across multiple sources (Facebook, News RSS, GDELT, Telegram, CommonCrawl) with real-time metrics, virality analysis, and visual propagation tracking.

**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: March 28, 2026

---

## 🎯 Quick Navigation

### I want to...

| Goal | Section | Time |
|------|---------|------|
| **Get running immediately** | [Quick Start (3 Steps)](#-quick-start-3-steps) | 5 mins |
| **Understand the system** | [System Architecture](#-system-architecture) | 10 mins |
| **Set up backend** | [Backend Setup](#-backend-setup) | 15 mins |
| **Configure Facebook/Reddit** | [Social Media Integration](#-facebook--reddit-integration-setup) | 10 mins |
| **See API endpoints** | [API Documentation](#-api-documentation) | 20 mins |
| **Deploy to production** | [Deployment Guide](#-deployment-guide) | 30 mins |
| **Integrate into my app** | [Integration Guide](#-integration-guide) | 20 mins |

---

## 🚀 Quick Start (3 Steps)

### What You'll Get
A complete propaganda detection system with:
- ✅ Live amplification feed showing how claims spread
- ✅ Propagation metrics across 5 data sources
- ✅ Claim verification with confidence scoring
- ✅ Threat assessment and virality analysis

### Step 1: Start Backend

```bash
cd backend
python -m uvicorn main:app --reload
# Server running: http://localhost:8000
```

### Step 2: Start Frontend

```bash
cd frontend
npm run dev
# App running: http://localhost:3000
```

### Step 3: Open Demo

```
Visit: http://localhost:3000/propagation-demo
```

Enter any claim to see:
- **Threat Assessment** (0-100 risk score)
- **Live Amplification Feed** (posts with sources & engagement)
- **Propagation Spread Analysis** (metrics across platforms)
- **Virality Indicators** (growth rate, doubling time)

---

## 💡 What the System Does

```
User Input: "Trump Dies with HeartAttack"
                    ↓
         [Backend Processing]
          ├─ Search 5 sources:
          │  ├─ News RSS (AP, BBC, CNN, Reuters)
          │  ├─ Facebook API (public posts)
          │  ├─ GDELT Global Events (200B+ events)
          │  ├─ Telegram Channels (public messages)
          │  └─ CommonCrawl Archive (200B+ pages)
          │
          ├─ Calculate Metrics:
          │  ├─ Total Reach (sum of engagement)
          │  ├─ Platform Distribution
          │  ├─ Timeline Analysis (24h/7d/30d)
          │  ├─ Top Spreaders (ranked by engagement)
          │  └─ Virality Score (0-100)
          │
          └─ Extract URLs for source attribution
                    ↓
       [Frontend Display]
         ├─ Threat Assessment (Risk Score)
         ├─ Metrics Dashboard (Reach, Timeline, Virality)
         └─ Live Feed (Individual posts with clickable links)
```

---

## ✨ Key Features

### Live Amplification Feed
- 🔴 Real-time live indicator
- 📰 Individual post display with metadata
- 🔗 **Clickable links** to original sources
- ❤️ Engagement metrics (likes, shares, comments)
- ⏰ Time-ago formatting ("45m ago", "2h ago")
- 🎨 Platform color coding (AP=red, BBC=blue, etc.)
- 🔥 High engagement badges
- ✨ Animated entries
- 📱 Responsive design

### Propagation Spread Component
- 📊 Total reach with engagement breakdown
- 📈 Platform distribution (bar/pie charts)
- ⏱️ Timeline analysis (24h/7d/30d windows)
- 🌟 Top spreaders leaderboard
- 📉 Virality score (0-100 gauge)
- 📊 Growth metrics (daily rate, doubling time)
- 🚀 Viral classification (non-viral to explosive)
- ✨ Animated visualizations

### Backend Capabilities
- ⚡ Parallel data collection from 5 sources
- 🔗 URL extraction and normalization
- ⚙️ Real-time metrics calculation
- 🛡️ Error handling and timeouts
- 🧪 Comprehensive test coverage (20+ tests)

---

## 🏛️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VERIGRAPH AI SYSTEM                       │
└─────────────────────────────────────────────────────────────┘

┌───── FRONTEND ─────────────────────────────────────────────┐
│ PropagationDemo Page                                        │
│ ├─ Search Interface                                        │
│ ├─ ScoreDisplay (threat level assessment)                 │
│ ├─ PropagationSpread (metrics visualization)              │
│ └─ LiveAmplificationFeed (individual posts with links)    │
└──────────────────────────────────────────────────────────────┘
                          ↓↑
                    HTTP/REST API
                          ↓↑
┌───── BACKEND API ──────────────────────────────────────────┐
│ POST /api/propagation/analyze-spread                       │
│ ├─ NewsRSSAdapter           → [posts with URLs]           │
│ ├─ FacebookClient           → [posts with URLs]           │
│ ├─ GDELTClient             → [posts with URLs]           │
│ ├─ TelegramClient          → [posts with URLs]           │
│ └─ CommonCrawlClient       → [posts with URLs]           │
│                                                             │
│ PropagationMetrics.analyze_spread(posts)                   │
│ ├─ calculate_total_reach()                                 │
│ ├─ breakdown_by_platform()                                 │
│ ├─ calculate_timeline()                                    │
│ ├─ identify_top_spreaders()                                │
│ └─ calculate_viral_coefficient()                           │
└──────────────────────────────────────────────────────────────┘
```

---

## 📊 Component Overview

### Frontend Components

| Component | File | Purpose | Size |
|-----------|------|---------|------|
| **LiveAmplificationFeed** | `frontend/src/components/LiveAmplificationFeed.tsx` | Individual posts with engagement & links | 400 lines |
| **PropagationSpread** | `frontend/src/components/PropagationSpread.tsx` | Aggregate metrics visualization | 500 lines |
| **PropagationDemo Page** | `frontend/src/app/propagation-demo/page.tsx` | Complete working example | 300 lines |

### Backend Services

| Service | File | Purpose | Lines |
|---------|------|---------|-------|
| **PropagationMetrics** | `backend/services/propagation_metrics.py` | Calculate all metrics | 400 |
| **ScraperService** | `backend/services/scraper.py` | Parallel collection from 5 sources | 300 |
| **API Routes** | `backend/api/routes.py` | REST endpoints | 150 |
| **Test Suite** | `backend/tests/test_propagation_metrics.py` | 20+ test cases | 350 |

---

## 📁 Project Structure

```
VeriGraph AI/
├── README.md                            # Master documentation (this file)
├── EXAMPLE_LIVE_FEED.py
├── backend/
│   ├── app.py, main.py, config.py
│   ├── adapters/                        # Data source adapters
│   │   ├── facebook_client.py
│   │   ├── reddit_client.py
│   │   ├── gdelt_client.py
│   │   ├── news_rss_adapter.py
│   │   └── ... (more adapters)
│   ├── services/                        # Business logic
│   │   ├── propagation_metrics.py
│   │   ├── scraper.py
│   │   └── ... (more services)
│   ├── api/routes.py                   # API endpoints
│   ├── tests/                          # Test suite
│   └── requirements.txt
├── frontend/                            # Next.js application
│   ├── src/components/
│   │   ├── LiveAmplificationFeed.tsx
│   │   ├── PropagationSpread.tsx
│   │   └── ...
│   ├── src/app/propagation-demo/
│   └── package.json
└── .gitignore
```

---

## 🔧 Backend Setup

### Prerequisites
- Python 3.8+
- pip or conda
- (Optional) GPU with CUDA 11.8+ for acceleration

### Installation

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
python -m uvicorn main:app --reload
```

### Configuration

Edit `config.py` or set environment variables:

```bash
export FLASK_ENV=development|production
export DEVICE=cuda|cpu|auto
export CACHE_ENABLED=true|false
export LOG_LEVEL=DEBUG|INFO|WARNING|ERROR
```

### Testing

```bash
pytest tests/ -v
pytest tests/ --cov=.
```

---

## 🌐 Facebook & Reddit Integration Setup

### Facebook Setup

1. **Create Developer Account**: [developers.facebook.com](https://developers.facebook.com)
2. **Create App** → Choose type: Consumer
3. **Get Access Token**:
   - Go to Settings → Basic (save App ID & Secret)
   - Tools → Access Token Tool
   - Request: `public_content`, `pages_read_engagement`
   - Copy User Access Token (valid ~2 months)
4. **Configure `.env`**:
   ```bash
   facebook_access_token=EABsbCS1iZC4BAJw7ZC...
   facebook_app_id=123456789012345
   facebook_app_secret=a1b2c3d4e5f6g7h8i9j0
   facebook_max_results=50
   ```
5. **Test**:
   ```python
   from adapters.facebook_client import FacebookClient
   import asyncio
   
   async def test():
       client = FacebookClient()
       posts = await client.search("vaccine safety")
   asyncio.run(test())
   ```

### Reddit Setup

1. **Create Account**: [reddit.com](https://reddit.com)
2. **Create App** at [reddit.com/user/settings/apps](https://reddit.com/user/settings/apps)
   - Type: "script"
   - Redirect URI: `http://localhost:8000`
3. **Get Credentials**: App shows Client ID & Secret
4. **Configure `.env`**:
   ```bash
   reddit_client_id=a1b2c3d4e5f6g7
   reddit_client_secret=aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890
   reddit_user_agent=VeriGraph/1.0 (by YourUsername)
   reddit_max_results=50
   ```
5. **Test**:
   ```python
   from adapters.reddit_client import RedditClient
   client = RedditClient()
   posts = await client.search("vaccine safety")
   ```

**API Limits**: Rate limiting by Reddit; keep `reddit_max_results` ≤ 50

---

## 📡 API Documentation

### Base URL
- **Development**: `http://localhost:8000`
- **Production**: `https://your-domain.com`

### Health Check

```bash
GET /health
# Response: {"status": "healthy", "service": "VeriGraph AI Backend", ...}
```

### Propagation Analysis

```bash
POST /api/propagation/analyze-spread
Content-Type: application/json

{"query": "vaccine safety concerns"}
```

**Response** includes:
- `total_reach`: Sum of all engagement
- `platform_breakdown`: Distribution by source
- `timeline`: Growth over 24h/7d/30d
- `top_spreaders`: Ranked accounts
- `virality`: Score 0-100

**Example Response**:
```json
{
  "query": "vaccine safety concerns",
  "status": "success",
  "analysis": {
    "total_reach": {"total_reach": 1755, "post_count": 45},
    "platform_breakdown": {
      "facebook": {"post_count": 10, "total_engagement": 535},
      "news": {"post_count": 15, "total_engagement": 700}
    },
    "timeline": {"24h": {}, "7d": {}, "30d": {}},
    "top_spreaders": [...],
    "virality": {"viral_coefficient": 0.65, "virality_score": 65}
  }
}
```

### Claim Verification

```bash
POST /api/verify
{"query": "The Earth is round", "use_cache": true}

# Verdict Score: 0-40 (TRUE), 40-60 (UNCERTAIN), 60-100 (FALSE)
```

### Batch Verification

```bash
POST /api/batch-verify
{"queries": ["claim1", "claim2", "claim3"]}
```

### Cache Management

```bash
GET /api/cache/status          # Cache statistics
POST /api/cache/clear          # Clear cache
GET /api/metrics               # Performance metrics
POST /api/metrics/reset        # Reset metrics
```

---

## 🔌 Integration Guide

### Backend Integration

```python
import requests

response = requests.post(
    "http://localhost:8000/api/propagation/analyze-spread",
    json={"query": "vaccine safety"}
)

data = response.json()
analysis = data['analysis']
print(f"Total Reach: {analysis['total_reach']['total_reach']}")
```

### Frontend Integration

```tsx
import { PropagationSpread } from "@/components/PropagationSpread";
import { LiveAmplificationFeed } from "@/components/LiveAmplificationFeed";

export default function ClaimAnalysisPage() {
  const [metrics, setMetrics] = useState(null);
  
  async function analyzeClaim(query: string) {
    const res = await fetch("/api/propagation/analyze-spread", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    const data = await res.json();
    setMetrics(data.analysis);
  }

  return (
    <div className="space-y-8">
      <PropagationSpread metrics={metrics} />
      <LiveAmplificationFeed posts={metrics?.top_spreaders} />
    </div>
  );
}
```

---

## 🚀 Deployment Guide

### Linux Server with Gunicorn + Nginx

```bash
# 1. Server Setup
sudo apt-get update && apt-get install -y python3.10 python3.10-venv nginx supervisor git

# 2. Create app user and directory
sudo useradd -m -s /bin/bash verigraph
sudo mkdir -p /home/verigraph/app
sudo chown -R verigraph:verigraph /home/verigraph/app

# 3. Setup application
sudo su - verigraph
git clone <repo> /home/verigraph/app
cd app/backend
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt gunicorn redis

# 4. Create supervisor config
cat > /etc/supervisor/conf.d/verigraph.conf << 'EOF'
[program:verigraph]
user=verigraph
directory=/home/verigraph/app/backend
command=/home/verigraph/app/backend/venv/bin/gunicorn --workers 4 --bind 127.0.0.1:5000 wsgi:application
autostart=true
autorestart=true
EOF

sudo supervisorctl reread && supervisorctl update && supervisorctl start verigraph

# 5. Nginx reverse proxy (see full guide for complete config)
# Create /etc/nginx/sites-available/verigraph with proxy settings

# 6. SSL with Let's Encrypt
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly -d your-domain.com
```

### Docker Deployment

```bash
docker build -t verigraph-backend:latest .
docker run -p 8000:8000 -e FLASK_ENV=production verigraph-backend:latest

# Or with Docker Compose
docker-compose up -d
```

---

## 🧪 Development & Testing

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-asyncio

# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=html

# Code quality
black . && flake8 . && mypy .
```

---

## 📊 Performance & Scalability

| Metric | Value |
|--------|-------|
| Cache Hit | 10-50ms |
| Single Verification | 2-5s |
| Propagation Analysis | 5-10s |
| Batch (10 items) | 15-30s |
| Memory (Base) | 2-4GB |
| GPU VRAM | 6-8GB |

---

## 🐛 Troubleshooting

### Out of Memory
```bash
# Reduce batch size
export BATCH_SIZE=5
# Use CPU
export DEVICE=cpu
# Enable caching
export CACHE_ENABLED=true
```

### Slow Inference
```bash
# Enable GPU
export DEVICE=cuda
# Reduce sources
export MAX_SOURCES=3
```

### Model Loading Issues
```bash
rm -rf ~/.cache/huggingface
python -c "from transformers import AutoModel; AutoModel.from_pretrained('model-name')"
```

### API Connection Issues
```bash
# Check backend running
curl http://localhost:8000/health

# Check firewall
sudo ufw allow 8000

# Check logs
tail -f logs/verigraph.log
```

---

## 📚 Support & Resources

### Documentation
- [Backend Configuration](#-backend-setup)
- [API Reference](#-api-documentation)
- [Integration Guide](#-integration-guide)
- [Deployment Guide](#-deployment-guide)

### Common Issues

| Issue | Solution |
|-------|----------|
| Port 8000 in use | `lsof -i :8000` and kill process |
| Module import errors | `pip install -r requirements.txt` |
| CUDA not found | Set `DEVICE=cpu` |
| Facebook API 401 | Refresh token at graph.facebook.com/explorer |
| Redis connection error | Verify Redis running with `redis-cli ping` |

---

**Last Updated**: March 28, 2026  
**Version**: 1.0.0  
**Status**: Production Ready
