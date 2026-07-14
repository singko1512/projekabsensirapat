from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.services.face_recognition import enroll_face, recognize_face
from app.services.liveness import check_liveness


app = FastAPI(title="Face Service")
BASE_DIR = Path(__file__).resolve().parent
CAMERA_PAGE = BASE_DIR / "static" / "camera.html"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def index():
    return {
        "status": "ok",
        "service": "face-service",
        "type": "api",
        "docs": "/docs",
        "health": "/health",
        "camera_test": "/camera",
    }


@app.get("/camera")
def camera():
    return FileResponse(CAMERA_PAGE)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "face-service",
    }


@app.post("/enroll")
async def enroll(user_id: str = Form(...), image: UploadFile = File(...)):
    image_bytes = await image.read()

    liveness_result = check_liveness(image_bytes)
    if not liveness_result["is_live"]:
        return {
            "success": False,
            "reason": "liveness_failed",
            "liveness": liveness_result,
        }

    enrollment_result = enroll_face(user_id=user_id, image_bytes=image_bytes)

    return {
        "success": enrollment_result["enrolled"],
        "liveness": liveness_result,
        "enrollment": enrollment_result,
    }


@app.post("/recognize")
async def recognize(image: UploadFile = File(...), threshold: float = Form(0.35)):
    image_bytes = await image.read()

    liveness_result = check_liveness(image_bytes)
    if not liveness_result["is_live"]:
        return {
            "success": False,
            "reason": "liveness_failed",
            "liveness": liveness_result,
        }

    recognition_result = recognize_face(image_bytes, threshold=threshold)

    return {
        "success": recognition_result["matched"],
        "liveness": liveness_result,
        "recognition": recognition_result,
    }
