#!/usr/bin/env python

import unittest
import sys
import json
from pynms_grpc.client.pynms_grpc_client import PyNMSGRPCClient
from pynms_grpc.client.client_common import PyNMSClientGRPCMethods, PyNMSConfigOperation
from pynms_grpc.server.server_common import PyNMSServerGRPCMethods
from pynms_grpc.common import pynms_rpc_pb2
from pynms_yang_examples.bindings import simple_device
from pyangbind.lib.xpathhelper import YANGPathHelper
from pyangbind.lib.serialise import pybindIETFJSONEncoder

class PyNMSGPRC_SimpleMessageTests(unittest.TestCase):

  def _build_invalid_set_message(self, request_id, operations):
    setreq = pynms_rpc_pb2.SetRequest(request_id=request_id, encoding=pynms_rpc_pb2.JSON_IETF)

    req = 0
    for operation in operations:
      setop = setreq.operation.add()
      setop.opcode = pynms_rpc_pb2.UPDATE_CONFIG
      setop.path = operation['path']
      encoder = pybindIETFJSONEncoder
      setop.value = json.dumps(operation['json'], cls=encoder)

    return setreq

  def test_000_generate_get_message(self):
    paths = ["/", "/system"]
    get_msg = PyNMSClientGRPCMethods.generate_get_message(paths, 42)

    self.assertEqual(get_msg.data_type, 0)
    self.assertEqual(pynms_rpc_pb2.GetDataCommand.Name(get_msg.data_type), 'GET_ALL')
    self.assertEqual(get_msg.path, ["/", "/system"])
    self.assertEqual(get_msg.request_id, 42)

  def test_001_generate_set_message(self):
    s = simple_device()
    s.system.config.hostname = "rtr0.lhr.uk"
    s.system.ntp.config.enabled = True

    operations = [
                    PyNMSConfigOperation(s.system.config),
                    PyNMSConfigOperation(s.system.ntp)
                 ]
    set_msg = PyNMSClientGRPCMethods.generate_set_message(operations)

    self.assertEqual(set_msg.request_id, 0)
    self.assertEqual(set_msg.encoding, 0)
    self.assertEqual(pynms_rpc_pb2.EncodingType.Name(set_msg.encoding), "JSON_IETF")
    self.assertEqual(set_msg.prefix, "")
    self.assertEqual(set_msg.operation[0].opcode, 0)
    self.assertEqual(set_msg.operation[0].path, "/system/config")
    self.assertEqual(json.loads(set_msg.operation[0].value), \
                        {u"simple-device:hostname": u"rtr0.lhr.uk"})
    self.assertEqual(set_msg.operation[1].opcode, 0)
    self.assertEqual(set_msg.operation[1].path, "/system/ntp")
    self.assertEqual(json.loads(set_msg.operation[1].value), \
                        {u"simple-device:config": {u"enabled": True}})

  def test_002_handle_get_one_path(self):
    server_ph = YANGPathHelper()
    s = simple_device(path_helper=server_ph)

    s.system.config.hostname = "rtr0.lhr.uk"
    s.system.config.domain_name = "test.jiveip.net"

    get_msg = PyNMSClientGRPCMethods.generate_get_message(["/system"], 0)
    ret_msg = PyNMSServerGRPCMethods.service_get_request(get_msg, server_ph)

    self.assertEqual(ret_msg.request_id, 0)
    self.assertEqual(ret_msg.response_code, 0)
    self.assertEqual(pynms_rpc_pb2.RPCResponse.Name(ret_msg.response_code), 'OK')
    self.assertEqual(len(ret_msg.response), 1)
    self.assertEqual(ret_msg.response[0].path, "/system")

    err = None
    try:
      json_returned = json.loads(ret_msg.response[0].value)
    except Exception as e:
      err = e

    self.assertIsNone(err)
    self.assertEqual(json_returned, {u'simple-device:ntp': {u'state': {u'enabled': False},
                u'config': {u'enabled': False}}, u'simple-device:config':
                {u'domain-name': u'test.jiveip.net', u'hostname': u'rtr0.lhr.uk'},
                u'simple-device:state': {u'domain-name': u'', u'hostname': u''}})

    del server_ph

  def test_003_handle_get_multiple_paths(self):
    server_ph = YANGPathHelper()
    s = simple_device(path_helper=server_ph)

    s.system.config.hostname = "rtr0.lhr.uk"
    s.system.config.domain_name = "test.jiveip.net"
    s.system.ntp.config.enabled = True

    get_msg = PyNMSClientGRPCMethods.generate_get_message(["/system/config", "/system/config/hostname"], 0)
    ret_msg = PyNMSServerGRPCMethods.service_get_request(get_msg, server_ph)

    self.assertEqual(ret_msg.request_id, 0)
    self.assertEqual(ret_msg.response_code, 0)
    self.assertEqual(len(ret_msg.response), 2)

    expected_results = [
                          ("/system/config", {u'simple-device:hostname': u'rtr0.lhr.uk', u'simple-device:domain-name': u'test.jiveip.net'}),
                          ("/system/config/hostname", u'rtr0.lhr.uk')
                       ]
    for returned,expected in zip(ret_msg.response, expected_results):
      self.assertEqual(returned.path, expected[0])
      err = None
      try:
        json_returned = json.loads(returned.value)
      except Exception as e:
        err = e
      self.assertIsNone(err)
      self.assertEqual(json_returned, expected[1])

    del server_ph

  def test_004_handle_one_set_path(self):
    server_ph = YANGPathHelper()
    s = simple_device(path_helper=server_ph)

    c = simple_device()
    c.system.config.hostname = "rtr0.lhr.uk"
    c.system.config.domain_name = "test.jiveip.net"

    set_msg = PyNMSClientGRPCMethods.generate_set_message([PyNMSConfigOperation(c.system)])
    ret_msg = PyNMSServerGRPCMethods.service_set_request(set_msg, server_ph)

    self.assertEqual(ret_msg.request_id, 0)
    self.assertEqual(ret_msg.response_code, 0)
    self.assertEqual(pynms_rpc_pb2.RPCResponse.Name(ret_msg.response_code), 'OK')
    self.assertEqual(ret_msg.message, "")

    self.assertEqual(s.system.config.hostname, "rtr0.lhr.uk")
    self.assertEqual(s.system.config.domain_name, "test.jiveip.net")

    del server_ph

  def test_005_handle_multiple_set_path(self):
    server_ph = YANGPathHelper()
    s = simple_device(path_helper=server_ph)

    c = simple_device()
    c.system.config.hostname = "rtr0.lhr.uk"
    c.system.ntp.config.enabled = True
    operations = [
                    PyNMSConfigOperation(c.system.config),
                    PyNMSConfigOperation(c.system.ntp)
                 ]
    set_msg = PyNMSClientGRPCMethods.generate_set_message(operations, request_id=42)
    ret_msg = PyNMSServerGRPCMethods.service_set_request(set_msg, server_ph)

    self.assertEqual(ret_msg.request_id, 42)
    self.assertEqual(ret_msg.response_code, 0)
    self.assertEqual(pynms_rpc_pb2.RPCResponse.Name(ret_msg.response_code), 'OK')
    self.assertEqual(ret_msg.message, "")

    self.assertEqual(s.system.config.hostname, "rtr0.lhr.uk")
    self.assertEqual(s.system.ntp.config.enabled, True)

    del server_ph


  def test_006_handle_scalar_set_operation(self):
    server_ph = YANGPathHelper()
    s = simple_device(path_helper=server_ph)

    c = simple_device()
    c.system.config.hostname = "rtr0.lhr.uk"

    operations = [PyNMSConfigOperation(c.system.config.hostname)]
    set_msg = PyNMSClientGRPCMethods.generate_set_message(operations, request_id=42)
    ret_msg = PyNMSServerGRPCMethods.service_set_request(set_msg, server_ph)

    self.assertEqual(ret_msg.request_id, 42)
    self.assertEqual(ret_msg.response_code, 0)
    self.assertEqual(pynms_rpc_pb2.RPCResponse.Name(ret_msg.response_code), 'OK')
    self.assertEqual(ret_msg.message, "")

    self.assertEqual(s.system.config.hostname, "rtr0.lhr.uk")

    del server_ph


  def test_007_handle_failed_transaction(self):
    server_ph = YANGPathHelper()
    s = simple_device(path_helper=server_ph)

    set_msg = self._build_invalid_set_message(42, [{"path": "/system/config/hostname", "json": "'rtr0.lhr.uk'"},
                                                   {"path": "/system/ntp/config", "json": {"config": {"enabled": 42}}}])
    ret_msg = PyNMSServerGRPCMethods.service_set_request(set_msg, server_ph)

    self.assertEqual(ret_msg.request_id, 42)
    self.assertEqual(ret_msg.response_code, 4)
    self.assertEqual(pynms_rpc_pb2.RPCResponse.Name(ret_msg.response_code), 'INVALID_CONFIGURATION')

    self.assertEqual(s.system.config.hostname, '')

    del server_ph

if __name__ == '__main__':
  T = unittest.main(exit=False)
  if len(T.result.errors) or len(T.result.failures):
    sys.exit(127)
  sys.exit(0)