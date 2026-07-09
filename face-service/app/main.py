from fastapi import FastAPI, UploadFile, File

from app.services.face_recognition import recognize_face
from app.services.liveness import check_liveness


app = FastAPI(title="Face Service")


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "face-service",
    }


@app.post("/recognize")
async def recognize(image: UploadFile = File(...)):
    image_bytes = await image.read()

    liveness_result = check_liveness(image_bytes)
    if not liveness_result["is_live"]:
        return {
            "success": False,
            "reason": "liveness_failed",
            "liveness": liveness_result,
        }

    recognition_result = recognize_face(image_bytes)

    return {
        "success": recognition_result["matched"],
        "liveness": liveness_result,
        "recognition": recognition_result,
    }

