from setuptools import setup, find_packages
import pathlib
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")
setup(
    name="snapshot",packages=find_packages(),python_requires=">=3.7, <4")