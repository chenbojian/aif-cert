#!/usr/bin/env python3
"""
简单的HTTP服务器，用于提供问答网页应用
"""

import http.server
import socketserver
import os
import json
from urllib.parse import urlparse, parse_qs

class QuestionHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 解析URL
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # 如果请求根路径，返回index.html
        if path == '/':
            self.path = '/index.html'
        
        # 如果请求questions.jsonc，返回JSON数据
        elif path == '/questions.jsonc':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                with open('questions.jsonc', 'r', encoding='utf-8') as f:
                    content = f.read()
                    # 移除JSONC注释
                    lines = content.split('\n')
                    cleaned_lines = []
                    for line in lines:
                        # 移除行注释
                        if '//' in line:
                            line = line.split('//')[0]
                        if line.strip():
                            cleaned_lines.append(line)
                    
                    cleaned_content = '\n'.join(cleaned_lines)
                    self.wfile.write(cleaned_content.encode('utf-8'))
            except Exception as e:
                error_response = json.dumps({'error': str(e)})
                self.wfile.write(error_response.encode('utf-8'))
            return
        
        # 处理其他静态文件
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

def main():
    PORT = 8000
    
    # 确保在正确的目录中运行
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), QuestionHandler) as httpd:
        print(f"服务器启动在 http://localhost:{PORT}")
        print("按 Ctrl+C 停止服务器")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")

if __name__ == "__main__":
    main() 