#!/usr/bin/env python3

import setuptools

with open("./README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("./src/genascii/about.py", encoding="utf-8") as f:
    about = {}
    exec(f.read(), about)

setuptools.setup(
    name="genascii",
    version=about["__version__"],
    author="brightsunshine0917",
    author_email="tanloong@foxmail.com",
    url="https://github.com/tanloong/pytregex",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    description="Python implementation of Stanford Tregex",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    entry_points={"console_scripts": ["pytregex = pytregex:main"]},
)
