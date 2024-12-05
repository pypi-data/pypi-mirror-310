"""Setup script for the Flick Python SDK."""
import os  # Standard library imports
from setuptools import setup, find_packages  # type: ignore


working_directory = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='flick_sdk',
    version='0.0.1',
    author='Quraba inc',
    description='Flick Python SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
)
