#!/usr/bin/env python

import sys
import os
import time
from grpc.beta import implementations
from pynms_grpc.common import cisco_ems_grpc_pb2
from pyangbind.lib.serialise import pybindIETFJSONEncoder
from pyangbind.lib.xpathhelper import YANGPathHelper
import json
from pynms_grpc.client.client_common import PyNMSConfigOperation, \
                        PyNMSGRPCClientException

class CiscoGRPCClient(object):
  def __init__(self, server, port, timeout=10, user=None, password=None):
    self._server = server
    self._port = port
    self._channel = None
    self._stub = None
    #self._metadata = [(b'username', user if user is not None else b'admin'),
    #                  (b'password', password if password is not None else b'admin')]
    self._metadata = [(b'username', b'admin'), (b'password', b'admin')]
    try:
      self._timeout = int(timeout)
    except ValueError:
      raise PyNMSGRPCClientException("Timeout specified must be an integer")

  def run(self):
    # TODO: probably should support more than the insecure channel
    #self._channel = implementations.insecure_channel(self._server, self._port)
    self._channel = implementations.insecure_channel(self._server, self._port)
    self._stub = cisco_ems_grpc_pb2.beta_create_gRPCConfigOper_stub(self._channel)
    configs = self._stub.GetConfig(cisco_ems_grpc_pb2.ConfigGetArgs(), 10, metadata=self._metadata)
    print configs

  def get_paths(self, paths, request_id, prefix=None, data_type='ALL'):
    # response = []
    # for path in paths:
    #   getmsg = cisco_ems_grpc_pb2.ConfigGetArgs(ReqId=request_id, yangpathjson=path)
    #   response.append(self._stub.GetConfig(getmsg, self._timeout))
    #   request_id += 1
    # return response
    return

  def set_paths(self, operations, request_id=0):
    return