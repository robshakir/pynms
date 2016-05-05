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
  RFC = "https://raw.githubusercontent.com/YangModels/" + \
            "yang/master/standard/ietf/RFC/"
  CISCO = "https://raw.githubusercontent.com/YangModels/" + \
            "yang/master/vendor/cisco/xr/600/"

  YANG_FILES = [
                    {
                      "type": "REMOTE",
                      "path": RFC + "ietf-inet-types.yang",
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
                      "type": "LOCAL",
                      "file": "vendor/cisco/xr/openconfig-bgp/bgp.yang",
                    },
                    {
                      "type": "LOCAL",
                      "file": "vendor/cisco/xr/openconfig-bgp/bgp-types.yang",
                      "build": False,
                    },
                    {
                      "type": "LOCAL",
                      "file": "vendor/cisco/xr/openconfig-bgp/bgp-operational.yang",
                    },
                    {
                      "type": "LOCAL",
                      "file": "vendor/cisco/xr/openconfig-bgp/bgp-multiprotocol.yang",
                    },
                    {
                      "type": "REMOTE",
                      "path": CISCO + "cisco-xr-bgp-deviations.yang",
                      "dir": "ciscoxr",
                    },
                    {
                      "type": "LOCAL",
                      "file": "vendor/cisco/xr/openconfig-bgp/bgp-policy.yang",
                    },
                    {
                      "type": "LOCAL",
                      "file": "vendor/cisco/xr/openconfig-routing-policy/routing-policy.yang",
                    },
                    {
                      "type": "LOCAL",
                      "file": "vendor/cisco/xr/openconfig-routing-policy/policy-types.yang",
                      "build": False,
                    },
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
  cmd += " -f pybind --split-class-dir %s" % os.path.realpath((os.path.join(this_dir, "..", "pynms_yang_examples", "xrbindings")))
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
