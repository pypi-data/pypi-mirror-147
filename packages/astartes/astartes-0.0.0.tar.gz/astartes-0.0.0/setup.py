import os.path
import codecs
import pathlib
from setuptools import setup, find_packages


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


# The directory containing this file
cwd = pathlib.Path(__file__).parent

# The text of the README file
README = (cwd / "README.md").read_text()

setup(
    name="astartes",
    version=get_version("extended_train_test_split/__init__.py"),
    description="Algorithmic train:test splitting for molecules, images, and arbitrary arrays.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/JacksonBurns/extended_train_test_split",
    author="Jackson Burns",
    author_email="jburnsky@udel.edu",
    license="MIT",
    classifiers=["Programming Language :: Python :: 3"],
    install_requires=read("requirements.txt").split("\n"),
    packages=find_packages(),
    include_package_data=True,
)
