import os
import sys

# 添加父目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from burphttp import burphttp

def main():
    # 从文件读取请求
    with open('test/proxy.http', 'r') as f:
        request_content = f.read()
    
    # 创建解析器实例
    bq = burphttp()
    bq.parse_request(request_content) # 解析请求从字符串
    # bq.parse_request_from_file("test/proxy.http") # 解析请求从文件
    bq.set_cookie("session=abc123; user=test; token=xyz789")# 设置cookie示例
    bq.set_proxy("http://127.0.0.1:7890") # 设置代理
    bq.save_response_body("test/response.json") #save response body to file
    bq.fixEncoding() #remove Accept-Encoding: gzip, deflate, br
    bq.send_request() #send request

    
    # 输出响应信息 
    print("full response:")
    print(bq.response)
    print("\nheaders:")
    print(bq.response_headers)
    print("\nbody:")
    print(bq.response_body)

if __name__ == "__main__":
    main()
