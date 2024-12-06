"""Crow/AAP Alarm IP / Serial Module package."""
from setuptools import setup, find_packages

setup(
    name='pyaapalarmmodule',
    version='2024.11.24',
    description='Library for AAP Alarm IP / Serial Module',
    url='https://github.com/osotechie/pyaapalarmmodule',
    author='osotechie',
    author_email='owen@demooy.co.nz',
    license='MIT',
    packages=find_packages(),
    install_requires=['requests'],
    keywords='AAP Alarm IP / Serial Module for Home Assistant',
    include_package_data=True,
    zip_safe=False
)

