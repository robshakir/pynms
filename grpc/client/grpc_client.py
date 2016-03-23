#!/usr/bin/env python

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "common"))
from grpc.beta import implementations
import pynms_rpc_pb2

def run():
  channel = implementations.insecure_channel('localhost', 50051)
  stub = pynms_rpc_pb2.beta_create_OCPyNMS_stub(channel)
  getr = pynms_rpc_pb2.GetRequest(path="a path")
  response = stub.Get(getr, 10)
  print response

if __name__ == '__main__':
  run()