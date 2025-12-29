# 🛡️ NetGuard Agents: Multi-Modal Network Defense System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![AI](https://img.shields.io/badge/AI-Google%20Gemini%201.5-orange)
![License](https://img.shields.io/badge/License-MIT-green)

**NetGuard Agents** is an autonomous Multi-Agent System (MAS) designed to automate Tier-1 Network Security triage. It orchestrates three specialized AI agents to correlate **Packet Capture (PCAP)** data with **Network Topology Diagrams**.



## 🤖 The Agent Team
1.  **Forensics Agent:** Uses `Scapy` to parse binary traffic logs and identify anomalies (SYN floods, port scanning).
2.  **Topology Agent:** Uses **Computer Vision** to analyze network diagrams and map physical infrastructure.
3.  **Orchestrator:** Synthesizes multi-modal data to produce a Root Cause Analysis (RCA).

## 🚀 Quick Start
1.  **Clone the Repo:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/NetGuard-Agents.git](https://github.com/YOUR_USERNAME/NetGuard-Agents.git)
    cd NetGuard-Agents
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure API:**
    Create a `.env` file and add your Google Gemini API key:
    ```env
    GEMINI_API_KEY=your_key_here
    ```
4.  **Run Simulation:**
    ```bash
    python generate_data.py  # Creates dummy attack data & diagrams
    python main.py           # Launches the agent swarm
    ```

## 💼 Business Logic
This project demonstrates **Agentic Workflow** applied to Cybersecurity:
* **Tool Use:** Agents execute Python code rather than just generating text.
* **Multi-Modality:** bridging the gap between visual documentation and text-based logs.