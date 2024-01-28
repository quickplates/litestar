#!/bin/bash

# Activate runtime shell
# shellcheck source=/dev/null
. /env/activate

# Activate virtual environment
# shellcheck source=/dev/null
. .venv/bin/activate

export PYTHONPATH="${VIRTUAL_ENV:?}/${PYTHON_SITE_PACKAGES:?}:${PYTHONPATH:-}"

/bin/bash -c "$*"
