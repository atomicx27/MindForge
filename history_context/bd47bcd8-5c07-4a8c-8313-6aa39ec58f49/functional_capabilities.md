# Sovereign AGI: Functional Capabilities & Logic Flows

This document provides a stepwise breakdown of how the Sovereign AGI Framework (Automation-Infinite) executes its core missions. 

---

## 🏗️ 1. The Sentinel: Proactive Life Triage
**Goal**: Handle incoming communications and schedule management autonomously.

### Stepwise Logic:
1.  **The Pulse**: Every 60 seconds, the Sentinel scans its "Sensory Connectors" (Gmail/Outlook toggles must be **ON**).
2.  **Triage**: It fetches the last `N` unread threads and extracts metadata (Sender, Urgency, Context).
3.  **Semantic Injection**: It queries **ChromaDB** for previous interactions with that sender or related project keywords.
4.  **The "Rimuru" Filter**: It applies tactical coordination weights. 
    - *Decision*: Is this a task, a meeting, or just info?
5.  **Actuation**:
    - **Drafting**: It writes a high-fidelity reply directly in your "Drafts" folder.
    - **Scheduling**: It checks for conflicts and proposes a 30-minute block (FindFreeSlot).
6.  **Log & Learn**: The result is recorded in the `S-State`. If the user eventually sends the draft, the Sentinel creates a "Success Recipe."

---

## 🛠️ 2. The Forge: Autonomous Product Development
**Goal**: Build MVPs (0→1) based on concepts in your Obsidian Wiki.

### Stepwise Logic:
1.  **Trigger**: You tag a Wiki page with `#build` or `#forge`.
2.  **Context Harvest**: The Forge Agent reads the **Concept Page** (e.g., `[[Club-Matchmaking]]`) and extracts the "Technical Spec."
3.  **Sandbox Initialization**: The AGI spins up an isolated **Docker Container** (Ubuntu/Node/Python).
4.  **Iterative Construction**: 
    - **Step A**: `npx create-next-app` (or equivalent).
    - **Step B**: Generate the database schema for Supabase.
    - **Step C**: Write the core logic/components.
5.  **Verification**: The AGI runs `npm run build` or `pytest` **inside the container**.
6.  **Delivery**: The AGI exports the code to your specified folder and posts a "Build Report" to your Cyberpunk Dashboard.

---

## 🔮 3. The Oracle: Strategic Vision & Future-Projection
**Goal**: High-level problem solving, market analysis, and ROI simulation.

### Stepwise Logic:
1.  **Input**: User query (e.g., "Analyze the ROI of switching my stack to Go for the Super-App").
2.  **Complexity Scan**: The system calculates the **Complexity Score ($C$)**. 
3.  **The Oracle Activation**: If $C > 0.8$, the system toggles the **Cloud Strategic Mind** (Gemini 1.5 Pro / Claude 3.5).
4.  **Deep Research**: The Oracle searches the web and your entire **Memory Heritage** (Wiki).
5.  **Synthesis**: It generates a "Master Vision Document" using its advanced reasoning capabilities.
6.  **Sovereign Masking**: Before the data is returned, the **Safety Sanitizer** ensures no sensitive business logic is leaked back to the cloud training logs.

---

## 📜 4. The Scholar: Knowledge Management
**Goal**: Ensuring your Second Brain is always up-to-date and interlinked.

### Stepwise Logic:
1.  **Monitor**: The Scholar watches the **Google Drive Mount** for file changes.
2.  **Ingestion**: New markdown files are parsed according to `[[AGENTS.md]]` rules.
3.  **Vectorization**: The content is embedded and stored in **ChromaDB**.
4.  **Auto-Relinking**: If the Scholar finds a mention of a project in an email that isn't in the Wiki, it creates a **Stub Page** and asks you to fill it later.
5.  **Log Entry**: Every ingestion is recorded in `wiki/log.md` to maintain a transaction history.

---

## 💳 5. The Spend-Valve: Financial Actuator
**Goal**: Managing autonomous costs (APIs, Domain names, Cloud compute).

### Stepwise Logic:
1.  **Request**: An agent (e.g., The Forge) needs to buy a domain or spend $2.00 on a heavy API call.
2.  **Verification**: The `Spend-Sentry` checks the **Monthly Budget** in the `S-State`.
3.  **Validation**: 
    - *Under Threshold*: AGI approves it immediately and logs the transaction.
    - *Over Threshold*: AGI pauses and sends a **Push Notification** to your Dashboard for One-Tap Approval.
4.  **Execution**: The AGI uses the encrypted payment token to complete the purchase.
