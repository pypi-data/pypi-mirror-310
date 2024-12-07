from setuptools import setup, find_packages

setup(
    name="exn-booking-sdk",
    version="0.1.2",
    description="SDK for interacting with Booking Service",
    author="Ryan",
    author_email="ryan@exnodes.vn",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
