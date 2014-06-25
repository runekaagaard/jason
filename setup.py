from distutils.core import setup
from setuptools import find_packages

description = 'Lightweight helpers for views returning json data in Django.'

try:
    long_description = open('README.rst').read()
except:
    long_description = description

setup(
    name='jason',
    version='0.1.7',
    author=u'Rune Kaagaard',
    author_email='rumi.kg@gmail.com',
    packages=find_packages(),
    url='https://github.com/runekaagaard/jason',
    license='GPLv2',
    description=description,
    long_description=long_description,
    zip_safe=False,
)
