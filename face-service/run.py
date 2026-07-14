import argparse
import os
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
VENV_PYTHON = BASE_DIR / "venv" / "Scripts" / "python.exe"


def relaunch_with_venv() -> int | None:
    if VENV_PYTHON.exists() and Path(sys.executable).resolve() != VENV_PYTHON.resolve():
        completed = subprocess.run(
            [str(VENV_PYTHON), str(Path(__file__).resolve()), *sys.argv[1:]],
            check=False,
        )
        return completed.returncode

    return None


def configure_environment() -> None:
    os.chdir(BASE_DIR)
    (BASE_DIR / ".cache" / "torch").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / ".cache" / "matplotlib").mkdir(parents=True, exist_ok=True)
    (BASE_DIR / "embeddings").mkdir(parents=True, exist_ok=True)

    os.environ.setdefault("TORCH_HOME", str(BASE_DIR / ".cache" / "torch"))
    os.environ.setdefault("MPLCONFIGDIR", str(BASE_DIR / ".cache" / "matplotlib"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the face-service API.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8001)
    parser.add_argument("--no-reload", action="store_true", help="Disable auto reload.")
    return parser.parse_args()


def main() -> int:
    relaunch_result = relaunch_with_venv()
    if relaunch_result is not None:
        return relaunch_result

    configure_environment()
    args = parse_args()

    try:
        import uvicorn
    except ModuleNotFoundError:
        print("Dependency belum terinstall.")
        print("Jalankan dari folder face-service:")
        print("  python -m venv venv")
        print("  .\\venv\\Scripts\\python.exe -m pip install -r requirements.txt")
        return 1

    url = f"http://{args.host}:{args.port}"
    print(f"Face Service jalan di {url}")
    print(f"Buka kamera: {url}/camera")
    print("Stop server: Ctrl+C")

    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.port,
        reload=not args.no_reload,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
