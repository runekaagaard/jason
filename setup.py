from distutils.core import setup
from setuptools import find_packages

setup(
    name='jason',
    version='0.1.0',
    author=u'Rune Kaagaard',
    author_email='rumi.kg@gmail.com',
    packages=find_packages(),
    url='https://github.com/runekaagaard/jason',
    license='GPLv2',
    description='Lightweight helpers for views returning json data in Django.' ,
    long_description=open('README.rst').read(),
    zip_safe=False,
)