from setuptools import setup, find_packages
import os

setup(
    name="lemmo-apps",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="2MCorp",
    author_email="your.email@example.com",
    description="A short description of your lemmo-apps project",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/lemmo-apps",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
