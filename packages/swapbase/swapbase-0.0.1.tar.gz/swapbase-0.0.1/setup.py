from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = "Swap Base converts numbers to different bases, and provides option to override character maps"
LONG_DESCRIPTION = "WIP: Currently only conversion to base10 is supported"

# Setup Details
setup(
    name="swapbase",
    version=VERSION,
    author="Pratik Mishra",
    author_email="overtnibble.packages@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[], # no additional packages required for current setup

    keywords=['python3', 'base conversion', 'decimal base', "generic base calculator"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Programming Language :: Python :: 3"
    ],
)
