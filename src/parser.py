import argparse


def parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HELP")
    parser.add_argument("-u", type=str, dest="url", help="目标URL")
    parser.add_argument(
        "-T", dest="threads", type=int, default=5000, help="线程数, 默认5000"
    )
    parser.add_argument(
        "-t", dest="timeout", type=int, default=5000, help="超时时间(ms), 默认 5000ms"
    )
    try:
        args = parser.parse_args()
        return args
    except Exception as e:
        parser.error(str(e))
