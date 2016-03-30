#!/bin/bash

SDIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
rm -rf $SDIR/../{build,dist,*.egg*}
