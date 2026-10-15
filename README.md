# VeriGraph AI

## 1. Project Overview

- **Project Title:** VeriGraph AI – Real-Time Propaganda Detection & Misinformation Intelligence Platform
- **Team Members:**  
  - Name – Roll Number  
  - Name – Roll Number  
  - Name – Roll Number  
  *(Add all team members and their roll numbers here.)*
- **Technology Stack:** Next.js, React, TypeScript, Python, FastAPI, PyTorch, HuggingFace Transformers, Scikit-Learn, D3.js, Docker
- **Project Guide/Mentor:**  
  *(Add guide/mentor name here.)*
- **Project Objective:**  
  VeriGraph AI is an open-source misinformation surveillance and claim verification platform designed to analyze online claims, identify potentially misleading or manipulative information, and visualize how information spreads across different digital sources. The system combines NLP-based transformer models, graph-based analysis, and multi-source data collection to generate an overall risk assessment for a given claim.

---

## 2. Problem Statement

The rapid spread of misinformation and propaganda across digital platforms makes it difficult for users to determine whether an online claim is reliable, misleading, or potentially manipulated.

Traditional fact-checking methods can be time-consuming and may not provide information about how a claim is spreading across different sources.

**VeriGraph AI** addresses this problem by providing an automated system that:

- Analyzes the language and framing of a claim.
- Performs AI-based fact verification.
- Examines relationships and patterns between information sources.
- Collects information from multiple online data sources.
- Generates a combined risk score.
- Provides visual representations of information propagation.

---

## 3. Features

- **AI-Based Claim Analysis**  
  Analyzes user-provided claims using transformer-based NLP models.

- **Fact Verification**  
  Uses BART-Large-MNLI to perform zero-shot natural language inference and classify claims.

- **Framing & Manipulation Detection**  
  Uses RoBERTa-Large-MNLI to analyze sensationalism, urgency, propaganda language, and potential bias.

- **Multi-Source Data Aggregation**  
  Collects information from News RSS feeds, GDELT, Telegram, CommonCrawl, and public feeds.

- **Graph-Based Propagation Analysis**  
  Represents relationships between sources and analyzes semantic and temporal connections.

- **Virality Metrics**  
  Calculates metrics such as estimated reach, virality score, platform distribution, and doubling rate.

- **Interactive Network Visualization**  
  Uses D3.js to display relationships and propagation patterns through an interactive graph.

- **Risk Score Generation**  
  Combines different analysis layers into a final risk score between 0 and 100.

- **Direct Source Attribution**  
  Provides links to relevant source articles and verification results.

- **Modern Web Interface**  
  Provides a responsive futuristic interface using Next.js, TailwindCSS, glassmorphism, and Framer Motion.

---

## 4. Technology Stack

| Category | Technologies |
|---|---|
| **Frontend** | Next.js 16, React 19, TypeScript |
| **UI & Styling** | TailwindCSS v4, Vanilla CSS, Glassmorphism, Framer Motion |
| **Graph Visualization** | D3.js, SVG |
| **Backend** | Python 3.10+, FastAPI, Uvicorn |
| **Machine Learning** | PyTorch, HuggingFace Transformers, Scikit-Learn |
| **AI Models** | BART-Large-MNLI, RoBERTa-Large-MNLI |
| **Data Collection** | HTTPX, Feedparser, XML ElementTree |
| **External Data Sources** | GDELT 2.0, CommonCrawl, News RSS, Telegram, Public Feeds |
| **Containerization** | Docker, Docker Compose |

The project uses a dual-transformer AI pipeline consisting of BART-MNLI for fact verification and RoBERTa-Large-MNLI for framing and manipulation analysis.

---

## 5. Project Structure

```text
VeriGraph-AI/
├── README.md
│
├── backend/
│   ├── main.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── services/
│   │   ├── nlp_analyzer.py
│   │   ├── ml_fact_checker.py
│   │   ├── gnn_analyzer.py
│   │   ├── fusion_engine.py
│   │   ├── graph_builder.py
│   │   └── scraper.py
│   │
│   ├── adapters/
│   │   ├── news_rss_adapter.py
│   │   ├── gdelt_client.py
│   │   ├── commoncrawl_client.py
│   │   ├── telegram_client.py
│   │   └── facebook_client.py
│   │
│   └── schemas/
│       └── contracts.py
│
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── page.tsx
    │   │   ├── layout.tsx
    │   │   ├── analysis/
    │   │   │   └── page.tsx
    │   │   └── api/
    │   │       ├── analyze/
    │   │       └── propagation/
    │   │
    │   ├── components/
    │   │   ├── LiveAmplificationFeed.tsx
    │   │   ├── PostsList.tsx
    │   │   ├── NetworkGraph.tsx
    │   │   ├── ScoreDisplay.tsx
    │   │   └── LayerBreakdown.tsx
    │   │
    │   ├── lib/
    │   │   ├── api.ts
    │   │   └── graph-fallback.ts
    │   │
    │   └── types/
    │       └── analysis.ts
    │
    └── package.json
```

The repository separates the FastAPI backend, AI services, data adapters, schemas, and Next.js frontend into dedicated modules.

