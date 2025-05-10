import nmap
import os
from config import TARGET_IP, OUTPUT_DIR

class NmapScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()
        self.target = TARGET_IP
        self.output_dir = OUTPUT_DIR

    def scan_network(self):
        """Thực hiện quét TCP SYN, phát hiện dịch vụ và hệ điều hành"""
        print(f"Đang quét {self.target}...")
        self.nm.scan(self.target, arguments="-sS -sV -O -p 1-1000")
        
        result = []
        for host in self.nm.all_hosts():
            host_info = f"Host: {host} ({self.nm[host].hostname()})\n"
            host_info += f"State: {self.nm[host].state()}\n"
            
            for proto in self.nm[host].all_protocols():
                host_info += f"Protocol: {proto}\n"
                ports = self.nm[host][proto].keys()
                for port in sorted(ports):
                    port_info = self.nm[host][proto][port]
                    host_info += f"Port: {port}\tState: {port_info['state']}\tService: {port_info.get('name', 'unknown')}\n"
            
            if 'osclass' in self.nm[host]:
                host_info += "OS Details:\n"
                for osclass in self.nm[host]['osclass']:
                    host_info += f"Type: {osclass['type']} | Vendor: {osclass['vendor']} | OS Family: {osclass['osfamily']}\n"
            
            result.append(host_info)
        
        # Lưu kết quả vào tệp
        os.makedirs(self.output_dir, exist_ok=True)
        output_file = os.path.join(self.output_dir, "scan_results.txt")
        with open(output_file, "w") as f:
            f.write("\n".join(result))
        
        print(f"Kết quả quét đã được lưu tại {output_file}")
        return "\n".join(result)