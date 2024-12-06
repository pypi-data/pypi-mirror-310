# File Manager for FastAPI

A plug-and-play solution for managing file uploads in FastAPI apps. It handles file uploads, saves them uniquely, and serves them via a static route automatically.
https://github.com/emeraldlinks/fastapiFileManager
## Installation

Install using pip:

```bash
pip install fastapiFileManager


#File manager for fastApi is designed to be a plug and play package to manage files in fastapi just like in django. you only need three line of code:

from fastapiFileManager import FileManager
file_manager = FileManager(app=app, base_path="uploads", route_path="/
files")

    file_url = file_manager.save_file(file)


## full example:



from fastapi import FastAPI, UploadFile
from fastapiFileManager import FileManager

app = FastAPI()

# Initialize FileManager
file_manager = FileManager(app=app, base_path="uploads", route_path="/files")

 
@app.post("/upload")
async def upload_file(file: UploadFile):
    # Save the file and get its URL
    file_url = file_manager.save_file(file)
    return {"file_url": file_url, "check as": f"localhost:8000/{file_url}"}


@app.get("/download/{filename}")
async def download_file(filename: str):
    # Serve the file for download
    return file_manager.serve_file(filename)



# file-manager
