import os
from setuptools import setup, find_packages

long_description = ""
try:
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Meta Unicode Language Framework"

setup(
    name="meta_unicode_lang",
    version="1.0.1",
    description="Meta Unicode Language Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Pu Justin Scarfy Yang",
    author_email="pujustinscarfyyang@icloud.com",
    license="MIT",
    license_files=["LICENSE.txt"],  # Ensure LICENSE.txt is included
    packages=find_packages(),
    install_requires=[
        "fusepy",
        "pyqt5",
        "pygls"
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7",
    include_package_data=True,
)
