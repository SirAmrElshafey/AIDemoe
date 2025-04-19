from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os
import uuid
from deepSeek_halal import process_image_with_deepseek

app = FastAPI()


# --- FastAPI Endpoint ---
@app.post("/process-pdf")
async def process_pdf(file: UploadFile = File(...)):
    temp_filename = f"./tmp/{uuid.uuid4()}.pdf"
    print(f"Received file: {file.filename}")
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        print(f"Received file: {temp_filename}")
        result = process_image_with_deepseek(temp_filename)
        return JSONResponse(content=result)
    finally:
        os.remove(temp_filename)
