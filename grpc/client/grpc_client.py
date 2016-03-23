#!/usr/bin/env python

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "common"))
from grpc.beta import implementations
import pynms_rpc_pb2


class grpc_PyNMS_client_exception(Exception):
  pass

class grpc_PyNMS_client(object):
  def __init__(self, server, port, timeout=2):
    self._server = server
    self._port = port
    self._channel = None
    self._stub = None
    try:
      self._timeout = int(timeout)
    except ValueError:
      raise grpc_PyNMS_client_exception("Timeout specified must be an integer")

  def run(self):
    # TODO: probably should support more than the insecure channel
    self._channel = implementations.insecure_channel(self._server, self._port)
    self._stub = pynms_rpc_pb2.beta_create_OCPyNMS_stub(self._channel)

  def get_paths(self, paths, request_id, operation_id_base="operation", operation='GET_ALL'):
    try:
      msg_reqid = int(request_id)
    except ValueError:
      raise grpc_PyNMS_client_exception("request_id must be an integer")

    getreq = pynms_rpc_pb2.GetRequest(request_id=msg_reqid,
                                    encoding=pynms_rpc_pb2.JSON_IETF)

    req = 0
    for path in paths:
      getop = getreq.get_request.add()
      getop.operation_id = "%s_%s" % (operation_id_base, req)
      if operation == 'GET_ALL':
        getop.operation = pynms_rpc_pb2.GET_ALL
      else:
        # only support sending GET_ALL right now
        getop.operation = pynms_rpc_pb2.GET_ALL
      getop.path = path
      req += 1

    response = self._stub.Get(getreq, self._timeout)
    return response

if __name__ == '__main__':
  client = grpc_PyNMS_client('localhost', 50051)
  client.run()
  print client.get_paths(["/system/config/hostname", "/system/config/domain-name", "/system"],
                         request_id=0)
  sys.exit(0)
