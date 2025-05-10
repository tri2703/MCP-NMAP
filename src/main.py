import nmap
import json
import requests
import os
from config import DEEPSEEK_API_KEY, TARGET_HOST, SCAN_PORTS

def scan_network(target, ports):
    """Perform an Nmap scan on the target host."""
    nm = nmap.PortScanner()
    try:
        print(f"Scanning {target} on ports {ports}...")
        nm.scan(target, ports, arguments='-sS -O')  # SYN scan with OS detection
        scan_results = {
            "target": target,
            "hosts": []
        }
        
        for host in nm.all_hosts():
            host_data = {
                "ip": host,
                "state": nm[host].state(),
                "ports": [],
                "os": nm[host].get('osmatch', [{}])[0].get('name', 'Unknown')
            }
            for proto in nm[host].all_protocols():
                ports = nm[host][proto].keys()
                for port in ports:
                    port_data = {
                        "port": port,
                        "state": nm[host][proto][port]['state'],
                        "service": nm[host][proto][port]['name']
                    }
                    host_data["ports"].append(port_data)
            scan_results["hosts"].append(host_data)
        
        # Save results to file
        os.makedirs('results', exist_ok=True)
        safe_target = target.replace('/', '_').replace(':', '_')
        result_file = f"results/scan_{safe_target}.json"
        with open(result_file, 'w') as f:
            json.dump(scan_results, f, indent=4)
        print(f"Scan results saved to {result_file}")
        return scan_results
    except Exception as e:
        print(f"Error during scan: {e}")
        return None

def local_analysis(scan_results):
    """Fallback analysis if DeepSeek API fails."""
    open_ports = [
        f"Port {p['port']} ({p['service']})"
        for host in scan_results['hosts']
        for p in host['ports']
    ]
    analysis = f"""
    - Số host phát hiện: {len(scan_results['hosts'])}
    - Hệ điều hành: {[host['os'] for host in scan_results['hosts']] if scan_results['hosts'] else 'Không xác định'}
    - Các cổng mở: {', '.join(open_ports) if open_ports else 'Không có cổng mở'}
    - Rủi ro tiềm ẩn: {'Cổng mở có thể bị khai thác nếu không được bảo mật.' if open_ports else 'Không phát hiện cổng mở, nhưng cần kiểm tra thêm.'}
    - Khuyến nghị: {'Cấu hình firewall và cập nhật phần mềm.' if open_ports else 'Kiểm tra kết nối mạng và quyền truy cập.'}
    """
    return analysis

def analyze_results_with_deepseek(scan_results):
    """Send scan results to DeepSeek API for analysis."""
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    open_ports = [
        f"Port {p['port']} ({p['service']})"
        for host in scan_results['hosts']
        for p in host['ports']
    ]
    prompt = f"""
    Phân tích kết quả quét Nmap sau:
    - Mục tiêu: {scan_results['target']}
    - Số host: {len(scan_results['hosts'])}
    - Cổng mở: {', '.join(open_ports) if open_ports else 'Không có'}
    Cung cấp tóm tắt ngắn gọn, rủi ro bảo mật tiềm ẩn và khuyến nghị.
    """
    
    payload = {
        "model": "deepseek-chat",  # Updated model (verify with documentation)
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500
    }
    
    try:
        print("Gửi payload:", json.dumps(payload, indent=2, ensure_ascii=False))
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        analysis = response.json()['choices'][0]['message']['content']
        return analysis
    except requests.RequestException as e:
        print(f"Lỗi khi gọi DeepSeek API: {e}")
        if e.response:
            print("Nội dung phản hồi:", e.response.text)
        print("Sử dụng phân tích cục bộ làm phương án dự phòng...")
        return local_analysis(scan_results)

def format_output(scan_results, analysis):
    """Format output in the requested structure."""
    open_ports = [
        f"Port {p['port']} ({p['service']})"
        for host in scan_results['hosts']
        for p in host['ports']
    ]
    result_output = f"""
Kết quả scan của Nmap:
- Mục tiêu: {scan_results['target']}
- Số host phát hiện: {len(scan_results['hosts'])}
- Hệ điều hành: {[host['os'] for host in scan_results['hosts']] if scan_results['hosts'] else 'Không xác định'}
- Các cổng mở: {', '.join(open_ports) if open_ports else 'Không có cổng mở'}

Phân tích kết quả scan được:
{analysis}
    """
    safe_target = scan_results['target'].replace('/', '_').replace(':', '_')
    analysis_file = f"results/analysis_{safe_target}.txt"
    with open(analysis_file, 'w', encoding='utf-8') as f:
        f.write(result_output)
    print(result_output)
    print(f"Phân tích đã lưu vào {analysis_file}")

def main():
    """Main function to run the Nmap scan and analysis."""
    scan_results = scan_network(TARGET_HOST, SCAN_PORTS)
    if not scan_results:
        print("Quét thất bại. Thoát chương trình.")
        return
    
    analysis = analyze_results_with_deepseek(scan_results)
    format_output(scan_results, analysis)

if __name__ == "__main__":
    main()