#!/usr/bin/env python

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "common"))
import pynms_rpc_pb2


class NetElem(pynms_rpc_pb2.BetaOCPyNMSServicer):
  def Get(self, request, context):
    return pynms_rpc_pb2.GetResponse(value="a response")

def serve():
  server = pynms_rpc_pb2.beta_create_OCPyNMS_server(NetElem())
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(84600)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
