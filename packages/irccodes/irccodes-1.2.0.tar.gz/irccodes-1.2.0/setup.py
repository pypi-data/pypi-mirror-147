from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='irccodes',
    version='1.2.0',
    author='Tomas Globis',
    description='Python module for formatting text in IRC',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type="text/markdown",
    url='https://github.com/TomasGlgg/irccodes',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 6 - Mature',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Filters'
    ]
)
