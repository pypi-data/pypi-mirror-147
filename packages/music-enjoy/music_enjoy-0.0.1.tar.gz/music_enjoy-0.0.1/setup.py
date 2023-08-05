from setuptools import find_packages, setup
 
# Package meta-data.
NAME = 'music_enjoy'
DESCRIPTION = 'A spider to get paid music by LuShengcan.'
URL = 'https://github.com/LuShengcan'
EMAIL = 'shengcan_lu@foxmail.com'
AUTHOR = 'LuShengcan'
REQUIRES_PYTHON = '>=3.8.0'
VERSION = '0.0.1'

# What packages are required for this module to be executed?
REQUIRED = []

# Setting.
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    license="MIT"
)