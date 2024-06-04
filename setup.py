from setuptools import setup

setup(
    name='fhe_py',
    description='A Python library for Fully Homomorphic Encryption',
    author='0xvon',
    author_email='kingmasatojames@gmail.com',
    license='MIT',
    install_requires=['numpy', 'pytest'],
    packages=['util', 'tests', 'bfv', 'ckks']
)