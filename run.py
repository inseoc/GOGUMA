import subprocess
import os
import sys
from pathlib import Path

# 프로젝트 루트 디렉토리 설정
ROOT_DIR = Path(__file__).parent

def run_backend():
    backend_dir = ROOT_DIR / "backend" / "app"
    os.chdir(backend_dir)
    return subprocess.Popen([sys.executable, "-m", "uvicorn", "backend:app", "--reload"])

def run_frontend():
    frontend_dir = ROOT_DIR / "frontend"
    os.chdir(frontend_dir)
    # npm의 전체 경로를 지정합니다.
    npm_path = r"C:/Program Files/nodejs/npm.cmd"  # 이 경로는 실제 npm 설치 위치에 따라 다를 수 있습니다.
    return subprocess.Popen([npm_path, "start"], shell=True)

if __name__ == "__main__":
    print("Starting servers...")
    
    backend_process = run_backend()
    frontend_process = run_frontend()
    
    try:
        # 두 프로세스가 종료될 때까지 대기
        backend_process.wait()
        frontend_process.wait()
    except KeyboardInterrupt:
        print("Stopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
    
    print("Servers stopped.")