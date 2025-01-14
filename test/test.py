from burphttp import burphttp


with open('curlcommand.txt', 'r') as f:
    request_content = f.read()

# 创建解析器实例
bq = burphttp()
print(bq.parse_curl(request_content))
bq.send_request()
bq.save_response_body("response.http")
