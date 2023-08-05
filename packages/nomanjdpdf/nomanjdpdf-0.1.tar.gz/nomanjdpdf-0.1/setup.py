import setuptools
from pathlib import Path

setuptools.setup(
    name="nomanjdpdf",
    version=0.1,
    long_description=Path("README.md").read_text(),
    packages=setuptools.setuptools.find_packages(exclude=["tests", "data"]),
)
