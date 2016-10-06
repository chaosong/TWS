#!/usr/bin/env bash
DIR=$(dirname $(readlink -nf $0))
export HOME=$(readlink -nf ${DIR}/../)

python ${HOME}/src/main.py