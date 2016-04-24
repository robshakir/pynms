from setuptools import setup, find_packages
from codecs import open
from os import path

thisdir = path.abspath(path.dirname(__file__))

with open(path.join(thisdir, "README.rst"), encoding='utf-8') as readme:
  long_description = readme.read()

print find_packages()

setup(
    name='PyNMSGRPC',
    version='0.0.1',

    description="gRPC API library conforming to the OpenConfig RPC specification",
    long_description=long_description,

    url="https://github.com/robshakir/pynms",

    author="Rob Shakir",
    author_email="rjs@rob.sh",
    license="Apache",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Developers',
        'Topic :: System :: Networking',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only'
    ],
    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
    install_requires=['pyangbind', 'grpcio'],
    package_data={'pynms_grpc': ['examples/*']}
)
