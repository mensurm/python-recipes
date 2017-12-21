#!/bin/bash

set -o errexit   # Exit on error
set -o pipefail  # On pipeline fail, the failing command return status is used

ARGS=$@

if [ ! -z "$VIRTUAL_ENV" ]; then
    echo "Please deactivate the running virtualenv ($VIRTUAL_ENV) first"
    exit 1
fi

if [ -z "$PIP_CACHE" -a -d /tmp ]
then
    [ -d /tmp/pip_cache ] || mkdir -p /tmp/pip_cache
    PIP_CACHE="/tmp/pip_cache"
fi

venvdir="python"
rm -rf ${venvdir}
virtualenv ${PYTHON:+ -p "$PYTHON"} --distribute ${VE_CACHE:+ --extra-search-dir=$VE_CACHE} $@ ${venvdir}  || exit 1
. ${venvdir}/bin/activate

pip install -r requirements.txt -r requirements.dev.txt || exit 1

echo "To switch to the development environment type:"
echo "$ . ${venvdir}/bin/activate"
echo "In order to exit, type:"
echo "$ deactivate"
