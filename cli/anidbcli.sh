#!/bin/bash

me="$(dirname $(readlink -nf $0))"

cd $me/../

source venv/bin/activate
./cli/anidbcli.py "$@"