---

## 6. Installation and Execution

### Option 1: Using Docker

Clone the repository:

```bash
git clone https://github.com/AyushPatwa11/VeriGraph-AI.git
cd VeriGraph-AI
```

Build and start the complete application:

```bash
docker compose up --build -d
```

Check the running containers:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs -f
```

The application can then be accessed through:

- **Frontend:** `http://localhost:3000`
- **Backend API:** `http://localhost:8000`
- **Swagger API Documentation:** `http://localhost:8000/docs`

To stop the application:

```bash
docker compose down
```

These Docker execution steps and local service addresses are specified in the project documentation.

### Option 2: Manual Setup

#### Backend

Navigate to the backend:

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
python -m uvicorn main:app --reload --port 8000
```

#### Frontend

Open another terminal:

```bash
cd frontend
```

Install Node.js dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

The frontend runs on:

```text
http://localhost:3000
```

The propagation demonstration is available at:

```text
http://localhost:3000/propagation-demo
```



---

## 7. Screenshots / Output

Add screenshots of the following sections of the application:

### Home Page

![Home Page](screenshots/home.png)

### Claim Analysis Dashboard

![Analysis Dashboard](screenshots/analysis.png)

### Risk Score

![Risk Score](screenshots/risk-score.png)

### Network Graph

![Network Graph](screenshots/network-graph.png)

### Propagation Analysis

![Propagation Analysis](screenshots/propagation.png)

> Replace the image paths above with the actual screenshots from the project.

---

## 8. DSA Concepts Used

The project uses several data structures and algorithmic concepts as part of its analysis and visualization pipeline.

### 1. Graphs

Graphs are a major component of VeriGraph AI.

The system represents relationships between sources using nodes and links. These relationships can represent semantic similarity, URL connections, source propagation, and temporal relationships.

The frontend uses D3.js to create an interactive force-directed graph.

### 2. Graph Analysis

The backend's graph analysis includes concepts such as:

- Graph density
- Clustering coefficients
- Network topology
- Source coordination
- Propagation relationships

The GNN analysis layer uses these network characteristics to contribute to the final risk assessment.

### 3. Hashing / Key-Based Data Mapping

Hash-based mappings can be used for efficiently associating sources, claims, posts, and graph nodes with their corresponding identifiers.

### 4. Arrays and Lists

Arrays/lists are used to store:

- News articles
- Social posts
- Graph nodes
- Graph links
- Analysis layers
- Platform data
- Model outputs

### 5. Searching

Searching is involved in retrieving and matching relevant information from external data sources and web indexes.

### 6. Sorting and Ranking

Collected information and analysis results can be ranked based on relevance, confidence, risk score, or propagation-related metrics.

### 7. Time and Space Complexity

The project involves processing multiple sources, text inputs, and graph relationships. Efficient data structures and algorithms are therefore important for handling increasing amounts of information.

> **Note:** The project documentation explicitly identifies graph/GNN analysis, clustering coefficients, graph density, semantic links, URL propagation, temporal windows, and virality analysis. Other DSA topics should only be claimed in the final academic report if they are actually present in the implementation.

---

## 9. Learning Outcomes

Through the development of VeriGraph AI, the team gained practical experience in:

- Developing a full-stack web application.
- Building REST APIs using FastAPI.
- Developing modern web interfaces using Next.js and React.
- Working with TypeScript.
- Integrating machine learning models using PyTorch and HuggingFace Transformers.
- Understanding Natural Language Inference and transformer-based NLP.
- Applying graph-based analysis to real-world information networks.
- Creating interactive data visualizations using D3.js.
- Working with real-time and external data sources.
- Designing modular backend architectures.
- Using Docker and Docker Compose for application deployment.
- Connecting frontend applications with backend APIs.

---

## 10. Future Scope

The project can be further improved by adding:

- Support for additional social media platforms.
- More advanced fact-checking models.
- Improved multilingual misinformation detection.
- More sophisticated Graph Neural Network models.
- Real-time streaming and continuous monitoring.
- User authentication and personalized dashboards.
- Historical misinformation trend analysis.
- Improved source credibility scoring.
- Automated alerts for rapidly spreading suspicious claims.
- Browser extensions for detecting potentially misleading content while browsing.
- Larger datasets for improving model accuracy.
- More advanced visualization and network-analysis techniques.

---

## 11. References

- **HuggingFace Transformers** – Used for integrating BART-MNLI and RoBERTa-Large-MNLI models.
- **PyTorch** – Machine learning framework used for neural model execution.
- **FastAPI Documentation** – Backend REST API development.
- **Next.js Documentation** – Frontend application development.
- **React Documentation** – UI development.
- **D3.js Documentation** – Interactive graph visualization.
- **GDELT 2.0** – Global event and news data.
- **CommonCrawl** – Web-scale web indexing and data.
- **News RSS Feeds** – News data aggregation.
- **Docker Documentation** – Containerization and deployment.
- **Scikit-Learn Documentation** – Machine learning utilities.

---

## 12. License

This project is distributed under the **MIT License**.

See the `LICENSE` file in the repository for complete license information.
