# Master Blueprint v7.0: Sovereign AGI Technical & Functional Manual

This is the **Definitive Architectural Truth** for Automation-Infinite. It serves as both the technical specification and the operational logic manual for the Sovereign AGI Framework.

---

## 🏛️ 1. Infrastructure: The Cloud HQ

The system is a persistent, cloud-native entity designed for absolute sovereignty and privacy.

- **Host**: **Oracle Cloud (Always Free ARM Instance)**.
  - **Specs**: 4 OCPUs, 24 GB RAM.
  - **OS**: Ubuntu 22.04 LTS.
- **Access**: **Password-Protected Public URL**.
  - **Security**: Nginx Reverse Proxy with Basic Auth.
- **Memory Bridge**: **Google Drive** (Mounted via `rclone` + FUSE).
  - **Sync**: Direct link to the Obsidian Vault (Second Brain).
- **Connectors**: **Google & Microsoft OAuth2**.
  - **Logic**: Manual "Activate Connection" toggles for Gmail/Outlook visibility.
- **Sovereign Toggle (100% Safety)**:
  - **GLOBAL**: LiteLLM may use Cloud Fallbacks (Gemini/Claude) for high-complexity tasks.
  - **SOVEREIGN**: All reasoning is restricted to the **Local Ollama** instance.

---

## 🎡 2. System Logic & Decision Loops

The framework operates on a shared, validated state via the **S-State Sentry**.

### 2.1 The Decision Cycle
Agents and logic loops (Sentinel/Forge) cannot write directly to the database. They must:
1.  **Read** the current S-State.
2.  **Propose** a mutation (using a Pydantic-guarded JSON request).
3.  **Validate**: The Sentry checks for type-safety, budget, and persona-policy compliance.
4.  **Mutate**: The state is atomically updated.

---

## 🎭 3. Functional Capabilities & Stepwise Logic

### 3.1 The Sentinel: Proactive Life Triage
**Logic Flow**:
1.  **Pulse**: Sentinel checks unread mail/calendar (if connectors are ON).
2.  **Context**: Queries **ChromaDB** for thread summaries or project tags.
3.  **Heuristic**: Applies "Rimuru" weights (Logistical priority).
4.  **Actuation**: Drafts a professionnel reply in Outlook or checks calendar conflicts.
5.  **Log**: Replay recorded in `infinite_core.db`.

### 3.2 The Forge: Autonomous Product Development
**Logic Flow**:
1.  **Trigger**: Detects `#forge` or `#build` tags in the Wiki.
2.  **Harvest**: Reads technical specs from the Obsidian Concept page.
3.  **Containment**: Spins up an isolated **Docker Sandbox** (WSL2 Architecture).
4.  **Build**: Iteratively generates code, installs dependencies, and writes DB schemas.
5.  **Verify**: Runs automated tests **inside the container**.
6.  **Deliver**: Exports the build logs and code snippets to the Singularity Dashboard.

### 3.3 The Oracle: Strategic Vision & Scaling
**Logic Flow**:
1.  **Input**: User query or high-complexity goal ($C > 0.8$).
2.  **Routing**: If "Sovereign Mode" is OFF, LiteLLM routes context (sanitized of PII) to Cloud APIs.
3.  **Research**: Performs deep web-search and Wiki synthesis.
4.  **Synthesis**: Generates a "Master Vision Document" or ROI simulation.
5.  **Reflection**: Stores the success as a "Recipe" in long-term memory.

### 3.4 The Scholar: Knowledge Management
**Logic Flow**:
1.  **Monitor**: Watches the Google Drive mount for `.md` changes.
2.  **Sync**: Parses new ingestion files into **ChromaDB**.
3.  **Integrate**: Auto-links new metadata to existing project entities.

---

## 🏁 4. Implementation Roadmap

### Phase 0: The Spinal Chord
- Setup **Oracle Cloud VM** and GDrive **rclone** mount.
- Initialize **ChromaDB** and **LiteLLM** (Local-to-Cloud proxy).
- Deploy the **S-State Sentry** (Mutation Guard).

### Phase 1: The Singularity Dashboard
- Build the **Cyberpunk** vs **Minimalist** UI (Stitch MCP).
- Integrate OAuth2 Toggles and the "Thought-Stream" telemetry panel.

### Phase 2: The Agentic Nation
- Enable recursive agent spawning and Docker-sandboxed Forge actions.
- Implement the "Spend-Valve" monthly budget actuator.

---

## 📜 5. Context Summary
- **Primary Goal**: Absolute agency with user-controlled safety boundaries.
- **Developer**: Pashin Kasad.
- **System Heritage**: Successor to Automation 1-5.
