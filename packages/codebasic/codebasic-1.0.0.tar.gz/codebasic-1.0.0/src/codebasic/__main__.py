import sys
from .cli import main, print_banner

if __name__ == "__main__":
    try:
        print_banner()  # 배너 출력
        main()  # CLI 실행
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)