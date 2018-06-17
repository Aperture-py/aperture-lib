'''Setup for Aperture distribution.'''

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

__version__ = '0.0.0.dev8'

setup(
    name='aperturelib',
    version=__version__,
    description='A library for image re-sizing and compression.',
    long_description=readme,
    url='https://github.com/Aperture-py/aperture-lib',
    author='salvatorej1@wit.edu, kennedyd3@wit.edu, robbinsa@wit.edu',
    license=license,
    install_requires=['Pillow==5.0.0'],
    packages=find_packages(
        exclude=['docs', 'tests*']
    ),  # prevent docs and tests from being installed on user's system as actual packages
    include_package_data=True,
    classifiers=('Programming Language :: Python :: 3',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independant'))
