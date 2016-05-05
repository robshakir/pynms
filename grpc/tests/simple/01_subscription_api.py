
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

class PyNMSGPRC_SimpleMessage_SubscriptionTests(unittest.TestCase):

  def test_000_generate_subscribe_message(self):
    subsreq = pynms_rpc_pb2.SubscribeRequest(request_id=42)

    for host, port in [("192.0.2.1", 43), ("192.0.2.2", 1026)]:
      dest = subsreq.destination.add()
      dest.address = host
      dest.port = port

    for path in ["/bgp", "/system"]:
      pth = subsreq.paths.add()
      pth.path = path

    subsreq.sample_interval = 32
    subsreq.heartbeat_interval = 64
    subsreq.suppress_redundant = False
    subsreq.originated_qos_marking = 46
    subsreq.encoding = pynms_rpc_pb2.JSON_IETF

    return


if __name__ == '__main__':
  T = unittest.main(exit=False)
  if len(T.result.errors) or len(T.result.failures):
    sys.exit(127)
  sys.exit(0)