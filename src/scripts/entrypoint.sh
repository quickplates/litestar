#!/bin/bash

# Activate runtime shell
# shellcheck source=/dev/null
. /env/activate

# Run as non-root user
# Use tini to handle signals
exec su-exec service tini -- "$@"
