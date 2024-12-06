import os
import uuid
from fastapi import HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


class FileManager:
    def __init__(self, app, base_path: str = "uploads", route_path: str = "/files"):
        """
        FileManager class for handling file uploads in FastAPI.

        Args:
            app: FastAPI application instance.
            base_path (str): The directory where files will be stored.
            route_path (str): The route to serve uploaded files.
        """
        self.base_path = base_path
        self.route_path = route_path

        # Ensure the upload directory exists
        os.makedirs(self.base_path, exist_ok=True)

        # Add static file route for serving files
        app.mount(self.route_path, StaticFiles(directory=self.base_path), name="uploads")

    def save_file(self, file):
        """
        Save an uploaded file to the upload directory.

        Args:
            file: The uploaded file (an instance of UploadFile).

        Returns:
            str: The URL of the saved file.
        """
        if not file.filename:
            raise HTTPException(status_code=400, detail="Invalid file")

        # Generate a unique filename
        file_extension = os.path.splitext(file.filename)[-1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(self.base_path, unique_filename)

        # Save the file to the disk
        with open(file_path, "wb") as f:
            f.write(file.file.read())

        # Return the file URL
        file_url = f"{self.route_path}/{unique_filename}"
        return file_url

    def get_file_path(self, filename: str):
        """
        Get the absolute file path of a saved file.

        Args:
            filename (str): The name of the file.

        Returns:
            str: The absolute file path.
        """
        file_path = os.path.join(self.base_path, filename)
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        return file_path

    def serve_file(self, filename: str):
        """
        Serve a specific file as a response.

        Args:
            filename (str): The name of the file to serve.

        Returns:
            FileResponse: The file response.
        """
        file_path = self.get_file_path(filename)
        return FileResponse(file_path)
