from PyVoltammetry import __version__
import setuptools

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name = "PyVoltammetry",
    version = __version__,
    author = "Yang Li",
    author_email = "yli52156@gmail.com",
    description = "A Python package for analysing CV curves of electrocatalysts",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/kkyang26/PyVoltammetry",
    packages = setuptools.find_packages(),
    install_requires=['matplotlib', 'numpy'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)