#!/bin/bash
download_path=$HPCbench_DOWNLOAD
type_=wget
url=
filename=
OPTIND=1

while getopts ":u:f:t:" opt;
do
        case $opt in
                #下载的链接
                u) url=$OPTARG;;
                #使用的下载类型，默认wget
                t) type_=$OPTARG;;
                #下载后重命名,可不添加
                f) filename=$OPTARG;;
                ?) echo -e "\033[0;31m[Error]\033[0m:Unknown parameter:"$opt
                   exit 0;;
        esac

done

if [ ! "$url" ];then
        echo "Error: No available download link found"
        exit 0
fi
#如果需要重命名，则修改exist
if [ "$filename" ];then
        exist_path=$download_path/$filename
else
        if [ "$type_" == "git" ];then
                url=$(echo $url|sed 's/\.[^./]*$//')
        fi
        exist_path=$download_path/${url##*/}
fi

#判断文件是否存在
if [ ! -e $exist_path ];then
        if [ "$type_" == "wget" ];then
                echo -e "\033[0;32m[Info]\033[0m:Using commands: wget $url -O $exist_path --no-check-certificate"
                wget $url -O $exist_path --no-check-certificate || rm -rf $exist_path
        elif [ "$type_" == "git" ];then
                echo -e "\033[0;32m[Info]\033[0m:Using commands: git clone $url $exist_path"
                git clone $url $exist_path
        else
                echo -e "\033[0;31m[Error]\033[0m:Unsupported download mode:"$type_
                exit 0
        fi

        #下载失败
        if [ $? != 0 ];then
                rm -rf $exist_path
                echo -e "\033[0;31m[Error]\033[0m:Download failed:"$url
                exit 0
        fi
else
        echo -e "\033[0;32m[Info]\033[0m:"$exist_path" already exist"
fi
