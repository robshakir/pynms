#!/bin/bash
SDIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYBINDPLUGIN=`/usr/bin/env python -c 'import pyangbind; import os; print "%s/plugin" % os.path.dirname(pyangbind.__file__)'`
pyang --plugindir $PYBINDPLUGIN -f pybind -p $SDIR/common/yang \
      --split-class-dir $SDIR/common/ybind \
      --use-xpathhelper \
      $SDIR/common/yang/simple-device.yang