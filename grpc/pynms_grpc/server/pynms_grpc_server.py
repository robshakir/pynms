#!/usr/bin/env python

import sys
import os
import time
import logging
from pyangbind.lib.xpathhelper import YANGPathHelper
from pyangbind.lib.serialise import pybindJSONEncoder
from pynms_grpc.common import pynms_rpc_pb2
from pynms_grpc.server.server_common import PyNMSServerGRPCMethods

class GPRCPyNMSServicer(pynms_rpc_pb2.BetaOCPyNMSServicer):
  def __init__(self, path_helper, logger=None):
    self._path_helper = path_helper
    self._logger = logger
    self._logger.debug("Created PyNMS gRPC servicer")

  def Get(self, request, context):
    self._logger.debug("Got get request: %s" % str(request))
    response_msg = PyNMSServerGRPCMethods.service_get_request(request, self._path_helper, logger=self._logger)
    self._logger.debug("SENDING: %s" % response_msg)
    return response_msg

  def Set(self, request, context):
    self._logger.debug("Got set request: %s" % str(request))
    response_msg = PyNMSServerGRPCMethods.service_set_request(request, self._path_helper, logger=self._logger)
    self._logger.debug("SENDING: %s" % response_msg)
    return response_msg

class PyNMSGRPCServer(object):
  def __init__(self, path_helper, port=50051):
    self._path_helper = path_helper

    self._logger = logging.getLogger('PyNMSGRPCServer')
    self._logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('/tmp/pynms_grpc_server.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    self._logger.addHandler(fh)
    self._logger.info("pynms gRPC server started")

    self._server = pynms_rpc_pb2.beta_create_OCPyNMS_server(GPRCPyNMSServicer(self._path_helper, logger=self._logger))
    self._server.add_insecure_port("[::]:%s" % port)

  def serve(self, runtime=86400):
    self._server.start()
    try:
      while True:
        time.sleep(86400)
    except KeyboardInterrupt:
      self._server.stop(0)
