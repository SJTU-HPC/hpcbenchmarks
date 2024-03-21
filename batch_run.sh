source ./init.sh
./hpcbench -e
source ./env.sh

cd $HPCbench_ROOT

cd $RESULT_DIR
exec 1>$RESULT_DIR/system.log 2>/dev/null
# compute_efficiency
echo "Calculating Compute_Effiency"
CLUSTER_POWER=314.25 #w
TOTAL_NODES=5
TOTAL_CLUSTER_POWER=$(echo "scale=2; $CLUSTER_POWER*$TOTAL_NODES*0.875/1000"|bc)
CLUSTER_HPL=$(python -c "from utils.result import extract_pflops;print(extract_pflops('$HPCbench_ROOT/result/compute/hpl.txt'))") #Pflops
COMPUTE_EFFIENCY=$(echo "scale=2;$CLUSTER_HPL*1000/$TOTAL_CLUSTER_POWER"|bc)
echo COMPUTE_EFFIENCY=$COMPUTE_EFFIENCY
# IO_operation_rate
echo "Calculating IO_OPERATION_RATE"
IOPS=`cat $HPCbench_ROOT/result/storage/ior/iops.txt |grep write |awk 'NR==2 {print $3}'`
STORAGE_POWER=384
STORAGE_POWER=$(echo "scale=2; $STORAGE_POWER*0.8"|bc)
IO_operation_rate=$(echo "scale=2; $IOPS/$STORAGE_POWER/1000"|bc)
echo "IO_operation_rate=$IO_operation_rate"