import requests
import socket
import os
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL

class DeepSeekAnalyzer:
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.api_url = DEEPSEEK_API_URL
        # Cấu hình proxy (nếu cần, thay bằng proxy của bạn)
        self.proxies = {
            # "http": "http://proxy.company.com:8080",
            # "https": "http://proxy.company.com:8080"
        }

    def check_connectivity(self, host="api.openrouter.ai", port=443):
        """Kiểm tra kết nối đến host"""
        try:
            socket.create_connection((host, port), timeout=5)
            return True
        except socket.gaierror as e:
            return f"Lỗi kết nối: Không thể phân giải tên miền {host} ({str(e)})"
        except socket.timeout:
            return f"Lỗi kết nối: Hết thời gian chờ khi kết nối đến {host}"
        except Exception as e:
            return f"Lỗi kết nối: {str(e)}"

    def analyze_scan_results(self, scan_results):
        """Gửi kết quả quét đến DeepSeek API để phân tích"""
        # Kiểm tra kết nối
        connectivity = self.check_connectivity()
        if connectivity is not True:
            return connectivity

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        prompt = (
            "Bạn là chuyên gia bảo mật mạng. Hãy phân tích kết quả quét Nmap sau đây và cung cấp nhận xét về các lỗ hổng bảo mật tiềm ẩn, "
            "khuyến nghị cải thiện an ninh mạng, và bất kỳ rủi ro nào cần chú ý. Kết quả quét:\n\n"
            f"{scan_results}\n\n"
            "Vui lòng trả lời bằng tiếng Việt, ngắn gọn và rõ ràng."
        )
        
        payload = {
            "model": "deepseek-v3",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                proxies=self.proxies,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.RequestException as e:
            return f"Lỗi khi gọi DeepSeek API: {str(e)}"