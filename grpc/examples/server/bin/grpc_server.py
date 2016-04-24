#!/usr/bin/env python

from pyangbind.lib.xpathhelper import YANGPathHelper
from pyangbind.lib.yangtypes import safe_name
from pynms_grpc.server.pynms_grpc_server import PyNMSGRPCServer
import yaml
import importlib
import sys
import os

class PyNMSServerExampleException(Exception):
  pass

class PyNMSServerExample(object):
  def __init__(self, module_cfg):
    try:
      self._modcfg = yaml.load(open(module_cfg, 'r'))
    except IOError:
      raise PyNMSServerExampleException("Configuration file did not exist")
    self._yph = YANGPathHelper()
    self.load_modules()

  def load_modules(self):
    """
      Dynamically import the bindings modules that are specified in the
      configuration file.
    """
    imports = []
    for module in self._modcfg['modules']:
      if not module['python_module'] in imports:
        imports.append(module['python_module'])

    for modimport in imports:
      globals()[modimport] = importlib.import_module(modimport)

    for mod in self._modcfg['modules']:
      ymod_cls = getattr(globals()[mod['python_module']], safe_name(mod['yang_module']), None)
      if ymod_cls is None:
        raise PyNMSServerExampleException("Cannot load module %s from bindings" % safe_name(mod['yang_module']))
      print "Registering %s->%s" % (ymod_cls, mod)
      ymod_cls(path_helper=self._yph)

  def run(self):
    """
      Run the example server.
    """
    netelem = PyNMSGRPCServer(path_helper=self._yph)
    netelem.serve()

if __name__ == '__main__':
  cfg = os.path.realpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "etc", "modules.yml"))
  app = PyNMSServerExample(cfg)
  app.run()