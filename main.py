from enum import IntEnum

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import Response
import cv2
import numpy as np

app = FastAPI()

MAX_UPLOAD_BYTES = 20 * 1024 * 1024

class Rotation(IntEnum):
    CLOCKWISE_90 = cv2.ROTATE_90_CLOCKWISE  # 0
    ROTATE_180 = cv2.ROTATE_180  # 1
    COUNTERCLOCKWISE_90 = cv2.ROTATE_90_COUNTERCLOCKWISE  # 2


def decode_upload(file: UploadFile) -> np.ndarray:
    img_content = file.file.read(MAX_UPLOAD_BYTES + 1)
    if len(img_content) > MAX_UPLOAD_BYTES:
        raise HTTPException(413, "Image too large")

    np_array = np.frombuffer(img_content, np.uint8)
    # IMREAD_UNCHANGED keeps the alpha channel of transparent PNGs
    img = cv2.imdecode(np_array, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise HTTPException(400, "Could not convert image to opencv format")
    return img


def png_response(img: np.ndarray) -> Response:
    ok, encoded_img = cv2.imencode(".png", img)
    if not ok:
        raise HTTPException(500, "Could not encode image")
    return Response(content=encoded_img.tobytes(), media_type="image/png")


@app.get("/health-check", status_code=200)
async def health_check():
    return {
            "message" : "Running"
    }

# Sync (def) endpoints run in a threadpool, so the OpenCV work doesn't block the event loop
@app.post("/crop", response_class=Response)
def crop(
    file: UploadFile = File(...),
    x_start: int = Form(..., ge=0),
    x_end: int = Form(..., gt=0),
    y_start: int = Form(..., ge=0),
    y_end: int = Form(..., gt=0),
):
    img = decode_upload(file)
    height, width = img.shape[:2]

    if not (x_start < x_end <= width and y_start < y_end <= height):
        raise HTTPException(
            400,
            f"Invalid crop region for a {width}x{height} image: "
            "need 0 <= start < end <= image size",
        )

    return png_response(img[y_start:y_end, x_start:x_end])

@app.post("/rotate", response_class=Response)
def rotate(
    file: UploadFile = File(...),
    rotation: Rotation = Form(...),
):
    img = decode_upload(file)
    return png_response(cv2.rotate(img, rotation))
