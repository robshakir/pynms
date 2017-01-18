#!/bin/bash

# This example requires virtualenv.
virtualenv pytest
source pytest/bin/activate

pip install pyangbind requests pyaml

# We need to build the protobuf library in order to
# ensure that we have a proto3 shared lib.
BERR=$(
  wget https://github.com/google/protobuf/releases/download/v3.1.0/protobuf-python-3.1.0.tar.gz --quiet
  tar xvzf protobuf-python-3.1.0.tar.gz >/dev/null 2>&1
  cd protobuf-3.1.0
  ./configure >/dev/null 2>&1 && make >/dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo "ERR"
  fi
)

if [ "$BERR" != "" ]; then
  echo "Could not build protobuf C++ module..."
  exit
fi

export LD_LIBRARY_PATH=../src/.libs

ERR=$(
  cd protobuf-3.1.0/python
  python setup.py build >/dev/null 2>&1 && python setup.py test >/dev/null 2>&1 && python setup.py install >/dev/null 2>&1
  if [ $? -ne 0 ]; then
    echo "ERR"
  fi
)

echo $ERR

if [ "$ERR" != "" ]; then
  echo "Could not build protobuf python module..."
  exit
fi

# Install the example bindings module.
(
  cd egbindings
  scripts/build.sh
  python setup.py install
)

# Install the gRPC example components.
(
  cd grpc
  python setup.py install
)

