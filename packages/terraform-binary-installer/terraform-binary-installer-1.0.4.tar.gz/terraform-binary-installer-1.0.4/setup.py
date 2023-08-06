#!/usr/bin/env python

from setuptools import setup

setup(
    name='terraform-binary-installer',
    version='1.0.4',
    description='Python wrapper for install terraform version corresponding to package version.',
    author='Iman Azari',
    author_email='azari@mahsan.co',
    url='https://github.com/imanazari70/terraform-binary-installer',
    packages=['terraform_binary_installer'],
    scripts=['scripts/terraform']
)
