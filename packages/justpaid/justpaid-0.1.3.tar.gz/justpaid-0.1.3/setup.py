from setuptools import setup, find_packages
import os

version = {}
with open(os.path.join("src", "justpaid", "_version.py")) as f:
    exec(f.read(), version)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="justpaid",
    version=version["__version__"],
    author="JustPaid Development",
    author_email="engineering@justpaid.io",
    description="A Python SDK for the JustPaid API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/loopfour/justpaid-python-sdk",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
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
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=1.8.0",
    ],
)
