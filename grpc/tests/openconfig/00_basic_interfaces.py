#!/usr/bin/env python

import unittest
import sys
import logging
import json
from pynms_grpc.client.pynms_grpc_client import PyNMSGRPCClient
from pynms_grpc.client.client_common import PyNMSClientGRPCMethods, PyNMSConfigOperation
from pynms_grpc.server.server_common import PyNMSServerGRPCMethods
from pynms_grpc.common import pynms_rpc_pb2
from pynms_yang_examples.bindings import openconfig_interfaces
from pyangbind.lib.xpathhelper import YANGPathHelper
from pyangbind.lib.serialise import pybindIETFJSONEncoder

class PyNMSGPRC_OCMessageTests_Interfaces(unittest.TestCase):


  def test_000_set_interfaces(self):
    server_ph = YANGPathHelper()
    s = openconfig_interfaces(path_helper=server_ph)

    ocif = openconfig_interfaces()

    gi0 = ocif.interfaces.interface.add("gi0/0/0")
    subint0 = gi0.subinterfaces.subinterface.add(0)
    ip4 = subint0.ipv4.addresses.address.add("192.0.2.1")
    ip4.config.prefix_length = 24

    ip6 = subint0.ipv6.addresses.address.add("2001:db8::1")
    ip6.config.prefix_length = 64

    transaction = [PyNMSConfigOperation(ocif.interfaces, 'UPDATE_CONFIG')]
    logger = logging.getLogger('PyNMSGPRC_OCMessageTests_Interfaces')
    logger.addHandler(logging.NullHandler())

    set_msg = PyNMSClientGRPCMethods.generate_set_message(transaction)
    ret_msg = PyNMSServerGRPCMethods.service_set_request(set_msg, server_ph, logger=logger)

    # TODO assertions

    del server_ph

  def test_001_get_interfaces(self):
    server_ph = YANGPathHelper()
    s = openconfig_interfaces(path_helper=server_ph)

    gi0 = s.interfaces.interface.add(u"gi0/0/0")
    subint0 = gi0.subinterfaces.subinterface.add(0)
    ip4 = subint0.ipv4.addresses.address.add(u"192.0.2.1")
    ip4.config.prefix_length = 24

    ip6 = subint0.ipv6.addresses.address.add(u"2001:db8::1")
    ip6.config.prefix_length = 64

    logger = logging.getLogger('PyNMSGPRC_OCMessageTests_Interfaces')
    logger.addHandler(logging.NullHandler())

    get_msg = PyNMSClientGRPCMethods.generate_get_message(["/interfaces"], 42)
    ret_msg = PyNMSServerGRPCMethods.service_get_request(get_msg, server_ph, logger=logger)
    print ret_msg

    #
    # TODO: assertions
    #

    del server_ph

  def test_002_replace_interfaces(self):
    server_ph = YANGPathHelper()
    s = openconfig_interfaces(path_helper=server_ph)

    logger = logging.getLogger('PyNMSGPRC_OCMessageTests_Interfaces')
    logger.addHandler(logging.NullHandler())

    gi0 = s.interfaces.interface.add("gi0/0/0")
    subint0 = gi0.subinterfaces.subinterface.add(0)
    ip4 = subint0.ipv4.addresses.address.add("192.0.2.1")
    ip4.config.prefix_length = 24

    ocif = openconfig_interfaces()

    gi0 = ocif.interfaces.interface.add("gi0/0/0")
    subint0 = gi0.subinterfaces.subinterface.add(0)
    ip6 = subint0.ipv6.addresses.address.add("2001:db8::1")
    ip6.config.prefix_length = 64

    transaction = [PyNMSConfigOperation(ocif.interfaces, 'REPLACE_CONFIG')]
    set_msg = PyNMSClientGRPCMethods.generate_set_message(transaction)
    ret_msg = PyNMSServerGRPCMethods.service_set_request(set_msg, server_ph, logger=logger)

    print s.interfaces.get(filter=True)

    #
    # TODO: assertions
    #

  def test_003_delete_interface(self):
    server_ph = YANGPathHelper()
    s = openconfig_interfaces(path_helper=server_ph)

    logger = logging.getLogger('PyNMSGPRC_OCMessageTests_Interfaces')
    logger.addHandler(logging.NullHandler())

    gi0 = s.interfaces.interface.add(u"gi0/0/0")
    subint0 = gi0.subinterfaces.subinterface.add(0)
    ip4 = subint0.ipv4.addresses.address.add(u"192.0.2.1")
    ip4.config.prefix_length = 24

    logger = logging.getLogger('PyNMSGPRC_OCMessageTests_Interfaces')
    logger.addHandler(logging.NullHandler())

    ocif = openconfig_interfaces()
    gi0 = ocif.interfaces.interface.add(u"gi0/0/0")
    transaction = [PyNMSConfigOperation(gi0, 'DELETE_CONFIG')]
    set_msg = PyNMSClientGRPCMethods.generate_set_message(transaction)
    print set_msg
    ret_msg = PyNMSServerGRPCMethods.service_set_request(set_msg, server_ph, logger=logger)

    print s.interfaces.get(filter=True)


if __name__ == '__main__':
  T = unittest.main(exit=False)
  if len(T.result.errors) or len(T.result.failures):
    sys.exit(127)
  sys.exit(0)