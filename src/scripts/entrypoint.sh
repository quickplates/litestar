#!/bin/bash

# Activate runtime shell
# shellcheck source=/dev/null
. /env/activate

# Set permissions
chown -R app: /app/

# Activate virtual environment
# shellcheck source=/dev/null
. .venv/bin/activate

export PYTHONPATH="${VIRTUAL_ENV:?}/${PYTHON_SITE_PACKAGES:?}:${PYTHONPATH:-}"

# Run as non-root user
# Use tini to handle signals
exec su-exec app tini -- "$@"
