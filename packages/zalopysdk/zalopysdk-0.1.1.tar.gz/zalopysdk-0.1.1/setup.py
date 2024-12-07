import os
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="zalopysdk",
    version=os.getenv("VERSION", "0.1.0"),
    author="Giã Dương Đức Minh",
    author_email="giaduongducminh@gmail.com",
    description="A Python SDK for Zalo API integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ducminhgd/zalo-python-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pkce==1.0.3",
        "requests==2.32.3",
    ],
)
