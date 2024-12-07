from setuptools import setup, find_packages

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Implementation of the Feng-Hirst RST Discourse Parser"

setup(
    name="feng-hirst-rst-parser",
    version="0.1.1",
    author="Thomas Huber",
    author_email="thomas.huber@unisg.ch",
    description="Implementation of the Feng-Hirst RST Discourse Parser",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ThHuberSG/feng-hirst-rst-parser",
    project_urls={
        "Bug Tracker": "https://github.com/ThHuberSG/feng-hirst-rst-parser/issues",
        "Documentation": "https://github.com/ThHuberSG/feng-hirst-rst-parser/wiki",
    },
    packages=["feng_hirst_parser"],
    package_dir={"feng_hirst_parser": "feng_hirst_parser"},
    include_package_data=True,
    package_data={
        "": ["model/*", "texts/*", "tools/*"],
    },
    install_requires=[
        "networkx==3.4.2",
        "nltk==3.9.1",
        "pytest==8.3.3",
    ],
    license="BSD-3-Clause",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    keywords="RST discourse parsing, computational linguistics, NLP, Feng-Hirst",
)