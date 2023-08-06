import setuptools
from setuptools import find_packages

setuptools.setup(
    name = "git-rebase-chain",
    packages = find_packages(),
    version = "0.1.0",
    long_description = open("README.md", "r").read(),
    entry_points = {
        "console_scripts": [
            "git-rebase-chain=git_rebase_chain.cmd:main"
        ]
    }
)