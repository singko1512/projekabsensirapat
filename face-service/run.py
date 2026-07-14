import os
from pathlib import Path

import uvicorn


BASE_DIR = Path(__file__).resolve().parent

os.environ.setdefault("TORCH_HOME", str(BASE_DIR / ".cache" / "torch"))
os.environ.setdefault("MPLCONFIGDIR", str(BASE_DIR / ".cache" / "matplotlib"))


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8001,
        reload=True,
    )
