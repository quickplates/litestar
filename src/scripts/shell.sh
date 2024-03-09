#!/bin/bash

# Activate runtime shell
# shellcheck source=/dev/null
. /env/activate

/bin/bash -c "$*"
