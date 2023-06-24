#!/bin/bash

# Activate runtime shell
# shellcheck source=/dev/null
. /env/activate

# Activate virtual environment
# shellcheck source=/dev/null
. .venv/bin/activate

# Run as non-root user
# Use tini to handle signals
su-exec app tini -s -- "$@"
