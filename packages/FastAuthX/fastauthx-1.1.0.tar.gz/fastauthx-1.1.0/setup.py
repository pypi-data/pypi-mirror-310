from setuptools import setup, find_packages

setup(
    name="FastAuthX",
    version="1.1.0",
    author="Joseph Christopher",
    author_email="joechristophersc@gmail.com",
    description="A plug-and-play authentication system for FastAPI.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/emeraldlinks/FastAuthX",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "sqlalchemy",
        "sqlmodel",
        "passlib[bcrypt]",
        "python-jose",
        "uvicorn",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Framework :: FastAPI",
        "License :: OSI Approved :: MIT License",
    ],
)
