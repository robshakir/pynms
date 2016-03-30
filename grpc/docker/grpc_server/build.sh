#!/bin/bash

set -e
PACKAGE_VER="1"
RELEASE_VER="0.0.1"
THISDIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENTDIR=$THISDIR/../..
DISTDIR=$PARENTDIR/dist

GRPC_WHEEL=$DISTDIR/PyNMSGRPC-${RELEASE_VER}-py2-none-any.whl
(cd $PARENTDIR && python setup.py bdist_wheel)
cp $GRPC_WHEEL .

docker build -t pynms/grpc_server:${RELEASE_VER}p${PACKAGE_VER} .
rm $THISDIR/*.whl

