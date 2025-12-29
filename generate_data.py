from scapy.all import wrpcap, Ether, IP, TCP
from PIL import Image, ImageDraw, ImageFont

def create_dummy_pcap():
    print("Generating malicious PCAP...")
    packets = []
    # Normal Traffic
    for _ in range(5):
        packets.append(Ether()/IP(src="192.168.1.50", dst="10.0.0.5")/TCP(dport=443, flags="A"))
    
    # Malicious Traffic (SYN Flood)
    for _ in range(15):
        # 192.168.1.105 is our "bad actor"
        packets.append(Ether()/IP(src="192.168.1.105", dst="10.0.0.5")/TCP(dport=3306, flags="S"))
        
    wrpcap("traffic.pcap", packets)

def create_dummy_topology():
    print("Generating network diagram...")
    img = Image.new('RGB', (600, 400), color = (255, 255, 255))
    d = ImageDraw.Draw(img)
    
    # Draw simple network
    d.rectangle([50, 150, 150, 250], outline="black", width=3)
    d.text((60, 200), "User LAN", fill="black")
    
    d.rectangle([250, 150, 350, 250], outline="red", width=5)
    d.text((260, 200), "Firewall", fill="black")
    
    d.rectangle([450, 150, 550, 250], outline="blue", width=3)
    d.text((460, 200), "DB Server", fill="black")
    
    # Lines
    d.line([(150, 200), (250, 200)], fill="black", width=2)
    d.line([(350, 200), (450, 200)], fill="black", width=2)
    
    img.save('topology.png')

if __name__ == "__main__":
    create_dummy_pcap()
    create_dummy_topology()
    print("Data generation complete.")