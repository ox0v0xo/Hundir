import argparse
import socket
import sys
from urllib.parse import urlparse


def check_url(url: str) -> str:
    parse_url = urlparse(url)
    if not parse_url.scheme:
        return "http://" + url
    return url


def check_network() -> bool:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(("www.baidu.com", 80))
        sock.close()
        return True
    except OSError:
        return False
    finally:
        if "sock" in locals() and sock:
            sock.close()


def check_arg(args: argparse.Namespace) -> bool:
    if not args.url:
        print("错误: 未提供URL。")
        return False
    args.url = check_url(args.url)
    if args.threads <= 0:
        print("错误: 线程数必须大于0。")
        return False
    if args.timeout <= 0:
        print("错误: 超时时间必须大于0。")
        return False
    return True


def check(args: argparse.Namespace) -> None:
    if not check_network():
        print("网络连接失败，程序终止。")
        sys.exit(1)
    if not check_arg(args):
        sys.exit(1)
