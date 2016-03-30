#!/bin/bash

PYNMS_GRPC_VERSION="0.0.1"

export DEBIAN_FRONTEND=noninteractive
echo "deb http://http.debian.net/debian jessie-backports main" >> /etc/apt/sources.list
apt-get -y --force-yes update
apt-get -y --force-yes install python-pip python2.7 zlib1g-dev libgrpc-dev python-dev libxml2-dev libxslt1-dev python-virtualenv
pip install --upgrade pip

virtualenv /usr/virtualenv
source /usr/virtualenv/bin/activate

# no dependencies right now for PyNMSGRPC
pip install grpcio pyangbind

pip install /tmp/PyNMSGRPC-${PYNMS_GRPC_VERSION}-py2-none-any.whl
rm /tmp/*.whl
