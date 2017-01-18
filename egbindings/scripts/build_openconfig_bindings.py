#!/usr/bin/env python

import os
import sys
import pyangbind
import requests
import shutil

def main():
  this_dir = os.path.dirname(os.path.realpath(__file__))
  python_path = sys.executable
  pyangbind_path = "%s/plugin" % os.path.dirname(pyangbind.__file__)

  pyang_path = os.environ.get('PYANGPATH') if \
                os.environ.get('PYANGPATH') is not None else False

  if pyang_path is False:
    sys.stderr.write("FATAL:      Cannot find pyang")
    sys.exit(1)

  OC = "https://raw.githubusercontent.com/openconfig/" + \
            "public/master/release/models/"
  RFC = "https://raw.githubusercontent.com/robshakir/yang/master/"+ \
          "standard/ietf/RFC/"

  YANG_FILES = [
                    {
                      "type": "REMOTE",
                      "path": OC + "bgp/openconfig-bgp-common-multiprotocol.yang",
                      "dir": "openconfig"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "bgp/openconfig-bgp-common-structure.yang",
                      "dir": "openconfig"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "bgp/openconfig-bgp-common.yang",
                      "dir": "openconfig"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "bgp/openconfig-bgp-global.yang",
                      "dir": "openconfig"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "bgp/openconfig-bgp-neighbor.yang",
                      "dir": "openconfig"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "bgp/openconfig-bgp-peer-group.yang",
                      "dir": "openconfig"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "bgp/openconfig-bgp-policy.yang",
                      "dir": "openconfig"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "bgp/openconfig-bgp-types.yang",
                      "dir": "openconfig"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "bgp/openconfig-bgp.yang",
                      "dir": "openconfig"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "policy/openconfig-routing-policy.yang",
                      "dir": "openconfig"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "policy/openconfig-policy-types.yang",
                      "dir": "openconfig"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "openconfig-extensions.yang",
                      "dir": "include"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "openconfig-types.yang",
                      "dir": "include"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "interfaces/openconfig-interfaces.yang",
                      "dir": "openconfig"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "interfaces/openconfig-if-ip.yang",
                      "dir": "openconfig"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "interfaces/openconfig-if-ethernet.yang",
                      "dir": "openconfig"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "interfaces/openconfig-if-ip-ext.yang",
                      "dir": "openconfig"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "vlan/openconfig-vlan.yang",
                      "dir": "openconfig"
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "vlan/openconfig-vlan-types.yang",
                      "dir": "include",
                      "build": False,
                    },
                    {
                      "type": "REMOTE",
                      "path": OC + "interfaces/openconfig-if-aggregate.yang",
                      "dir": "openconfig"
                    },
                    {
                      "type": "REMOTE",
                      "path": RFC + "ietf-inet-types.yang",
                      "dir": "include",
                      "build": False,
                    },
                    {
                      "type": "REMOTE",
                      "path": RFC + "iana-if-type.yang",
                      "dir": "include",
                      "build": False,
                    },
                    {
                      "type": "REMOTE",
                      "path": RFC + "ietf-yang-types.yang",
                      "dir": "include",
                      "build": False,
                    },
                    {
                      "type": "REMOTE",
                      "path": RFC + "ietf-interfaces.yang",
                      "dir": "include",
                      "build": False,
                    },
                    {
                      "type": "LOCAL",
                      "file": "example/simple-device.yang"
                    }
                ]

  this_dir = os.path.dirname(os.path.realpath(__file__))
  files = []
  remove_dirs = []
  for fn in YANG_FILES:
    if fn['type'] == 'REMOTE':
      wrdir = os.path.realpath(os.path.join(this_dir, "..", fn['dir']))

      if not os.path.exists(wrdir):
        os.mkdir(wrdir)
        remove_dirs.append(wrdir)

      wrpath = os.path.join(this_dir, "..", fn['dir'], fn['path'].split("/")[-1])
      if not os.path.exists(wrpath):
        response = requests.get(fn['path'])
        assert response.status_code == 200, "Could not get %s" % fn['path']
        f = open(wrpath, 'w')
        f.write(response.content)
        f.close()

      if 'build' in fn:
        if fn['build'] is True:
          files.append(os.path.join(fn['dir'], fn['path'].split("/")[-1]))
      else:
        files.append(os.path.join(fn['dir'], fn['path'].split("/")[-1]))
    else:
        if 'build' in fn:
          if fn['build'] is True:
            files.append(fn['file'])
        else:
          files.append(fn['file'])

  files_str = " ".join([os.path.join(this_dir, "..", i) for i in files])

  for fn in os.listdir(os.path.realpath(os.path.join(this_dir, "..", "pynms_yang_examples"))):
    if not fn in ["__init__.py"]:
      path = os.path.realpath(os.path.join(this_dir, "..", "pynms_yang_examples", fn))

  cmd = "%s " % python_path
  cmd += "%s --plugindir %s" % (pyang_path, pyangbind_path)
  cmd += " -f pybind --split-class-dir %s" % os.path.realpath((os.path.join(this_dir, "..", "pynms_yang_examples", "bindings")))
  cmd += " -p %s" % os.path.join(this_dir, "..")
  cmd += " -p %s" % os.path.join(this_dir, "..", "include")
  cmd += " --use-xpathhelper"
  cmd += " "
  cmd += files_str
  os.system(cmd)

  for directory in remove_dirs:
    for fn in os.listdir(directory):
      os.remove(os.path.join(directory, fn))
    os.rmdir(directory)



if __name__ == '__main__':
  main()
