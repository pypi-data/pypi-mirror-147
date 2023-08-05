import pathlib
from setuptools import setup
import setuptools

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="pytnu",
    version="1.0.1",
    description="An easy text-menu creation interface",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/kYpranite/pytnu",
    author="Ethan Huang",
    author_email="ethanhuang2078@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    packages=setuptools.find_packages(where="src", exclude=("tests",)),
    include_package_data=True,
)
