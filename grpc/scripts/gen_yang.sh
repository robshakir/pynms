#!/bin/bash
SDIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYBINDPLUGIN=`/usr/bin/env python -c 'import pyangbind; import os; print "%s/plugin" % os.path.dirname(pyangbind.__file__)'`
pyang --plugindir $PYBINDPLUGIN -f pybind -p $SDIR/../pynms_grpc/common/yang \
      --split-class-dir $SDIR/../pynms_grpc/common/ybind \
      --use-xpathhelper \
      $SDIR/../pynms_grpc/common/yang/simple-device.yang
