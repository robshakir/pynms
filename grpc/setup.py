from setuptools import setup, find_packages
from codecs import open
from os import path

thisdir = path.abspath(path.dirname(__file__))

with open(path.join(thisdir, "README.rst"), encoding='utf-8') as readme:
  long_description = readme.read()

setup(
    name='PyNMSGRPC',

    # PyangBind uses the same versioning approach as OpenConfig - see
    # http://www.openconfig.net/file-cabinet/Semantic_Versioning_for_OpenConfig.pdf?attredirects=0&d=1
    version='0.0.1',

    description="",
    long_description=long_description,

    url="https://github.com/robshakir/pynms",

    author="Rob Shakir",
    author_email="rjs@rob.sh",

    #license="Apache",
    #classifiers=[
    #    'Development Status :: 4 - Beta',
    #    'Intended Audience :: Telecommunications Industry',
    #    'Intended Audience :: Developers',
    #    'Topic :: Software Development :: Code Generators',
    #    'License :: OSI Approved :: Apache Software License',
    #    'Programming Language :: Python :: 2.7',
    #    'Programming Language :: Python :: 2 :: Only'
    #],
    include_package_data=True,
    #keywords="yang pyang",
    packages=find_packages(),
    install_requires=['pyangbind', 'grpcio'],
)
