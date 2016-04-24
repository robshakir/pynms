#!/bin/bash

SDIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
protoc -I $SDIR/../pynms_grpc/common/proto --python_out=$SDIR/../pynms_grpc/common --grpc_out=$SDIR/../pynms_grpc/common \
          --plugin=protoc-gen-grpc=`which grpc_python_plugin` $SDIR/../pynms_grpc/common/proto/pynms_rpc.proto
protoc -I $SDIR/../pynms_grpc/common/proto --python_out=$SDIR/../pynms_grpc/common --grpc_out=$SDIR/../pynms_grpc/common \
          --plugin=protoc-gen-grpc=`which grpc_python_plugin` $SDIR/../pynms_grpc/common/proto/cisco_ems_grpc.proto
