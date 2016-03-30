#!/bin/bash

SDIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Generate the protobuf bindings
$SDIR/../scripts/gen_proto.sh
# Generate the YANG bindings
$SDIR/../scripts/gen_yang.sh > /dev/null

(cd $SDIR/.. && python setup.py bdist_wheel > /dev/null)
(cd $SDIR && vagrant up)
