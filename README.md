# Nmap-MCP: Agent-Based Network Scanning with DeepSeek API

## Mô tả dự án
Dự án này triển khai một agent sử dụng Nmap để quét mạng và DeepSeek API (thông qua OpenRouter) để phân tích kết quả quét. Agent được thiết kế theo mô hình MCP (Multi-Agent Control Protocol), trong đó agent điều phối các tác vụ quét và phân tích. Các tính năng chính:
- Quét mạng bằng Nmap (TCP SYN, phát hiện dịch vụ, hệ điều hành).
- Phân tích kết quả quét bằng DeepSeek API để phát hiện lỗ hổng bảo mật và đưa ra khuyến nghị.
- Lưu kết quả quét vào tệp (results/scan_results.txt).

Dự án được phát triển bằng Python và chạy trên Visual Studio Code, sử dụng môi trường ảo (venv) để quản lý thư viện.

## Cấu trúc dự án

Nmap-MCP/
├── venv/                     # Môi trường ảo Python
├── src/
│   ├── main.py              # Script chính điều phối agent
│   ├── nmap_scanner.py      # Module xử lý quét Nmap
│   ├── deepseek_analyzer.py # Module gọi DeepSeek API
│   └── config.py            # Cấu hình API key và IP mục tiêu
├── results/
│   └── scan_results.txt     # Kết quả quét
├── requirements.txt          # Danh sách thư viện
└── README.md                # Hướng dẫn này


## Mội trường thực hiện
- Hệ điều hành: Windows 11 .
- Python 3.12.
- Cài sẵn Nmap.
- Cài sẵn Visual Studio Code
- DeepSeek API Key

## Thiết lập môi trường
#2. Tạo và kích hoạt môi trường ảo
1. Tạo môi trường ảo:
   cd D:\Nmap-MCP
   python -m venv venv
2. Kích hoạt môi trường ảo:
   .\venv\Scripts\activate.bat
   - Nếu gặp lỗi The term '.\venv\Scripts\activate' is not recognized:
     - Kiểm tra thư mục venv\Scripts\ có tệp activate.bat không.
     - Xóa và tạo lại venv:
       powershell
       Remove-Item -Recurse -Force .\venv
       python -m venv venv
       .\venv\Scripts\activate.bat
### Cài đặt thư viện
Cài đặt các thư viện từ requirements.txt: pip install -r requirements.txt
### Cấu hình API Key và IP mục tiêu
1. Mở src/config.py.
2. Cập nhật:
   - DEEPSEEK_API_KEY: Thay bằng API key từ OpenRouter.
   - TARGET_IP: Thay bằng IP bạn có quyền quét (ví dụ: 192.168.1.1).

## Chạy chương trình
Kích hoạt môi trường ảo:
   .\venv\Scripts\activate.bat
   - Nếu terminal tự động kích hoạt (do .vscode/settings.json), bạn sẽ thấy (venv).
Chạy chương trình
1. Chạy script chính:
   python src\main.py
2. Nếu Nmap yêu cầu quyền quản trị (cho các lệnh như -sS hoặc -O):
   - Mở PowerShell với quyền admin:
     - Nhấn Win + X, chọn Windows PowerShell (Admin).
   - Điều hướng và kích hoạt venv:
     powershell
     cd D:\Nmap-MCP
     .\venv\Scripts\activate.bat
   - Chạy script:
     powershell
     python src\main.py
### Kiểm tra kết quả
- Kết quả quét: Lưu tại results/scan_results.txt.
- Phân tích từ DeepSeek: Hiển thị trên terminal, bao gồm nhận xét về lỗ hổng bảo mật và khuyến nghị.
- Nếu gặp lỗi:
  - Lỗi Nmap: Đảm bảo Nmap được cài và thêm vào PATH.
  - Lỗi API: Kiểm tra API key trong src/config.py và kết nối mạng.
  - Lỗi Python: Kiểm tra phiên bản Python và thư viện bằng pip list.
## Khắc phục sự cố
- Lỗi kích hoạt venv:
  - Kiểm tra venv\Scripts\activate.bat tồn tại.
  - Tái tạo venv (xem Thiết lập môi trường).
- Lỗi pip install:
  - Cập nhật pip:
    python -m pip install --upgrade pip
- Lỗi Nmap không tìm thấy:
  - Thêm Nmap vào PATH hoặc cài lại.
- Lỗi quyền admin:
  - Chạy PowerShell với quyền quản trị.