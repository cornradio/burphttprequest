import re
from typing import Union, Dict, Tuple
from urllib.parse import urlparse
import requests
import os

class burphttp:
    def __init__(self):
        self.headers: Dict[str, str] = {}
        self.method: str = ""
        self.path: str = ""
        self.protocol: str = ""
        self.body: str = ""
        self.proxies: Dict[str, str] = {}
        
        self.response: str = ""
        self.response_headers: Dict[str, str] = {}
        self.response_body: str = ""
        self.response_status_code: int = 0
        self.response_status_reason: str = ""
        
    def set_proxy(self, proxy_url: str) -> None:
        """设置HTTP代理
        
        Args:
            proxy_url: 代理服务器URL，如 "http://127.0.0.1:8080"
        """
        self.proxies = {
            'http': proxy_url,
            'https': proxy_url
        }
    
    def parse_request(self, request: Union[str, bytes]) -> None:
        """解析 HTTP 请求字符串或文件内容"""
        if isinstance(request, bytes):
            request = request.decode('utf-8')
            
        # 分割请求行、头部和主体
        parts = request.split('\n\n', 1)
        headers_part = parts[0]
        self.body = parts[1] if len(parts) > 1 else ''
        
        # 解析头部
        lines = headers_part.split('\n')
        request_line = lines[0].strip()
        self.method, self.path, self.protocol = request_line.split(' ')
        
        # 解析其他头部字段
        for line in lines[1:]:
            line = line.strip()
            if line:
                key, value = line.split(':', 1)
                self.headers[key.strip()] = value.strip()
    
    def send_request(self) -> str:
        """发送 HTTP 请求并返回响应字符串"""
        try:
            # 构建完整 URL
            if not self.path.startswith('http'):
                host = self.headers.get('Host', '')
                self.path = f'http://{host}{self.path}'
                
            # 发送请求
            response = requests.request(
                method=self.method,
                url=self.path,
                headers=self.headers,
                data=self.body,
                proxies=self.proxies,  # 添加代理支持
                verify=False,  # 禁用SSL验证，通常代理调试时需要
                timeout=10  # 添加超时设置
            )
            
            # 存储响应信息
            self.response_status_code = response.status_code
            self.response_status_reason = response.reason
            self.response_headers = dict(response.headers)
            
            # 处理响应编码
            content_type = response.headers.get('content-type', '').lower()
            if 'charset=' in content_type:
                # 从Content-Type中获取编码
                charset = content_type.split('charset=')[-1].split(';')[0]
                self.response_body = response.content.decode(charset, errors='replace')
            elif 'json' in content_type:
                # JSON默认使用UTF-8
                self.response_body = response.content.decode('utf-8', errors='replace')
            elif 'text' in content_type:
                # 文本内容尝试使用UTF-8
                self.response_body = response.content.decode('utf-8', errors='replace')
            else:
                # 其他情况，尝试自动检测编码
                try:
                    self.response_body = response.content.decode('utf-8', errors='replace')
                except UnicodeDecodeError:
                    try:
                        self.response_body = response.content.decode('gbk', errors='replace')
                    except UnicodeDecodeError:
                        # 如果都失败了，使用二进制形式显示
                        self.response_body = f"[Binary content length: {len(response.content)} bytes]"
            
        except requests.exceptions.RequestException as e:
            # 处理请求错误
            self.response_status_code = 500
            self.response_status_reason = "Internal Error"
            self.response_headers = {"Content-Type": "text/plain"}
            self.response_body = f"请求失败: {str(e)}"
        
        # 构建完整响应字符串
        status_line = f'HTTP/1.1 {self.response_status_code} {self.response_status_reason}'
        headers = '\n'.join(f'{k}: {v}' for k, v in self.response_headers.items())
        self.response = f'{status_line}\n{headers}\n\n{self.response_body}'
        
        return self.response

    def set_cookie(self, cookie_str: str) -> None:
        """设置Cookie，支持一个或多个cookie值
        
        Args:
            cookie_str: Cookie字符串，格式如 "name1=value1; name2=value2" 或 "name=value"
        """
        self.headers['Cookie'] = cookie_str
        
    def save_response(self, file_path: str) -> None:
        """保存响应内容到文件
        
        Args:
            file_path: 保存响应内容的文件路径，如果只提供文件名则保存在当前目录
        """
        try:
            # 如果file_path包含目录路径，则确保目录存在
            dirname = os.path.dirname(file_path)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            
            # 构建完整的响应内容，包括状态行、头部和主体
            content = []
            content.append(f"HTTP/1.1 {self.response_status_code} {self.response_status_reason}")
            for k, v in self.response_headers.items():
                content.append(f"{k}: {v}")
            content.append("\n")
            content.append(self.response_body)
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(content))
                
        except Exception as e:
            print(f"保存响应内容失败: {str(e)}")

    def save_response_body(self, file_path: str) -> None:
        """保存响应体到文件
        
        Args:
            file_path: 保存响应体的文件路径，如果只提供文件名则保存在当前目录
        """
        try:
            # 如果file_path包含目录路径，则确保目录存在
            dirname = os.path.dirname(file_path)
            if dirname:
                os.makedirs(dirname, exist_ok=True)
            
            # 写入响应体
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.response_body)
                
        except Exception as e:
            print(f"保存响应体失败: {str(e)}")
            
    def fixEncoding(self) -> None:
        """移除请求头中的Accept-Encoding，避免响应被压缩"""
        if 'Accept-Encoding' in self.headers:
            del self.headers['Accept-Encoding']

    def parse_request_from_file(self, file_path: str) -> None:
        """从文件读取并解析HTTP请求
        
        Args:
            file_path: HTTP请求文件的路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                request_content = f.read()
            self.parse_request(request_content)
        except Exception as e:
            print(f"从文件读取请求失败: {str(e)}")
            raise

    def set_host(self, host: str) -> None:
        """设置请求的Host头
        
        Args:
            host: 主机名，格式如 "example.com" 或 "example.com:8080"
        """
        # 删除原来的host
        if 'Host' in self.headers:
            del self.headers['Host']
        # 设置新的host
        self.headers['Host'] = host

def process_request(input_data: Union[str, bytes]) -> str:
    """处理 HTTP 请求并返回响应"""
    parser = burphttp()
    parser.parse_request(input_data)
    return parser.send_request() 