#!/bin/bash
#循环遍历脚本入参，查看是否存在
if [ $# -eq 0 ];then
  echo "Usage: $0 para1 para2"
  exit 1
fi
flag=0
result=''
echo "Start checking dependency..."
for i in $*        #在$*中遍历参数，此时每个参数都是独立的，会遍历$#次
do
   result=$(env|grep $i)
   if [ -z "$result" ];then
        echo "Please load $i first."
        flag=1
   else
        echo "$i detected."
   fi
done

if [ $flag == 0 ]; then
   echo 'CHECK SUCCESS'
else
   echo 'CHECK FAILED'
   exit 1
fi