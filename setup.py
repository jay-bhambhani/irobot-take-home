from distutils.core import setup

setup(
    name='food2fork',
    version='0.1',
    scripts=['food2fork_task.py'],
    packages=['f2f.*'],
    long_description=open('README.txt').read()
)