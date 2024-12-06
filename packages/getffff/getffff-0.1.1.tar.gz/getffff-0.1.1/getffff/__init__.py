import argparse
from getffff.main import run  # main.py의 run 함수 가져오기

def main():
    """Parse command-line arguments and execute the appropriate function."""
    parser = argparse.ArgumentParser(description="A tool to get the flag.")
    parser.add_argument(
        "command",
        choices=["run"],
        help="Command to execute. Use 'run' to execute 'cat /flag'."
    )
    args = parser.parse_args()

    if args.command == "run":
        run()
