import sys
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    deps = [dep for dep in f.read().split('\n') if dep.strip() != '']
    install_requires = deps

with open('README.md') as f:
    DESC = f.read()


setup(name='flakon',
      version="0.2",
      description="A collection of opinionated Flask Blueprints",
      long_description=DESC,
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      install_requires=install_requires)
