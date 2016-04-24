#!/usr/bin/env python

import sys
import os
import time
from grpc.beta import implementations
from pynms_grpc.common import pynms_rpc_pb2
from pyangbind.lib.serialise import pybindIETFJSONEncoder
from pyangbind.lib.xpathhelper import YANGPathHelper
import json
from pynms_grpc.client.client_common import PyNMSConfigOperation, \
                        PyNMSGRPCClientException, PyNMSClientGRPCMethods

class PyNMSGRPCClient(object):
  def __init__(self, server, port, timeout=2):
    self._server = server
    self._port = port
    self._channel = None
    self._stub = None
    try:
      self._timeout = int(timeout)
    except ValueError:
      raise PyNMSGRPCClientException("Timeout specified must be an integer")

  def run(self):
    # TODO: probably should support more than the insecure channel
    self._channel = implementations.insecure_channel(self._server, self._port)
    self._stub = pynms_rpc_pb2.beta_create_OCPyNMS_stub(self._channel)

  def get_paths(self, paths, request_id, prefix=None, data_type='ALL'):
    getreq = PyNMSClientGRPCMethods.generate_get_message(paths, request_id, prefix=prefix, data_type=data_type)
    response = self._stub.Get(getreq, self._timeout)
    return response

  def set_paths(self, operations, request_id=0):
    setreq = PyNMSClientGRPCMethods.generate_set_message(operations, request_id)
    response = self._stub.Set(setreq, self._timeout)
    return response