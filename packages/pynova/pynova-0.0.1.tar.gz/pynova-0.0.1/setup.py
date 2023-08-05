#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'An easy Python alternative to R functions relating to ANOVA'
LONG_DESCRIPTION =  """As an ANOVA professor's research assistant at Brigham Young University, 
                    I was tasked with converting sample R code designed for class instruction 
                    to Python. I was surprised with the lack of options in Python to perform 
                    tasks such as calculating power for more than two groups. This package 
                    provides easy Python function equivalents to some of the more complex R 
                    functions relating to analysis surrounding ANOVA and power."""

# Setting up
setup(
        name="pynova", 
        version=VERSION,
        author="Joshua Gladwell",
        author_email="joshegladwell@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['ANOVA', 'power', 'R'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)