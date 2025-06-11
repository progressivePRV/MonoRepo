'''
Phase 1: 
Use Fast API APP for creating Endponits to 
- List Files in a Folder
    List endpoint should read file name from path, and should validate there should not be any script or "." or ".." in path
- Get File
    get file should should show file if less than 25mb or download it.
- Upload File
    Upload file should read path form url path to upload.
- (No Delete yet, we don't want to delete files accidently)
'''

import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

DEFAULT_PATH = "."
NOT_ALLOWED_CHARACTERS = [".","..",":"]
# here path is a required query parameter
@app.get("/listFiles")
async def list_files(path: str = ""):
    # validations
    if [char for char in NOT_ALLOWED_CHARACTERS if char in path]:
        raise HTTPException(status_code=400, detail=f"{NOT_ALLOWED_CHARACTERS} character are not allowed in path quert parameter")
    file_or_folders = []
    full_path = os.path.join(DEFAULT_PATH, path)
    with os.scandir(full_path) as it:
        for entry in it:
                file_or_folders.append({"name":entry.name, "is_file":entry.is_file()})
    return {"path":path, "file_or_folders":file_or_folders}

# get files
# fastApis's static files support recursive files serving
# "Files" here is path where additional/other app "FilerServer" is mounted
# Note:- this APP will not show up in docs, and Files is case sensitive
app.mount("/Files", StaticFiles(directory="."), name="FilerServer")
# example: http://127.0.0.1:8000/Files/uploads/images/SampleJPGImage_5mbmb.jpg