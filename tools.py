import pandas as pd
from scapy.all import rdpcap
import json

class SecurityTools:
    @staticmethod
    def read_pcap_summary(pcap_path: str, max_packets: int = 20):
        """
        Reads a PCAP file and returns a JSON summary of traffic.
        Useful for identifying source IPs, destination IPs, and protocols.
        """
        try:
            print(f"    [Tool] Reading {pcap_path}...")
            packets = rdpcap(pcap_path)
            summary = []
            for pkt in packets[:max_packets]:
                if pkt.haslayer('IP'):
                    summary.append({
                        "src": pkt['IP'].src,
                        "dst": pkt['IP'].dst,
                        "proto": pkt['IP'].proto,
                        "len": len(pkt),
                        "flags": pkt['TCP'].flags if pkt.haslayer('TCP') else "N/A"
                    })
            return json.dumps(summary, indent=2)
        except Exception as e:
            return f"Error reading PCAP: {e}"

    @staticmethod
    def check_ip_reputation(ip_address: str):
        """
        Simulates checking a threat intelligence database for an IP.
        """
        # In a real app, this would hit VirusTotal API
        print(f"    [Tool] Checking reputation for {ip_address}...")
        known_bad_ips = ["192.168.1.105", "10.10.10.5"]
        if ip_address in known_bad_ips:
            return "CRITICAL: IP listed in ThreatDB as 'Botnet Controller'."
        return "SAFE: IP not found in blocklists."