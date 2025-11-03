"""
Setup configuration for destiny-cli
Created by Piotr Nowicki (DevOps Engineer)
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="destiny-cli",
    version="0.1.0",
    author="Destiny Team Framework",
    author_email="team@destiny-framework.dev",
    description="Command-line tools for Destiny Team Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/destiny-framework/destiny-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "requests>=2.28.0",
        "psycopg2-binary>=2.9.0",
    ],
    entry_points={
        "console_scripts": [
            "destiny=destiny_cli.main:main",
        ],
    },
)
