from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='FlaskAutoDocs',
    version='0.3.0',
    packages=find_packages(),
    description='Documentation generator for flask',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    include_package_data=True,
    install_requires=['Flask'],
)
