import os

from setuptools import find_packages, setup

REQUIREMENTS = ["grpcio", "protobuf>=3.19.0"]

setup(
    name="dialga-api",
    version=os.getenv("VERSION", "0.0.1"),
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
)
