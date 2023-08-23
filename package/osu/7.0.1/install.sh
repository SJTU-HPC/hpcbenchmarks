#!/bin/bash
set -x
set -e
. ${DOWNLOAD_TOOL} -u  http://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-7.0.1.tar.gz -f osu-micro-benchmarks-7.0.1.tar.gz
cd ${HPCbench_TMP}
tar -xvf ${HPCbench_DOWNLOAD}/osu-micro-benchmarks-7.0.1.tar.gz
cd osu-micro-benchmarks-7.0.1/
./configure --prefix=$1 CC=mpicc CXX=mpicxx
make
make install
