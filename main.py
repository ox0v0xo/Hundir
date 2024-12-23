from src import banner
from src import parser
from src import check
from src import scan


def main():
    try:
        args = parser.parser()
        check.check(args)
        # banner.banner()
        scan.scan(args.url, args.timeout, args.threads)
    except Exception as e:
        print(f"发生错误: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("程序被用户中断")
    except SystemExit:
        raise
