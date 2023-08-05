from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="passgr",
    version="0.0.1",
    author="davi h.",
    author_email="davi.henrique.lima01@gmail.com",
    description="A simple password generator",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Davi-dev-C/simple-package-template",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)