from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name = "RAG-ChatBot",
    version = "0.1",
    author = "Amaithi",
    packages = find_packages(),
    requires = requirements
)