import argparse


def parser() -> argparse.Namespace:
    parser_ = argparse.ArgumentParser(description="HELP")
    parser_.add_argument("-u", type=str, dest="url", help="目标URL")
    parser_.add_argument(
        "-T", dest="threads", type=int, default=500, help="线程数, 默认500"
    )
    parser_.add_argument(
        "-t", dest="timeout", type=int, default=5000, help="超时时间(ms), 默认 5000ms"
    )
    try:
        args = parser_.parse_args()
        return args
    except Exception as e:
        parser_.error(str(e))
