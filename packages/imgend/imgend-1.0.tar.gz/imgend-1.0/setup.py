from setuptools import setup, find_packages

setup(
    name='imgend',
    version='1.0',
    packages=find_packages(),
    install_requires=[],
    package_data={'imgend': ['*.ipynb', '*.py']},
)
