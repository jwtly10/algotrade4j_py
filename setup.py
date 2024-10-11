# setup.py
from setuptools import setup, find_packages

setup(
    name='algotrade4j_py',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
    ],
    description='A python SDK for fetching market data from AlgoTrade4j Platform',
    url='https://github.com/jwtly10/algotrade4j_py',
)
