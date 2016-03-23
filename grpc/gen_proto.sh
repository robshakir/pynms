#!/bin/bash

protoc -I common/proto --python_out=common --grpc_out=common --plugin=protoc-gen-grpc=`which grpc_python_plugin` common/proto/pynms_rpc.proto
