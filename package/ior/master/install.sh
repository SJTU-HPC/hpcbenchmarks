#!/bin/bash
set -x
set -e

#Download the IOR source:
git clone https://github.com/hpc/ior
#Compile the software:
cd ior
./bootstrap
./configure CC=mpicc --prefix=$1

make
make install
