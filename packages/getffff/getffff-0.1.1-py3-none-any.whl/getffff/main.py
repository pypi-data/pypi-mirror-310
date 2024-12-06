import subprocess

def run():
    """Execute the `cat /flag` command securely."""
    try:
        result = subprocess.run(["cat", "/flag"], text=True, capture_output=True, check=True)
        print(result.stdout)  # 명령의 출력 표시
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
