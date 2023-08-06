#!/usr/bin/env/python

from setuptools import setup, find_packages


setup(
    name="seeded-graph-matching",
    version="1.0.5",
    author="Ben Johnson and Fred Battista",
    maintainer="remi.rampin@nyu.edu",
    url="https://gitlab.com/datadrivendiscovery/contrib/sgm",
    license="MIT",
    description="Python port of seeded graph matching (SGM)",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'cython>=0.29.3',
        'tqdm',
        'numpy',
        'pandas',
        'lap05>=0.5.0,<0.6',
        'lapjv>=1.3.1',
    ],
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Programming Language :: Python :: 3",
    ],
)
