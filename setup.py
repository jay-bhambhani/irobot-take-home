from distutils.core import setup

from setuptools import find_packages

setup(
    name='food2fork',
    version='0.1',
    scripts=['food2fork_task.py'],
    data_files=['config/secrets.json'],
    packages=find_packages(),
    long_description=open('README.txt').read(),
)