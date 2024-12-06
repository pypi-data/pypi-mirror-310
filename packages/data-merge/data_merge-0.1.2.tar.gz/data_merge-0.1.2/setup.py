from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='data_merge',
    version='0.1.2',
    description='Python package for merging Excel and CSV files',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Ojo Ilesanmi',
    author_email='ojoilesanmi89@gmail.com',
    packages=find_packages(),
    install_requires=[
        'pandas'
    ],
)
