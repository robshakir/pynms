#!/usr/bin/env python

from pynms_grpc.client.cisco_grpc_client import CiscoGRPCClient
from pynms_grpc.client.client_common import PyNMSConfigOperation
from pynms_yang_examples.xrbindings import bgp
import sys
import json

def main():
  client = CiscoGRPCClient('198.18.1.12', 57344)
  client.run()

  client.get_paths(["/bgp"], 42)


if __name__ == '__main__':
  main()