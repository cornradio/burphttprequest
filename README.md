# BurpHTTPRequest

一个简单易用的Python HTTP请求处理库，支持从文件读取请求、设置代理、保存响应等功能。


## 特性

- 从文件读取HTTP请求 包括 GET POST
- 支持设置HTTP代理
- 支持设置Cookie
- 支持保存响应内容到文件
- 支持移除压缩编码

## 使用示例
更多实例见 [test/main.py](test/main.py)

```bash
pip install burphttp
```


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

可以用火狐浏览器获取原始请求
GET: 
- 右键-复制请求头（Q）
POST:
- 右键-复制请求头（Q）
- 手动起一个空行
- 右键-复制Post数据

![image](https://github.com/user-attachments/assets/088cd298-9886-4756-982a-aa206ba57025)

如果你不确定自己的请求体是否可用，可以借助这个vscode插件： 
https://marketplace.visualstudio.com/items?itemName=humao.rest-client


## 许可证

MIT License
