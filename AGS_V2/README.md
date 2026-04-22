<div align="center">
  
# AXIOM CORE ⚡ (Formerly AGS v2)
**Mechanically-Enforced, Multi-Runtime Autonomous Agentic Framework**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-blue?logo=docker)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A highly opinionated, production-grade AI orchestration framework designed to eliminate LLM hallucination loops through hard mathematical bounds, Directed Acyclic Graph (DAG) state machines, and a specialized 10-Persona fleet.

</div>

<br/>

## 🧠 Why Axiom?
Most agentic frameworks rely on trusting the LLM to behave via prompt engineering alone. **Axiom Core does not.** 
Axiom forces LLMs into a mathematically rigid lifecycle, featuring Two-Phase execution commits, persistent memory indexing, multi-provider token routing, and an absolute separation of intelligence from physical execution.

### Key Features
*   **Two-Phase DAG Execution Pipeline:** Uses SQLite Write-Ahead-Logging to manage chronological dependencies. The system mechanically locks tasks when parent requirements aren't met.
*   **The Checksum Sandbox:** Uses explicit `git diff` boundaries and SHA-256 directory hashing to validate changes *before* physically committing them to your active codebase.
*   **Failure Memory (ChromaDB):** Try-Rewrite-Retry loops are mapped directly through Vector similarity searching (`all-MiniLM-L6-v2`), so the self-healer agent **never traps itself in an exact repetitive hallucination.**
*   **Hardware-Agnostic Proxy:** Intelligently rolls between local `Ollama`, heavy-offload Cloud GPU instances (`Colab + Ngrok`), and API endpoints (`Anthropic/OpenAI`) using a Redis-backed token bucket to dynamically prevent arbitrary rate limit crashes.
*   **Decoupled Tools (FastMCP):** Absolute isolation of Python actuator tools natively scaling across all Model Context Protocol (MCP) clients.

---

## 🏛️ The 10-Node Persona Fleet
Axiom does not use dynamic "one-size-fits-all" agents. Every instruction is routed through highly constrained classes that enforce Pydantic output schemas (`AgentResult`).

| Node | Role | Backend Architecture |
| :--- | :--- | :--- |
| **Ichigo** | Security Firewall | Regex pre-processing against destructive shell commands. |
| **Madara** | DAG Orchestrator | Strictly polls SQLite DB and manages the flow routing graph. |
| **Itachi** | Sandbox Auditor | Performs logical diff-checking before executing `dry_run` commits. |
| **Rimuru** | Context Bridge | Compresses system logs into Hard Anchors replacing context sliding. |
| **Naruto** | Self-Healer | Cross-references active stack traces against ChromaDB history vectors. |
| **Natsu** | Builder | Pure target string output and exact code logic generation. |
| **Goku** | AST Explorer | Semantic search and logic mapping. |
| **Chhota Bheem**| Dense Dispatcher | Hard-routes heavy loads down a proprietary Colab/Ngrok Tunnel. |
| **Doraemon** | Compositor | Plugs into 3rd-party MCP abstractions. |
| **Ben 10** | Web Fetch | Navigates diversity-scored endpoints to prevent bad data scraping. |

---

## ⚡ Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (If running strictly local bare-metal)

### 1. Boot Sub-Systems
Start the Axiom core (FastAPI), Redis Token-Bucket Limiter, the Next.js Observability UI, and the Python Sandbox Simulator.
```bash
docker-compose up -d
```

### 2. Enter Local Dev Environment (Optional Bare-Metal)
If you wish to test the internal runner locally without Docker isolating the paths:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1   # (Or source venv/bin/activate on Mac/Linux)
pip install -r requirements.txt
```

### 3. Launch System
```bash
python run.py
```
> The script will automatically construct `database.db` and the `/memory_data` Chroma collection.

---

## 🔭 Observability Dashboard
To view live telemetry, DAG queuing, and the Server-Sent Event (SSE) neural stream, open your web browser once docker-compose is active:
**[http://localhost:3000](http://localhost:3000)** or view the local HTML mock file `dashboard.html`.

---

## 🛡️ License
This framework is licensed under MIT. See the [`LICENSE`](LICENSE) file for more details. 
*Note: Ensure proper permissioning is established before plugging absolute root paths into the MCP File Write Actuators.*
