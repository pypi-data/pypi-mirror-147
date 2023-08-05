# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

setup(
    name='myNeurospydia',
    packages=find_packages(),
    version='0.1.6',
    description='Partially fixed version of Neuropsydia library, a Python module for creating experiments, tasks and questionnaires',
    author='Laborde',
    license='ENS_Paris_Saclay',
    package_data = {
                	"neuropsydia.files.font":["*.ttf", "*.otf"],
                	"neuropsydia.files.binary":["*.png"],
                	"neuropsydia.files.logo":["*.png"]},
    dependency_links=[
	"https://github.com/neuropsychology/NeuroKit.py/zipball/master"],
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


