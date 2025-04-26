# ------------- iter 1
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

FILES_DIRECTORY = "uploads"
STATIC_DIRECTORY = "static"

# Ensure the directory for uploaded files exists
os.makedirs(FILES_DIRECTORY, exist_ok=True)
os.makedirs(STATIC_DIRECTORY, exist_ok=True)

# Mount the static files directory
app.mount("/static", StaticFiles(directory=STATIC_DIRECTORY, html=True), name="static")

@app.get("/")
async def read_index():
    return FileResponse('./static/index.html')

@app.post("/upload/{folder_path}")
async def upload_file(folder_path, files: list[UploadFile]):
    for file in files:
        file_path = os.path.join(FILES_DIRECTORY, folder_path, file.filename)
        with open(file_path, "wb") as f:
            f.write(file.file.read())
    return {"filenames": [file.filename for file in files]}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(FILES_DIRECTORY, filename)
    return FileResponse(path=file_path, filename=filename)

@app.get("/storage/")
@app.get("/storage/{folder_or_file_path}")
async def list_files_in_folder(folder_or_file_path: str = ""):
    invalid_chars = {"..", "("}  # Need valdaition to hacker and monkey user
    if any(char in folder_or_file_path for char in invalid_chars):
        print("validation failed")
        return {"error": "Folder not found"}
    folder_or_file_path = os.path.join(FILES_DIRECTORY, folder_or_file_path)
    if os.path.exists(folder_or_file_path):
        if os.path.isdir(folder_or_file_path):
            files = {}
            with os.scandir(folder_or_file_path) as entries:
                for entry in entries:
                    if entry.is_file():
                        files[entry.name] = "file"
                    elif entry.is_dir():
                        files[entry.name] = "folder"
            return files
        else:
            return FileResponse(folder_or_file_path)     
    else:
        return {"error": "Folder or file not found"}
    
@app.get("/file")
async def get_file(file_path: str):
    invalid_chars = {"..", "("}  # Need valdaition to hacker and monkey user
    if any(char in file_path for char in invalid_chars):
        print("validation failed")
        return {"error": "Folder not found"}
    file_path = os.path.join(FILES_DIRECTORY, file_path[1:])  # [1:] for removing leading /
    print("file_path=",file_path)
    if os.path.exists(file_path):
        return FileResponse(file_path)     
    else:
        return {"error": "file not found"}


# @app.delete("/delete/{filename}")
# async def delete_file(filename: str):
#     file_path = os.path.join(FILES_DIRECTORY, filename)
#     if os.path.exists(file_path):
#         os.remove(file_path)
#         return {"message": f"{filename} deleted successfully"}
#     else:
#         return {"error": "File not found"}
