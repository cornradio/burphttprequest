# BurpHTTPRequest

一个简单易用的Python HTTP请求处理库，支持从文件读取请求、设置代理、保存响应等功能。


## 特性

- 从文件读取HTTP请求 包括 GET POST
- 支持设置HTTP代理
- 支持设置Cookie
- 支持保存响应内容到文件
- 支持移除压缩编码
- 支持解析curl(bash)请求（chrome 浏览器右键-复制请求）

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

# 从http字符串读取请求
request_content = open('req.http', 'r') .read()
bq.parse_request(request_content)

# 从curl 字符串命令读取请求
request_content = open('curlcommand.txt', 'r') .read()
bq.parse_curl(request_content)

# 设置代理（可选）
bq.set_proxy("http://127.0.0.1:8080")

# 设置Cookie（可选）
bq.set_cookie("session=abc123; user=test; phpsessionid=123456")

# 设置host（可选）
bq.set_host("www.baidu.com")

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

可以用火狐浏览器获取原始请求

![image](https://i.imgur.com/gwulP4w.png)

如果你不确定自己的请求体是否可用，可以借助这个vscode插件： 
https://marketplace.visualstudio.com/items?itemName=humao.rest-client

## curl命令解析模式

curl命令解析模式支持chrome浏览器右键-复制请求 curl(bash)


![image](https://i.imgur.com/ueef3K4.png)

推荐一个网站，可以解析curl命令到http请求：
https://curlconverter.com/http/

## 更新日志

- v0.1.4 2025-01-13 支持设置host
- v0.1.6 2025-01-14 支持解析curl(bash)请求 
- v0.1.7 2025-01-15 修复了https时候的cookie消失问题
