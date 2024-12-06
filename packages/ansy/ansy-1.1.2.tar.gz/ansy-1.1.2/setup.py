from setuptools import setup, find_packages
from os import path

# Current working directory
cwd = path.abspath(path.dirname(__file__))


with open(path.join(cwd, "README.md"), encoding="utf-8") as f:
    try:
        long_description = f.read()
    except:
        long_description = None

setup(
    name="ansy",
    version="1.1.2",
    description="A Python package to colorize and format output in the terminal.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Anas-Shakeel/ansy",
    author="Anas Shakeel",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points={"console_scripts": ["ansy=ansy.cli:main"]},
    keywords=[
        "python",
        "ANSI",
        "ANSI color",
        "color",
        "cli",
        "command-line",
        "terminal",
        "text formatting",
        "color output",
        "ansy",
        "terminal",
        "text styling",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Terminals",
    ],
    python_requires=">=3.8",
)
