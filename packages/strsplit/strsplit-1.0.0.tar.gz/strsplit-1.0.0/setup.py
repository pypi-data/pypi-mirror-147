from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='strsplit',
    version='1.0.0',
    license='MIT',
    author="not-nef",
    description="Easy splitting of strings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/not-nef/strsplit',
    keywords='strsplit',
)