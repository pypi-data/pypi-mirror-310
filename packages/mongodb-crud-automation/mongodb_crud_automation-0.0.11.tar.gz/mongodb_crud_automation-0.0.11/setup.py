from setuptools import setup, find_packages
from typing import List

with open("README.md", "r") as fh:
    long_description = fh.read()

__version__ = "0.0.11"
REPO_NAME = "mongodbconnectorpkg"
PKG_NAME= "mongodb_crud_automation"
AUTHOR_USER_NAME = "Minali0"
AUTHOR_EMAIL = "minali.jain@seaflux.tech"

setup(
    name=PKG_NAME,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="CRUD operations for MongoDB",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    )
