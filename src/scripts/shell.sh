#!/bin/bash

# Activate runtime shell
# shellcheck source=/dev/null
. /env/activate

# Activate virtual environment
# shellcheck source=/dev/null
. .venv/bin/activate

/bin/bash -c "$*"
