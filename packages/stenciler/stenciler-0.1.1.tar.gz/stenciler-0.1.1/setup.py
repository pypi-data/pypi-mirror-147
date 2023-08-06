"""Installation script for stenciler."""
from pathlib import Path

from setuptools import find_packages, setup


def get_readme_text() -> str:
    """Gets the contents of the README."""
    return (Path(__file__).parent / "README.md").read_text(encoding="utf8")


setup(
    name="stenciler",
    version="0.1.1",
    description=(
        "A CLI tool for building plaintext artifacts by populating Jinja templates"
        " from YAML files."
    ),
    long_description=get_readme_text(),
    long_description_content_type="text/markdown",
    author="Miles Butler",
    author_email="miles@milesbutler.dev",
    url="https://github.com/mtmbutler/stenciler",
    license="MIT",
    packages=["stenciler"] + ["stenciler." + i for i in find_packages("stenciler")],
    setup_requires=["wheel"],
    install_requires=[
        "pyyaml>=6.0",
        "Jinja2>=3.1",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["stenciler = stenciler.cli:cli"]},
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Text Processing",
    ],
)
