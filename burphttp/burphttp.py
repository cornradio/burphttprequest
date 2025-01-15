import re
from typing import Union, Dict, Tuple
from urllib.parse import urlparse, parse_qs, urlencode
import requests
from requests.models import PreparedRequest
import urllib3
import os

# 禁用不安全请求的警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
        
        self.params: Dict[str, list] = {}
        self.verify: bool = False  # 默认禁用SSL验证
        
    def set_proxy(self, proxy_url: str) -> None:
        """设置HTTP代理
        
        Args:
            proxy_url: 代理服务器URL，如 "http://127.0.0.1:8080"
            如果输入为空字符串，则不设置代理
        """
        if proxy_url != "":   
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
        self.method, full_path, self.protocol = request_line.split(' ')
        
        # 解析路径和查询参数
        url_parts = full_path.split('?', 1)
        self.path = url_parts[0]
        if len(url_parts) > 1:
            query_string = url_parts[1]
            self.params = parse_qs(query_string)
        
        # 解析其他头部字段
        for line in lines[1:]:
            line = line.strip()
            if line:
                key, value = line.split(':', 1)
                self.headers[key.strip()] = value.strip()
    
    def send_request(self) -> str:
        """发送 HTTP 请求并返回响应字符串
        
        Returns:
            str: 完整的HTTP响应字符串，包含状态行、响应头和响应体
        
        Raises:
            requests.exceptions.RequestException: 当请求发生错误时
        """
        # 构建完整URL
        url = self._build_full_url()
        
        # 创建session以支持HTTP/2
        session = requests.Session()
        
        # 如果有Cookie头，设置到session中
        if 'Cookie' in self.headers:
            # 解析Cookie字符串
            cookie_str = self.headers['Cookie']
            cookies = {}
            for item in cookie_str.split(';'):
                if '=' in item:
                    name, value = item.strip().split('=', 1)
                    cookies[name] = value
            # 设置到session中
            session.cookies.update(cookies)
            # 移除headers中的Cookie，因为已经设置到session中了
            del self.headers['Cookie']
        
        # 添加默认请求头
        default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'Accept': 'text/html',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Ch-Ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Priority': 'u=1, i'
        }
        
        # 合并默认头部和用户设置的头部，用户设置的优先级更高
        headers = {**default_headers, **self.headers}
        
        # 发送请求
        response = session.request(
            method=self.method,
            url=url,
            headers=headers,
            data=self.body if self.body else None,
            proxies=self.proxies,
            verify=self.verify,
            allow_redirects=True
        )
        
        # 保存响应信息
        self.response_status_code = response.status_code
        self.response_status_reason = response.reason
        self.response_headers = dict(response.headers)
        self.response_body = response.text
        
        # 构建完整响应字符串
        protocol = 'HTTP/2' if response.raw.version == 2 else 'HTTP/1.1'
        status_line = f"{protocol} {self.response_status_code} {self.response_status_reason}"
        headers = '\n'.join(f"{k}: {v}" for k, v in self.response_headers.items())
        self.response = f"{status_line}\n{headers}\n\n{self.response_body}"
        
        return self.response

    def _build_full_url(self) -> str:
        """构建完整的请求URL，包含查询参数"""
        base_url = self.path
        if not base_url.startswith('http'):
            host = self.headers.get('Host', '')
            base_url = f'http://{host}{self.path}'
        
        # 如果有查询参数，添加到URL中
        if self.params:
            # 移除原有的查询参数（如果有）
            url_parts = base_url.split('?', 1)
            base_url = url_parts[0]
            # 将参数添加到URL
            query_string = urlencode(self.params, doseq=True)
            base_url = f"{base_url}?{query_string}"
            
        return base_url
    
    def set_params(self, params: Dict[str, Union[str, list]]) -> None:
        """设置URL查询参数
        
        Args:
            params: 参数字典，值可以是字符串或列表
        """
        # 确保所有的值都是列表形式
        self.params = {k: v if isinstance(v, list) else [v] for k, v in params.items()}
    
    def get_params(self) -> Dict[str, list]:
        """获取当前的URL查询参数
        
        Returns:
            Dict[str, list]: 当前的查询参数
        """
        return self.params
    
    def add_param(self, key: str, value: Union[str, list]) -> None:
        """添加单个查询参数
        
        Args:
            key: 参数名
            value: 参数值，可以是字符串或列表
        """
        if isinstance(value, list):
            self.params[key] = value
        else:
            self.params[key] = [value]


    def set_cookie(self, cookie_str: str) -> None:
        """设置Cookie，支持一个或多个cookie值
        
        Args:
            cookie_str: Cookie字符串，格式如 "name1=value1; name2=value2" 或 "name=value"
        """
        cookie_str = cookie_str.strip('\n')
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

    def parse_curl(self, curl_command: str) -> str:
        """解析curl命令并转换为HTTP请求，并返回原始请求字符串
        chrome-网络-复制-cURL(bash)
        
        Args:
            curl_command: curl命令字符串
            
        Returns:
            str: 原始HTTP请求字符串
        """
        # 移除开头的curl和结尾的引号（如果有）
        curl_command = curl_command.strip()
        if curl_command.startswith('curl '):
            curl_command = curl_command[5:]
        
        # 使用正则表达式解析参数
        url_match = re.search(r'["\']?(https?://[^"\']+)["\']?', curl_command)
        if url_match:
            url = url_match.group(1)
            parsed_url = urlparse(url)
            self.path = url
            self.headers['Host'] = parsed_url.netloc
            # 根据URL scheme设置协议
            self.protocol = 'HTTP/2' if parsed_url.scheme == 'https' else 'HTTP/1.1'
        
        # 解析请求方法
        method_match = re.search(r'-X\s+([A-Z]+)', curl_command)
        self.method = method_match.group(1) if method_match else 'GET'
        
        # 解析请求头
        header_matches = re.finditer(r'-H\s+["\']([^"\']+)["\']', curl_command)
        for match in header_matches:
            header = match.group(1)
            if ':' in header:
                key, value = header.split(':', 1)
                self.headers[key.strip()] = value.strip()
        
        # 解析请求体
        data_patterns = [
            r'--data\s+[\'"](.*?)[\'"](?:\s|$)',
            r'--data-raw\s+[\'"](.*?)[\'"](?:\s|$)',
            r'--data\s+(\{.*?\})(?:\s|$)',
            r'--data-raw\s+(\{.*?\})(?:\s|$)'
        ]
        
        for pattern in data_patterns:
            data_match = re.search(pattern, curl_command, re.DOTALL)
            if data_match:
                self.body = data_match.group(1)
                if 'Content-Type' not in self.headers:
                    self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
                # 如果没有指定方法，设置为 POST
                if not method_match:
                    self.method = 'POST'
                break
        
        # 设置默认协议
        self.protocol = 'HTTP/1.1'
        
        # 构建并返回原始请求字符串
        request_line = f'{self.method} {self.path} {self.protocol}'
        headers = '\n'.join(f'{k}: {v}' for k, v in self.headers.items())
        request = f'{request_line}\n{headers}'
        
        if self.body:
            request += f'\n\n{self.body}'
            
        return request

    def get_request_str(self) -> str:
        """返回完整的HTTP请求字符串，包含请求行、请求头和请求体
        
        Returns:
            str: 完整的HTTP请求字符串
        """
        # 构建请求行
        request_line = f'{self.method} {self.path} {self.protocol}'
        
        # 构建请求头
        headers = '\n'.join(f'{k}: {v}' for k, v in self.headers.items())
        
        # 组合请求字符串
        request = f'{request_line}\n{headers}'
        
        # 如果有请求体，添加空行和请求体
        if self.body:
            request += f'\n\n{self.body}'
        else:
            request += '\n\n'
            
        return request

    def get_request(self) -> requests.PreparedRequest:
        """返回一个已准备好的requests.PreparedRequest对象
        
        Returns:
            requests.PreparedRequest: 可以直接用session发送的请求对象
        """
        # 构建完整URL
        url = self._build_full_url()
            
        # 创建request对象
        req = requests.Request(
            method=self.method,
            url=url,
            headers=self.headers,
            data=self.body if self.body else None
        )
        
        # 准备请求
        session = requests.Session()
        session.verify = self.verify  # 设置session的verify属性
        prepared_req = session.prepare_request(req)
        
        return prepared_req