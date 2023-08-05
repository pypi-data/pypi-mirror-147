# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='myNeurospydia',
    packages=find_packages(),
    version='0.1.3',
    description='Partially fixed version of Neuropsydia library, a Python module for creating experiments, tasks and questionnaires',
    author='Laborde',
    license='ENS_Paris_Saclay',
    install_requires=['Pillow',
                      'cryptography',
                      'neurokit',
                      'numpy',
                      'pandas',
                      'pygame',
                      'python-docx',
                      'pyxid',
                      'statsmodels'],
)


