from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import requests
import yaml
import re


def scan(url, timeout, threads):
    template_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "templates")
    )
    futures = []
    with ThreadPoolExecutor(max_workers=1) as executor:
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
    path = data["Request"].get("path", "")
    headers = data["Request"].get("headers", {})
    body = data["Request"].get("body", "")
    request_url = url + str(path)

    try:
        response = requests.request(
            method=method,
            url=request_url,
            headers=headers,
            data=body,
            timeout=timeout / 1000,
        )
        if analyze_response(response, data["Response"]):
            print(f"[+] 包含漏洞{data['Info']['name']}")
    except requests.RequestException as e:
        print(f"请求错误: {e}")


def analyze_status_code(response: requests.Response, codes, condition):
    if condition == "and":
        return all(status == response.status_code for status in codes)
    elif condition == "or":
        return any(status == response.status_code for status in codes)


def analyze_words(response: requests.Response, words, part, condition):
    if part == "body":
        text = response.text
    elif part == "header":  # 字典转换为字符串进行匹配验证
        text = " ".join(str(value) for value in response.headers.values())

    if condition == "and":
        return all(word in text for word in words)
    elif condition == "or":
        return any(word in text for word in words)


def analyze_regex(response: requests.Response, regexes, part, condition):
    if part == "body":
        text = response.text
    elif part == "header":
        text = " ".join(str(value) for value in response.headers.values())

    if condition == "and":
        return all(re.search(regex, text) for regex in regexes)
    elif condition == "or":
        return any(re.search(regex, text) for regex in regexes)


def analyze_response(response: requests.Response, response_rules) -> bool:
    # print(response.status_code)
    # print(response.headers)
    # print(response.text)
    for rule in response_rules:
        condition = rule.get("condition", "and")
        match_part = rule.get("part", "body")

        if rule["type"] == "status":
            if not analyze_status_code(response, rule["code"], condition):
                return False

        elif rule["type"] == "word":
            if not analyze_words(response, rule["words"], match_part, condition):
                return False

        elif rule["type"] == "regex":
            if not analyze_regex(response, rule["regex"], match_part, condition):
                return False

    return True
