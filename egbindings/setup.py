from setuptools import setup, find_packages
from codecs import open
from os import path
from glob import glob

thisdir = path.abspath(path.dirname(__file__))
import pynms_yang_examples

setup(
    name='PyNMSYANGExamples',
    version=pynms_yang_examples.__version__,
    author="Rob Shakir",
    author_email="rjs@rob.sh",
    url="https://github.com/robshakir/pynms",
    packages=find_packages(),
    install_requires=['pyangbind', 'requests'],
)
