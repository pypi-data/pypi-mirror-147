import os
from codecs import open
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

os.chdir(here)

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

with open(os.path.join(here, "VERSION"), encoding="utf-8") as f:
    version = f.read()

setup(
    name="elements-pay",
    version=version,
    description="The Elements Pay Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Elements",
    packages=find_packages(exclude=["tests"]),
    package_data={"elements": ["certs/cacert.pem"]},
    install_requires=[
        'requests >= 2.20; python_version >= "3.0"',
        'requests[security] >= 2.20; python_version < "3.0"',
    ],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
)
