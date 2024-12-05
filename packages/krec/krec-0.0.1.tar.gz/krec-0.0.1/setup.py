# mypy: disable-error-code="import-untyped"
#!/usr/bin/env python
"""Setup script for the project."""

import re

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description: str = f.read()


with open("krec/requirements.txt", "r", encoding="utf-8") as f:
    requirements: list[str] = f.read().splitlines()


with open("krec/requirements-dev.txt", "r", encoding="utf-8") as f:
    requirements_dev: list[str] = f.read().splitlines()


with open("krec/__init__.py", "r", encoding="utf-8") as fh:
    version_re = re.search(r"^__version__ = \"([^\"]*)\"", fh.read(), re.MULTILINE)
assert version_re is not None, "Could not find version in krec/__init__.py"
version: str = version_re.group(1)


setup(
    name="krec",
    version=version,
    description="The krec project",
    author="K-Scale Labs",
    url="https://github.com/kscalelabs/krec",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.11",
    install_requires=requirements,
    tests_require=requirements_dev,
    extras_require={"dev": requirements_dev},
    packages=["krec"],
    # entry_points={
    #     "console_scripts": [
    #         "krec.cli:main",
    #     ],
    # },
)
