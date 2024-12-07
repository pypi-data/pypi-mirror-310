from setuptools import setup, find_packages

setup(
    name='mydebug',
    version='0.1.1',
    author='p4ylex',
    description="A simple debugging tool for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
)