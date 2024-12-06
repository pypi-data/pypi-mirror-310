import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="x23340355_aws_service_pkg",
    version="0.0.2",
    author="MinKo",
    author_email=" x23340355@student.ncirl.ie",
    description="A python library which interact with AWS services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/minkoaung89/homeconnect-v3",
    packages=setuptools.find_packages(),
    install_requires=[''],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    )