#!/usr/bin/env python
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="turbosmsua-python3",
    packages=find_packages(),
    include_package_data=True,
    version="0.4.1",
    description="Client for https://turbosms.ua",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="Oleksii Orzeshkovskyi",
    author_email="al.orzh@gmail.com",
    url="https://github.com/aorzh/turbosmsua",
    keywords=["turbosmsua", "turbosms", "sms ua"],
    classifiers=[],
    install_requires=[
        "suds",
    ],
)
