#!/bin/bash
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

export GPU_PARTITION=a100
export CPU_PARTITION=64c512g 
export CPU_MAX_CORES=64
export CLUSTER_SCALE=small
export CLUSTER_POWER=10000
export STORAGE_POWER=10000
export CLUSTER_HPL=10000
export CLUSTER_BURSTBUFFER=111616
export TOTAL_NODES=900
export PARA_STORAGE_PATH=/mnt/f
export BW_BURSTBUFFER=12100.38
export HADOOP_DATA=${CUR_PATH}/benchmark/storage/protocol/hadoop_data

mkdir -p tmp downloads 
if [ ! -d benchmark ];then
	mkdir -p benchmark/AI benchmark/compute benchmark/jobs benchmark/network benchmark/storage/ior benchmark/storage/protocol
fi
if [ ! -d result ];then
	mkdir -p result/AI result/balance result/compute result/network result/storage/ior result/storage/protocol result/system
fi

module purge
module load gcc openmpi