import setuptools
from os import path

with open("README.md", "r") as fh:
    long_description = fh.read()

# extract version
path = path.realpath("pyjavaz/_version.py")
version_ns = {}
with open(path, encoding="utf8") as f:
    exec(f.read(), {}, version_ns)
version = version_ns["__version__"]

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="pyjavaz",
    version=version,
    author="Henry Pinkard",
    author_email="henry.pinkard@gmail.com",
    description="Python remote procedure call of Java using ZeroMQ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pyjavaz/pyjavaz",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    python_requires=">=3.6",
    extras_require={
        "dev": [
 
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
)
