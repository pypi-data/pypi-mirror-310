from setuptools import setup, find_packages

setup(
    name='myDebuG',
    version='0.1.0',
    author='p4ylex',
    description="A simple debugging tool for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
)