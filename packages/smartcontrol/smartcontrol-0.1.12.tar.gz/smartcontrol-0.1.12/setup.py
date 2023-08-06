from setuptools import setup, find_packages
import os, re

with open("README.md") as readme_file:
    README = readme_file.read()

version = (
    re.findall(r"[0-9]+.[0-9]+.[0-9]+", os.environ["GITHUB_REF"])[0]
    if "GITHUB_REF" in os.environ
    else "0.0.0"
)
setup_args = dict(
    name="smartcontrol",
    version=version,
    description="Useful tools to make an automated actions script ",
    long_description_content_type="text/markdown",
    long_description=README,
    license="MIT",
    packages=["smartcontrol"],
    author="Badreddine bencherki",
    author_email="badrbencherki@gmail.com",
    keywords=[
        "bot",
        "control",
        "clock",
        "timer",
    ],
    url="https://github.com/badre2dine/smartcontrol",
    download_url="https://pypi.org/project/smartcontrol/",
)

install_requires = []

if __name__ == "__main__":
    setup(**setup_args, install_requires=install_requires)
