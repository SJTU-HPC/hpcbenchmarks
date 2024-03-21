#!/bin/bash

## User environment
#module purge
#module load openmpi/4.0.3-gcc-10.3.1
export UCX_NET_DEVICES=mlx5_0:1
export OMPI_MCA_btl=self,vader,tcp

## Cluster info
export CLUSTER_NAME=kp920
export GPU_PARTITION=asend01
export CPU_PARTITION=arm128c256g
export PARA_STORAGE_PATH=/lustre
export TOTAL_NODES=5
# A computing node's total cores
export CPU_MAX_CORES=128
# A computing node's power (W)
export CLUSTER_POWER=314.25
# The storage system total power (KW)
export STORAGE_POWER=192
# need testing
export CLUSTER_BURSTBUFFER=111616
export BW_BURSTBUFFER=12100.38

## Defult setting 
CUR_PATH=$(pwd)
export HPCbench_ROOT=${CUR_PATH}
export HPCbench_COMPILER=${CUR_PATH}/software/compiler
export HPCbench_MPI=${CUR_PATH}/software/mpi
export HPCbench_LIBS=${CUR_PATH}/software/libs
export HPCbench_UTILS=${CUR_PATH}/software/utils
export HPCbench_DOWNLOAD=${CUR_PATH}/downloads
export HPCbench_MODULES=${CUR_PATH}/software/modulefiles
export HPCbench_MODULEDEPS=${CUR_PATH}/software/moduledeps
export HPCbench_BENCHMARK=${CUR_PATH}/benchmark
export HPCbench_TMP=${CUR_PATH}/tmp
export HPCbench_RESULT=${CUR_PATH}/result
export DOWNLOAD_TOOL=${CUR_PATH}/package/common/download.sh
export CHECK_DEPS=${CUR_PATH}/package/common/check_deps.sh
export CHECK_ROOT=${CUR_PATH}/package/common/check_root.sh
export gcc_version_number=$(gcc --version |grep GCC | awk '{ match($0, /[0-9]+\.[0-9]+\.[0-9]+/, version); print version[0] }')
export arch=$(lscpu |grep Architecture|awk '{print $2}')
export HADOOP_DATA=${CUR_PATH}/benchmark/storage/protocol/hadoop_data

mkdir -p tmp downloads software
if [ ! -d benchmark ];then
        mkdir -p benchmark/AI benchmark/compute benchmark/jobs benchmark/network benchmark/storage/ior benchmark/storage/protocol
fi
if [ ! -d result ];then
        mkdir -p result/AI result/balance result/compute result/network result/storage/ior result/storage/protocol result/system
fi
