#!/usr/bin/env python

import sys
import os
import time
from pyangbind.lib.xpathhelper import YANGPathHelper
from pyangbind.lib.serialise import pybindJSONEncoder
from pynms_grpc.common import pynms_rpc_pb2
from pynms_grpc.server.server_common import PyNMSServerGRPCMethods

class GPRCPyNMSServicer(pynms_rpc_pb2.BetaOCPyNMSServicer):
  def __init__(self, path_helper):
    f = open("/tmp/foo1", 'w')
    f.write("server init\n")
    f.flush()
    f.close()
    self._path_helper = path_helper

  def Get(self, request, context):
    f = open("/tmp/foo2", 'w')
    f.write("server get req -> %s\n" % request)
    f.flush()
    f.close()
    f = open("/tmp/foo2.5", 'w')
    f.write("%s" % str(PyNMSServerGRPCMethods.service_get_request(request, self._path_helper)))
    f.write("\n")
    f.flush()
    f.close()
    response_msg = PyNMSServerGRPCMethods.service_get_request(request, self._path_helper)
    return response_msg

  def Set(self, request, context):
    response_msg = PyNMSServerGRPCMethods.service_set_request(request, self._path_helper)
    return response_msg

class PyNMSGRPCServer(object):
  def __init__(self, path_helper, port=50051):
    self._path_helper = path_helper
    self._server = pynms_rpc_pb2.beta_create_OCPyNMS_server(GPRCPyNMSServicer(self._path_helper))
    self._server.add_insecure_port("[::]:%s" % port)

  def serve(self, runtime=86400):
    self._server.start()
    try:
      while True:
        time.sleep(86400)
    except KeyboardInterrupt:
      self._server.stop(0)
