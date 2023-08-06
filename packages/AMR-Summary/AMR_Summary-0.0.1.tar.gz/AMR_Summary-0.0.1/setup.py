#!/usr/bin/env python
from setuptools import setup, find_packages
from distutils.util import convert_path
import os

# Find the version
version = dict()
with open(convert_path(os.path.join('amr_summary', 'version.py')), 'r') as version_file:
    exec(version_file.read(), version)

setup(
    name='AMR_Summary',
    version=version['__version__'],
    entry_points={
        'console_scripts': [
            'AMR_Summary = amr_summary.amr_summary:cli',
        ],
    },
    packages=find_packages(),
    include_package_data=True,
    author='Adam Koziol',
    author_email='adam.koziol@inspection.gc.ca',
    url='https://github.com/OLC-Bioinformatics/AMR_Summary',
)
