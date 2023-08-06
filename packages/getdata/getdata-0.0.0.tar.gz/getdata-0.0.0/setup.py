import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='getdata',
    version='0.0.0',
    long_description=README,
    long_description_content_type="text/markdown",
    license='MIT',
    author="Ryan Young",
    author_email='ryanyoung99@live.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/ryayoung/getdata',
    keywords='source data github',
    install_requires=[
          'pandas',
          'numpy',
      ],

)
