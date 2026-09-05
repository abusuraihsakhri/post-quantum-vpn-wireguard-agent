# Post Quantum Vpn Wireguard Agent

> **Domain:** Post-Quantum Cryptography & Zero-Knowledge Architecture
> **Standards:** NIST FIPS 203/204/205, IETF Noise Protocol & PQC Hybrid Extension

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Post Quantum Vpn Wireguard Agent** is an analytical platform implementing PQC-WireGuard hybrid post-quantum tunneling with ML-KEM ratchet rotation. It provides a multi-worker evaluation engine for task processing with cryptographic audit trails and zero-PHI outbound protection.

---

## 🚀 Installation

### Prerequisites
- Python 3.10+
- pip

### Setup
```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/post-quantum-vpn-wireguard-agent.git
cd post-quantum-vpn-wireguard-agent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn pydantic pytest
```

### Environment Configuration
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and set your configuration
# Generate a secure audit key:
python -c "import os; print(os.urandom(32).hex())"
```

---

## ⚙️ Key Capabilities

- **Multi-Worker Evaluation Engine**: InvariantQC, SafetyEscalation, and ProtocolConformance workers
- **Zero-PHI Outbound Interceptor**: Active regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers
- **Tamper-Evident HMAC-SHA256 Audit Trail**: Chained, cryptographically signed logs for every evaluation
- **FastAPI REST API**: OpenAPI 3.1 endpoints with Prometheus telemetry (`/metrics`)
- **Batch Processing**: CSV-based batch task evaluation
- **Enrichment Suite**: Domain-specific engines for compliance, verification, and deployment readiness

---

## 💻 CLI Usage

### 1. Single Task Evaluation
```bash
python cli.py audit --task-id TASK-001 --target KEY-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 2. Supervisory Chat
```bash
python cli.py chat "What is the system status?"
```

### 3. Batch Processing
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. Verify Audit Trail
```bash
python cli.py verify-audit
```

### 5. Launch REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
| Parameter | Description | Default |
|:----------|:------------|:--------|
| `--task-id` | Unique task identifier | TASK-2026-001 |
| `--target` | Target identifier | KEY-TARGET-01 |
| `--primary` | Primary metric value | 28.5 |
| `--secondary` | Secondary metric value | 14.2 |
| `--critical` | Critical flag | False |
| `--status` | Status descriptor | DISCORDANT |

---

## 🌐 REST API Endpoints

| Method | Endpoint | Description |
|:-------|:---------|:------------|
| GET | `/health` | Health check |
| GET | `/metrics` | Prometheus metrics |
| POST | `/api/audit` | Submit task for evaluation |
| POST | `/api/chat` | Supervisory chat |
| GET | `/api/audit/logs` | Retrieve audit trail |

---

## 🧪 Testing

```bash
# Run all tests
pytest -v

# Run with coverage
pytest -v --cov=agents --cov=pqc_wireguard

# Run simulation benchmark
python simulator.py --tasks 1000
```

---

## 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t post-quantum-vpn-wireguard-agent .
docker run -p 8000:8000 --env-file .env post-quantum-vpn-wireguard-agent
```

---

## 🔒 Security

### Environment Variables
| Variable | Required | Description |
|:---------|:---------|:------------|
| `AUDIT_SECRET_KEY` | Yes (production) | HMAC-SHA256 key for audit trail integrity |
| `MODEL_PROVIDER` | No | LLM provider: mock, ollama, claude, openai (default: mock) |
| `HOST` | No | Server host (default: 127.0.0.1) |
| `PORT` | No | Server port (default: 8000) |

### Security Features
- **Zero-PHI Guard**: Blocks outbound PHI (SSN, MRN, phone, email, DOB, patient names)
- **Path Traversal Protection**: Safe file path resolution for batch operations
- **Audit Trail**: Cryptographic chaining prevents log tampering
- **Ephemeral Key Fallback**: Warns and generates temporary key if `AUDIT_SECRET_KEY` not set

---

## 📁 Project Structure

```
post-quantum-vpn-wireguard-agent/
├── agents/                  # Core agent modules
│   ├── api.py              # FastAPI REST server
│   ├── base.py             # Security, PHI guard, audit trail
│   ├── learning.py         # Bayesian calibration engine
│   ├── llm_factory.py      # LLM provider factory
│   ├── metrics.py          # Prometheus metrics collector
│   ├── models.py           # Pydantic data models
│   ├── streamer.py         # WebSocket telemetry
│   ├── supervisor.py       # Master orchestrator
│   └── workers.py          # Specialized evaluation workers
├── pqc_wireguard/          # PQC-WireGuard tunneling module
│   ├── agents.py           # Sub-agents (Noise, ML-KEM, Replay)
│   ├── cli.py              # PQC-WireGuard CLI
│   ├── engine.py           # Core algorithmic engine
│   ├── models.py           # Data models
│   └── server.py           # FastAPI server factory
├── tests/                  # Test suite
├── web/index.html          # Operations console UI
├── cli.py                  # Main CLI entry point
├── enrichment.py           # Domain enrichment engines
├── simulator.py            # High-throughput simulation
├── Dockerfile              # Container build
├── docker-compose.yml      # Container orchestration
└── pyproject.toml          # Project configuration
```

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
