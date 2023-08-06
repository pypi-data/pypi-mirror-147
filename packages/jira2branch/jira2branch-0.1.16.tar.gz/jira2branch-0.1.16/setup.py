import pathlib

from setuptools import find_packages
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="jira2branch",
    version="0.1.16",
    description="Takes a JIRA issue and creates a git branch",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Tiago Pereira",
    author_email="tiago.pereira@infraspeak.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=[
        "click",
        "jira",
        "halo",
        "unidecode",
        "GitPython",
        "python-gitlab"
    ],
    entry_points={
        "console_scripts": [
            "jira2branch=jira2branch.__main__:cli",
        ]
    },
)
