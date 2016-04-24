#!/bin/bash

set -e
PACKAGE_VER="1"
RELEASE_VER="0.0.1"
THISDIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENTDIR=$THISDIR/../..
DISTDIR=$PARENTDIR/dist


YANG_EXAMPLES_VER="0.0.1"
YANG_EXAMPLES_DIR=$PARENTDIR/../egbindings
YANG_EXAMPLES_DIST_DIR=$YANG_EXAMPLES_DIR/dist


GRPC_WHEEL=$DISTDIR/PyNMSGRPC-${RELEASE_VER}-py2-none-any.whl
(cd $PARENTDIR && python setup.py bdist_wheel)
cp $GRPC_WHEEL .

YANG_EXAMPLES_WHEEL=$YANG_EXAMPLES_DIST_DIR/PyNMSYANGExamples-${YANG_EXAMPLES_VER}-py2-none-any.whl
(cd $YANG_EXAMPLES_DIR && python setup.py bdist_wheel)
cp $YANG_EXAMPLES_WHEEL .

cp -R ../../examples/client .

docker build -t pynms/grpc_client:${RELEASE_VER}p${PACKAGE_VER} .
rm $THISDIR/*.whl

