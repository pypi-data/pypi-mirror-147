# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='myNeurospydia',
    packages=find_packages(),
    version='0.1.2',
    description='Partially fixed version of Neuropsydia library, a Python module for creating experiments, tasks and questionnaires',
    author='Laborde',
    license='ENS_Paris_Saclay',
    install_requires=['pygame',
                      'numpy',
                      'neurokit',
                      'pandas',
                      'datetime',
                      'scipy'],
)