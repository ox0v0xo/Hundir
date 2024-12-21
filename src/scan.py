from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import random
import requests
import yaml


def scan(url, timeout, threads):
    template_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "templates")
    )
    futures = []
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for filename in os.listdir(template_dir):
            if filename.endswith((".yaml", ".yml")):
                filepath = os.path.join(template_dir, filename)
                with open(filepath, "r") as stream:
                    try:
                        data = yaml.safe_load(stream)
                        futures.append(
                            executor.submit(send_request, data, url, timeout)
                        )
                    except yaml.YAMLError as exc:
                        print(exc)

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"线程中发生错误: {e}")


def send_request(data, url, timeout):
    method = data["Request"]["method"]
    path = data["Request"]["path"]
    headers = data["Request"]["headers"]
    request_url = url + path

    try:
        response = requests.request(
            method, request_url, headers=headers, timeout=timeout / 1000
        )
        # 分析响应
        if analyze_response(response, data["Response"]):
            print(f"包含漏洞{data['Info']['name']}")
    except requests.RequestException as e:
        print(f"请求错误: {e}")


def analyze_response(response, response_rules) -> bool:
    for rule in response_rules:
        condition = rule.get("condition", "and")

        if rule["type"] == "status":
            if condition == "and":
                if not all(status == response.status_code for status in rule["code"]):
                    return False
            elif condition == "or":
                if not any(status == response.status_code for status in rule["code"]):
                    return False

        elif rule["type"] == "word":
            part = rule["part"]
            words = rule["words"]
            if condition == "or":
                if part == "body" and all(word not in response.text for word in words):
                    return False
                elif part == "header" and all(
                    word not in response.headers.get("Content-Type", "")
                    for word in words
                ):
                    return False
            elif condition == "and":
                if part == "body" and not all(word in response.text for word in words):
                    return False
                elif part == "header" and not all(
                    word in response.headers.get("Content-Type", "") for word in words
                ):
                    return False

    return True
