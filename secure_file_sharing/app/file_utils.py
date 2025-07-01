import os
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {"pptx", "xlsx", "docx"}
UPLOAD_DIR = "uploads"

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

async def save_file(file: UploadFile):
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type")
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as out_file:
        content = await file.read()
        out_file.write(content)
    return file_path