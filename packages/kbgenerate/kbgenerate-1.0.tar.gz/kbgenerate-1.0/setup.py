import setuptools
from pathlib import Path

setuptools.setup(
    name="kbgenerate",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages()
    # here we can include excludes to include an array of files or packages to exclude
)
