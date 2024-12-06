
from setuptools import setup, find_packages

setup(
    name="fastapiFileManager",
    version="1.1.1",
    description="A plug-and-play file management package for FastAPI.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Joseph Christopher",
    author_email="joechristophersc@gmail.com",
    url="https://github.com/emeraldlinks/file-manager",
    packages=find_packages(),
    install_requires=["fastapi", "uvicorn"],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Framework :: FastAPI",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
