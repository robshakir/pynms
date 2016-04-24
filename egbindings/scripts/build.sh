#!/bin/bash

SDIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export PYANGPATH=`which pyang`
$SDIR/build_bindings.py