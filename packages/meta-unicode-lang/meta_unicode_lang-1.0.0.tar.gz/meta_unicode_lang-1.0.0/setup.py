from setuptools import setup, find_packages

setup(
    name="meta_unicode_lang",
    version="1.0.0",
    description="Interpreter for META-Unicode[$∞$]Lang",
    author="MetaInfinity",
    author_email="support@metainfinity.example",
    packages=find_packages(),
    install_requires=[
        "fusepy",
        "pyqt5",
        "pygls"
    ],
    entry_points={
        "console_scripts": [
            "meta-lang=meta_unicode_lang.interpreter:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7"
)
