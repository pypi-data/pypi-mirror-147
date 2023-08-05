from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
   name='darkyaml',
   version='0.0.1',
   description='DarkYml is simple yaml db',
   long_description=long_description,
   long_description_content_type='text/markdown',
   license="MIT",
   author='xllwhoami',
   author_email='anonymous@ass.net',
   url="http://www.github.com/xllwhoami/darkyml",
   packages=['darkyaml'],
   install_requires=['ruamel.yaml'] #external packages as dependencies
)