from setuptools import setup, find_packages
with open("README.md", "r") as fh:
	long_description = fh.read()

setup(
    name='pypiolegg',
    version='0.1',
    license='MIT',
    description="A Hello World package",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="Oleg Nechaev",
    author_email='nechaev20000@gmail.com',
    packages=find_packages(),
    url='https://https://github.com/olegnechaev1/github/tree/dev/task12',
    install_requires=[
          'Django==4.0.4',
          'fastapi==0.75.1'
      ],

)