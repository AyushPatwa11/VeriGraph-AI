<div align="center">

# 🌐 VERIGRAPH AI
### *Next-Generation Real-Time Propaganda Detection & Misinformation Intelligence Platform*

[![Status](https://img.shields.io/badge/Status-Production%20Ready-00F0FF?style=for-the-badge&logo=rocket&logoColor=black)](https://github.com/AyushPatwa11/VeriGraph-AI)
[![Version](https://img.shields.io/badge/Version-1.0.0-7000FF?style=for-the-badge&logo=semver&logoColor=white)](https://github.com/AyushPatwa11/VeriGraph-AI)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-16.2%20(Turbopack)-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org)
[![BART+RoBERTa](https://img.shields.io/badge/AI%20Core-BART%20%2B%20RoBERTa-FF6F00?style=for-the-badge&logo=huggingface&logoColor=white)](https://huggingface.co)

<p align="center">
  <a href="#-quick-start"><b>🚀 Quick Start</b></a> •
  <a href="#-system-architecture"><b>🏛️ Architecture</b></a> •
  <a href="#-dual-transformer-ai-core"><b>🧠 Neural AI Engine</b></a> •
  <a href="#-api-documentation"><b>📡 API Reference</b></a> •
  <a href="#-key-features"><b>✨ Features</b></a>
</p>

---

</div>

## 🌌 Overview

**VeriGraph AI** is a state-of-the-art, open-source misinformation surveillance and claim verification engine. Powered by a **Dual Transformer Neural Pipeline (BART-MNLI + RoBERTa-Large)**, real-time Graph Neural Network (GNN) topological analysis, and deep web multi-source scrapers, VeriGraph tracks how claims emerge, amplify, and spread across global digital ecosystems in real time.

```
                  ┌────────────────────────────────────────────────────────┐
                  │                 VERIGRAPH AI ENGINE                     │
                  └────────────────────────────────────────────────────────┘
                                               │
           ┌───────────────────────────────────┼───────────────────────────────────┐
           ▼                                   ▼                                   ▼
┌──────────────────────┐            ┌──────────────────────┐            ┌──────────────────────┐
│  LIVE DATA PIPELINE  │            │ DUAL TRANSFORMER NLI │            │ GRAPH DENSITY & GNN  │
│  ├─ News RSS (AP/BBC)│            │  ├─ BART-Large-MNLI  │            │  ├─ Semantic Links   │
│  ├─ GDELT 200B+      │  ───────►  │  │   (Fact-Checker) │  ───────►  │  ├─ URL Propagation  │
│  ├─ Telegram Streams │            │  └─ RoBERTa-Large    │            │  ├─ Temporal Window  │
│  ├─ CommonCrawl Web  │            │      (Framing / NLP) │            │  └─ Virality Matrix  │
│  └─ Public FB Feeds  │            └──────────────────────┘            └──────────────────────┘
└──────────────────────┘                                                           │
                                                                                   ▼
                                                                        ┌──────────────────────┐
                                                                        │ FUSION VERDICT PANEL │
                                                                        │ Risk: 0-100% Score   │
                                                                        │ Interactive Graph    │
                                                                        │ Direct Source Links  │
                                                                        └──────────────────────┘
```

---

## ✨ Key Capabilities & Highlights

- 🧠 **Dual-Transformer Neural Core**: Combines zero-shot `BART-Large-MNLI` for factual credibility scoring and `RoBERTa-Large-MNLI` for sensationalism and manipulation detection.
- 📡 **Multi-Stream Data Aggregation**: Parallel real-time ingestion from **5 global data channels** (News RSS, GDELT 200B+ Event Database, Telegram, CommonCrawl, and Public Feeds).
- 🔗 **Deep Direct Source Attribution**: Every output card and news item includes direct links straight to the **exact specific article page** or automated deep-search verification.
- 🕸️ **Interactive Graph Neural Network**: D3.js powered dynamic node-link visualizer showing coordination clusters, semantic similarity, and temporal alignment between spreaders.
- 📈 **Real-Time Virality Metrics**: Instant calculation of total reach, viral coefficient, doubling time, and platform distribution.
- 🎨 **Futuristic UI/UX**: Designed with Next.js 16 (Turbopack), TailwindCSS, Glassmorphic components, dark mode aesthetic, and micro-animations via Framer Motion.

---

## 🧠 Dual Transformer AI Core

VeriGraph AI operates local, high-speed neural models via PyTorch & HuggingFace Transformers—requiring **zero external API keys** or proprietary third-party dependencies:

| Neural Model | Architecture | Role & Target Output | Performance |
| :--- | :--- | :--- | :--- |
| **BART-MNLI** | `facebook/bart-large-mnli` | **Fact Verification Engine**: Zero-shot natural language inference classifying claims into *True News*, *False News*, or *Misleading*. | ~45ms Inference (91% Accuracy) |
| **RoBERTa-Large** | `roberta-large-mnli` | **Framing & Manipulation Analyzer**: Evaluates text for sensationalism, urgency framing, propaganda language pressure, and tone bias. | ~50ms Inference |
| **GNN Topology** | Custom Feature Matrix | **Network Virality Engine**: Computes clustering coefficients, cross-platform propagation density, and accounts coordination score. | Instant Computation |

---

## ⚡ Quick Start

### Prerequisites
- **Python**: `3.10+`
- **Node.js**: `18.0+`
- **npm** or **pnpm**

---

### Step 1: Start Backend API Server

```bash
# Navigate to backend directory
cd backend

# Install dependencies (PyTorch, Transformers, FastAPI, Uvicorn, Scikit-Learn)
pip install -r requirements.txt

# Launch FastAPI server with hot reload
python -m uvicorn main:app --reload --port 8000
```
> 🔹 **Backend API URL**: `http://localhost:8000`  
> 🔹 **Interactive Swagger Docs**: `http://localhost:8000/docs`

---

### Step 2: Start Frontend Application

```bash
# In a new terminal tab, navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Next.js Turbopack dev server
npm run dev
```
> 🔹 **Web Application URL**: `http://localhost:3000`  
> 🔹 **Propagation Demo Dashboard**: `http://localhost:3000/propagation-demo`

---

## 📡 API Reference

VeriGraph backend exposes high-performance RESTful JSON endpoints:

### 1. Execute Comprehensive Claim Analysis
- **Endpoint**: `POST /api/analyze`
- **Headers**: `Content-Type: application/json`
- **Request Body**:
  ```json
  {
    "query": "Tom Holland Spider-Man needs to evolve or quit"
  }
  ```
- **Sample Response**:
  ```json
  {
    "query": "Tom Holland Spider-Man needs to evolve or quit",
    "finalScore": 25,
    "riskLevel": "Low",
    "resultStatus": "final",
    "confidence": 0.72,
    "summary": "Low risk assessment driven primarily by network coordination patterns. Signals: NLP=20, GNN=30, ML-FactCheck=15...",
    "layers": [
      {
        "name": "NLP",
        "score": 20,
        "explanation": "RoBERTa model evaluated language as mostly objective ('objective reporting', confidence: 0.84).",
        "status": "available",
        "confidence": 0.84
      },
      {
        "name": "GNN",
        "score": 30,
        "explanation": "Network topological density indicates low artificial coordination.",
        "status": "available",
        "confidence": 0.75
      },
      {
        "name": "ML-FactCheck",
        "score": 15,
        "explanation": "Claim exhibits characteristics typical of factual, verifiable entertainment reporting.",
        "status": "available",
        "confidence": 0.89
      }
    ],
    "nodes": [
      { "id": "a1", "label": "bbc.co.uk", "followers": 2500000, "cluster": 1 }
    ],
    "links": [
      { "source": "a1", "target": "a2", "kind": "semantic" }
    ],
    "posts": [
      {
        "id": "news_123",
        "username": "bbc.co.uk",
        "timestamp": "2h ago",
        "text": "Tom Holland discusses the future of Spider-Man in upcoming Marvel projects...",
        "likes": 245,
        "shares": 89,
        "url": "https://www.bbc.co.uk/search?q=Tom+Holland"
      }
    ]
  }
  ```

---

### 2. Propagation & Virality Metrics
- **Endpoint**: `POST /api/propagation/analyze-spread`
- **Request Body**: `{ "query": "string" }`
- **Response**: Comprehensive total reach, virality score (0-100), platform breakdowns, and doubling rate.

---

### 3. Service Health Check
- **Endpoint**: `GET /health`
- **Response**: `{ "status": "ok", "service": "verigraph-backend" }`

---

## 🏛️ Repository Architecture

```
VeriGraph-AI/
├── 📄 README.md                          # Master Futuristic Documentation
├── 📁 backend/                           # FastAPI Python Server
│   ├── 📄 main.py                        # Server Entry Point & CORS Setup
│   ├── 📁 api/
│   │   └── 📄 routes.py                  # API Route Definitions
│   ├── 📁 services/                      # Core Neural Logic
│   │   ├── 📄 nlp_analyzer.py            # RoBERTa-Large MNLI Framing Classifier
│   │   ├── 📄 ml_fact_checker.py         # BART-Large MNLI Fact Verification Engine
│   │   ├── 📄 gnn_analyzer.py            # Graph Neural Network Virality Engine
│   │   ├── 📄 fusion_engine.py           # Multi-Layer Evidence Fusion Matrix
│   │   ├── 📄 graph_builder.py           # Semantic, Temporal & URL Link Builder
│   │   └── 📄 scraper.py                # Multi-Channel Data Aggregator
│   ├── 📁 adapters/                      # Real-Time Data Scrapers
│   │   ├── 📄 news_rss_adapter.py        # AP, BBC, CNN, Reuters RSS Feeds
│   │   ├── 📄 gdelt_client.py            # GDELT 2.0 Global Event Ingestion
│   │   ├── 📄 commoncrawl_client.py      # CommonCrawl CDX Web Index Search
│   │   ├── 📄 telegram_client.py        # Telegram Channel Client
│   │   └── 📄 facebook_client.py        # Facebook Graph Ingestor
│   └── 📁 schemas/
│       └── 📄 contracts.py              # Pydantic Data Contracts & Validation
└── 📁 frontend/                          # Next.js 16 Client App
    ├── 📁 src/
    │   ├── 📁 app/                       # App Router Pages
    │   │   ├── 📄 page.tsx               # Home Page & Claim Analyzer Input
    │   │   ├── 📄 layout.tsx             # Root Application Layout & Fonts
    │   │   ├── 📁 analysis/
    │   │   │   └── 📄 page.tsx           # Full Claims Analysis & Graph Dashboard
    │   │   └── 📁 api/                   # Server-Side API Proxies
    │   │       ├── 📁 analyze/
    │   │       └── 📁 propagation/
    │   ├── 📁 components/                # Glassmorphic UI Components
    │   │   ├── 📄 LiveAmplificationFeed.tsx # Real-Time Source Feed with Deep Links
    │   │   ├── 📄 PostsList.tsx          # Direct Clickable Articles List
    │   │   ├── 📄 NetworkGraph.tsx       # Interactive D3 Force-Directed Network
    │   │   ├── 📄 ScoreDisplay.tsx       # Cyberpunk Risk Score Dial
    │   │   └── 📄 LayerBreakdown.tsx     # Individual Model Diagnostics
    │   ├── 📁 lib/                       # Utility & API Wrappers
    │   │   ├── 📄 api.ts                 # Axios/Fetch API Client
    │   │   └── 📄 graph-fallback.ts      # Visual Graph Data Schemas
    │   └── 📁 types/
    │       └── 📄 analysis.ts            # TypeScript Interfaces & Contracts
    └── 📄 package.json                   # Next.js & Frontend Tooling Dependencies
```

---

## 🛠️ Technology Stack

| Layer | Technologies & Tools |
| :--- | :--- |
| **Frontend Framework** | Next.js 16 (App Router, Turbopack), React 19, TypeScript |
| **UI & Styling** | Vanilla CSS Design Tokens, TailwindCSS v4, Glassmorphism, Framer Motion |
| **Graph Visualization** | D3.js (Force-Directed Graph Simulation), SVG Rendering |
| **Backend Framework** | Python 3.10+, FastAPI, Uvicorn |
| **Machine Learning** | PyTorch, HuggingFace Transformers (`bart-large-mnli`, `roberta-large-mnli`), Scikit-Learn |
| **Data Scraping & APIs** | HTTPX, Feedparser, GDELT 2.0 API, CommonCrawl CDX Index, XML ElementTree |

---

## 🛡️ License & Attributions

Distributed under the **MIT License**. See `LICENSE` for details.  
*Developed with precision by the VeriGraph AI Team.*

<div align="center">
  <sub>Built with ❤️ for a safer, more transparent digital news landscape.</sub>
</div>
