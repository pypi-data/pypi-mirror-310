import os

from setuptools import setup

VERSION = "0.1-beta.7"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="activity.py",
    description="null",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Brenton Cleeland",
    url="https://github.com/sesh/activity.py",
    project_urls={
        "Issues": "https://github.com/sesh/activity.py/issues",
        "CI": "https://github.com/sesh/activity.py/actions",
        "Changelog": "https://github.com/sesh/activity.py/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["activity_py"],
    install_requires=["fitparse==1.2.0", "python-dateutil<2.9", "defusedxml==0.7.1"],
    extras_require={"test": ["pytest"]},
    python_requires=">=3.7",
)
