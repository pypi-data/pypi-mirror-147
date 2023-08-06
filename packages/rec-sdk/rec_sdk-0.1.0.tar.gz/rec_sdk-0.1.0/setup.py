from setuptools import setup, find_packages


NAME = 'rec_sdk'
DESCRIPTION  = 'wimi sdk for recommendation'
URL = 'https://wimigitlab.git'
EMAIL = ''
AUTHOR = 'Sun Xuen'

REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.0'
#REQUIRED = ["pyspark", "pyhive", "tensorflow>=1.7"]


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    #install_requires=REQUIRED,
    license="MIT"
)



# detail example  https://github.com/kennethreitz/setup.py/blob/master/setup.py
