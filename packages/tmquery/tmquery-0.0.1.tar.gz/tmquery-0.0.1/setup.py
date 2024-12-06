from setuptools import setup, find_packages

setup(
    name='tmquery',
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    install_requires=[
        'requests',
        'bs4'
    ]
)