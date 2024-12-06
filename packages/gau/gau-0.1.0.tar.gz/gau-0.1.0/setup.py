import os
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="gau",
    version=os.getenv("VERSION", "0.0.1"),
    author="Gia Duong Duc Minh",
    author_email="giaduongducminh@gmail.com",
    description="A Python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ducminhgd/gau",
    packages=find_packages(),
    package_dir={
        'gau': 'gau',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    tests_require=['pytest'],
)
