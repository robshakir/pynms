#!/usr/bin/env python

from pynms_grpc.client.pynms_grpc_client import PyNMSGRPCClient
from pynms_grpc.client.client_common import PyNMSConfigOperation
from pynms_yang_examples.bindings import openconfig_interfaces
import sys
import json

def print_get(msg):
  for res in msg.response:
    print "%s\n------\n" % (res.path)
    print json.dumps(json.loads(res.value), indent=4)

def main():
  client = PyNMSGRPCClient('localhost', 50051)
  client.run()

  ocif = openconfig_interfaces()

  gi0 = ocif.interfaces.interface.add("gi0/0/0")
  subint0 = gi0.subinterfaces.subinterface.add(0)
  ip4 = subint0.ipv4.addresses.address.add("192.0.2.1")
  ip4.config.prefix_length = 24

  ip6 = subint0.ipv6.addresses.address.add("2001:db8::1")
  ip6.config.prefix_length = 64

  transaction = [PyNMSConfigOperation(ocif.interfaces, 'UPDATE_CONFIG')]
  msg = client.set_paths(transaction, request_id=41)

  if msg.response_code == 0:
    print "Successfully updated /interfaces!"

  print "Following set, interfaces content is"
  msg = client.get_paths(["/interfaces"],42)
  print_get(msg)

  sys.exit(0)

if __name__ == '__main__':
  main()