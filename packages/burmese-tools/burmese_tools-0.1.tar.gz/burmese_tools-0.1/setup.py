from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    description = f.read()

setup(
    name="burmese_tools",
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # Empty because no external libraries are required
    long_description=description,
    long_description_content_type="text/markdown",
)
