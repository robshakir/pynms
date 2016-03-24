#!/usr/bin/env python

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "common"))
from grpc.beta import implementations
import pynms_rpc_pb2
from pyangbind.lib.serialise import pybindIETFJSONEncoder
from nms_grpc.helpers import grpc_PyNMS_methods
from pyangbind.lib.xpathhelper import YANGPathHelper
import ybind
import json

class grpc_PyNMS_config_operation(object):
  def __init__(self, path, obj, operation):
    self.path = path
    self.content = obj
    self.operation = operation

  def __str__(self):
    return "%s -> %s" % (self.path, self.content.get(filter=True))

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

  def set_paths(self, operations, request_id=0, operation_id_base="operation"):
    try:
      msg_reqid = int(request_id)
    except ValueError:
      raise grpc_PyNMS_client_exception("request_id must be an integer")

    setreq = pynms_rpc_pb2.SetRequest(request_id=msg_reqid, encoding=pynms_rpc_pb2.JSON_IETF)

    req = 0
    for operation in operations:
      if not isinstance(operation, grpc_PyNMS_config_operation):
        raise grpc_PyNMS_client_exception("operations must be grpc_PyNMS_config_operation instances")
      setop = setreq.config_operation.add()
      setop.operation_id = "%s_%s" % (operation_id_base, req)
      if operation == 'UPDATE_CONFIG':
        setop.operation = pynms_rpc_pb2.UPDATE_CONFIG
      else:
        # only support sending UPDATE_CONFIG right now
        setop.operation = pynms_rpc_pb2.UPDATE_CONFIG
      setop.path = operation.path

      # always use IETF JSON for now
      tree = pybindIETFJSONEncoder.generate_element(operation.content, flt=True)
      encoder = pybindIETFJSONEncoder
      setop.value = json.dumps(tree, cls=encoder)
      req += 1

    response = self._stub.Set(setreq, self._timeout)
    return response

if __name__ == '__main__':
  client = grpc_PyNMS_client('localhost', 50051)
  client.run()
  print client.get_paths(["/system/config/hostname", "/system/config/domain-name", "/system"],
                         request_id=0)

  from ybind.system import system
  s = system()
  s.config.hostname = "rtr42"
  s.config.domain_name = "gru.br"
  s_oper = grpc_PyNMS_config_operation("/system", s, 'UPDATE_CONFIG')

  print "BEFORE: "
  print client.get_paths(["/system/config"], request_id=0)
  print client.set_paths([s_oper])
  print "AFTER: "
  print client.get_paths(["/system/config"], request_id=1)

  print "BEFORE: "
  print client.get_paths(["/system/ntp"], request_id=2)

  from ybind.system.ntp import ntp
  n = ntp()
  n.config.enabled = True
  for svr in [('svr1', "2001:db8::1"), ('svr2', "2001:db8::42")]:
    s = n.servers.server.add(svr[1])
    s.config.name = svr[0]
  s_oper = grpc_PyNMS_config_operation("/system/ntp", n, 'UPDATE_CONFIG')

  print "AFTER: "
  print client.get_paths(["/system/ntp"], request_id=3)



  sys.exit(0)
