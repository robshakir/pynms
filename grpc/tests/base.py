#!/usr/bin/env python

import importlib
import unittest
import sys

class PyNMSGPRC_BaseTests(unittest.TestCase):
  def test_000_import(self):
    for module in ["pyangbind", "pynms_grpc.server.server_common",
                   "pynms_grpc.client.client_common", "pynms_yang_examples"]:
      err = None
      try:
        globals()[module] = importlib.import_module(module)
      except ImportError as e:
        err = e
      self.assertIs(err, None)

if __name__ == '__main__':
  T = unittest.main(exit=False)
  if len(T.result.errors) or len(T.result.failures):
    sys.exit(127)
  sys.exit(0)