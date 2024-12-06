"""Crow/AAP Alarm IP / Serial Module package."""
from setuptools import setup, find_packages

setup(
    name='pycrowmodule',
    version='0.10',
    description='Library for Crow/AAP Alarm IP / Serial Module',
    url='https://github.com/osotechie/pycrowmodule',
    author='osotechie',
    author_email='owen@demooy.co.nz',
    license='MIT',
    packages=find_packages(),
    install_requires=['requests'],
    keywords='Crow/AAP Alarm IP / Serial Module for Home Assistant',
    include_package_data=True,
    zip_safe=False
)

