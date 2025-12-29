from core_agents import ForensicsAgent, TopologyAgent, OrchestratorAgent
from tools import SecurityTools
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import os

console = Console()

def main():
    console.clear()
    console.print(Panel("[bold cyan]NetGuard Agents[/bold cyan] - Multi-Agent Defense System", subtitle="Powered by Gemini"))

    # 1. Setup
    tools = SecurityTools()
    forensics = ForensicsAgent(tools)
    topology = TopologyAgent()
    boss = OrchestratorAgent()

    # 2. Check for dummy data
    if not os.path.exists("traffic.pcap") or not os.path.exists("topology.png"):
        console.print("[red]Missing data! Please run `generate_data.py` first.[/red]")
        return

    # 3. The Incident
    incident_ticket = "User reports slow database access. Suspected denial of service or misconfig."
    console.print(f"[bold yellow]🔔 NEW INCIDENT:[/bold yellow] {incident_ticket}\n")

    # 4. Agent Execution Flow
    
    # Phase 1: Forensics
    with console.status("[cyan]Forensics Agent is investigating logs..."):
        forensics_prompt = f"Investigate 'traffic.pcap' for anomalies related to: {incident_ticket}"
        forensics_result = forensics.analyze(forensics_prompt)
        console.print(Panel(Markdown(forensics_result), title="🕵️ Forensics Report", border_style="cyan"))

    # Phase 2: Visual Topology
    with console.status("[purple]Topology Agent is inspecting diagrams..."):
        topo_prompt = "Describe the connection between the Users and the Database. Any single points of failure?"
        topo_result = topology.analyze_image("topology.png", topo_prompt)
        console.print(Panel(Markdown(topo_result), title="👁️ Topology Analysis", border_style="purple"))

    # Phase 3: Synthesis
    with console.status("[green]Orchestrator is generating Root Cause Analysis..."):
        final_report = boss.synthesize(forensics_result, topo_result)

    console.print(Panel(Markdown(final_report), title="✅ Final Root Cause Analysis", border_style="green"))

if __name__ == "__main__":
    main()