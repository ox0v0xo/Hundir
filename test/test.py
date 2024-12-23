import requests
from requests_toolbelt.utils import dump

url = "http://11.11.11.11:29000/minio/bootstrap/v1/verify"
headers = {"Content-Type": "application/x-www-form-urlencoded"}

response = requests.post(url, headers=headers, data={})
request = response.request

print(response.status_code)
print(response.headers)
print(response.text)

# print(request.method)  # 打印请求方法
# print(request.url)  # 打印请求URL
# print(request.headers)  # 打印请求头
# print(request.body)  # 打印请求体
