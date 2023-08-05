#!/usr/bin/env python

from importlib.metadata import entry_points
import setuptools
import pdf2image_cli

install_requires = [
    'pip',
    'setuptools',
    'pdf2image>=1.16.0'
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_decription = fh.read()

setuptools.setup(
    name="pdf2image-cli",
    version='1.0.0',
    author='Carlos Valdez',
    author_email='carlosvaldez@carlosvaldez.works',
    description='pdf2image port to a CLI version',
    long_description=long_decription,
    long_description_content_type='text/markdown',
    url='https://github.com/DJCarlosValdez/pdf2image-cli',
    python_requires='>=3.8',
    install_requires=install_requires,
    packages=setuptools.find_packages(
        include=['pdf2image_cli', 'pdf2image_cli.*']),
    entry_points={
        'console_scripts': [
            "pdf2image=pdf2image_cli.__main__:main"
        ]
    }
)
