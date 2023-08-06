from setuptools import setup, find_packages

PACKAGE = "axesdnSDK"
NAME = "axesdn_sdk"
DESCRIPTION = "AXESDN SDK Library for Python"
AUTHOR = "AXESDN DEV Team"
AUTHOR_EMAIL = "devops@axesdn.com"
VERSION = __import__(PACKAGE).__version__
LICENSE = "Apache License 2.0"
REQUIRES = [
    "requests>=2.26.0"
]

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license=LICENSE,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development"
    ],
    python_requires='>=3.7',
    install_requires=REQUIRES
)
