# BurpHTTPRequest

一个简单易用的Python HTTP请求处理库，支持从文件读取请求、设置代理、保存响应等功能。

## 安装

```bash
pip install burphttprequest
```

## 特性

- 从文件读取HTTP请求
- 支持设置HTTP代理
- 支持设置Cookie
- 自动处理响应编码
- 支持保存响应内容到文件
- 支持移除压缩编码

## 使用示例
更多实例见 [test/main.py](test/main.py)

```python
from burphttp import burphttp

# 创建实例
bq = burphttp()

# 从文件读取请求
bq.parse_request_from_file("request.http")

# 设置代理（可选）
bq.set_proxy("http://127.0.0.1:8080")

# 设置Cookie（可选）
bq.set_cookie("session=abc123; user=test")

# 移除压缩编码（可选）
bq.fixEncoding()

# 发送请求
bq.send_request()

# 保存响应体到文件
bq.save_response_body("response.txt")

# 打印响应信息
print(bq.response_status_code)  # 状态码
print(bq.response_headers)      # 响应头
print(bq.response_body)         # 响应体
```

## HTTP请求文件格式

请求文件格式示例：

```http
POST /api/test HTTP/1.1
Host: example.com
Content-Type: application/json

{"key": "value"}
```

## 许可证

MIT License
