#!/bin/bash
set -x
set -e
. ${DOWNLOAD_TOOL} -u https://github.com/xianyi/OpenBLAS/archive/refs/tags/v0.3.18.tar.gz -f OpenBLAS-0.3.18.tar.gz
cd ${HPCbench_TMP}
rm -rf OpenBLAS-0.3.18
tar -xzvf ${HPCbench_DOWNLOAD}/OpenBLAS-0.3.18.tar.gz
cd OpenBLAS-0.3.18
make -j 
make PREFIX=$1 install
