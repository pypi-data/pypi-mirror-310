from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.9'
DESCRIPTION = 'Data-mining tutorials'
LONG_DESCRIPTION = 'A package to help students'

# Setting up
setup(
    name="mksir",
    version=VERSION,
    author="Developer cheetah",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_data={
        'mksir': ['*.ipynb', '*.pdf'],  # Include all .ipynb and .pdf files in all subdirectories
    },
    install_requires=[],
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)