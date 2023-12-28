#!/bin/bash

# 1. 安装nfs-utils和rpcbind
#yum install -y nfs-utils rpcbind

# 2. 启用nfs和rpcbind
#systemctl enable --now rpcbind
#systemctl enable --now nfs-server

# 3. 配置要共享的文件夹
mkdir -p /dssg/test/protocol_test/nfs_data
echo "/dssg/test/protocol_test/nfs_data *(rw,no_root_squash,sync)" >> /etc/exports

#此文件的配置格式为：<输出目录> [客户端1 选项（访问权限,用户映射,其他）] [客户端2 选项（访问权限,用户映射,其他）]
#rw   read-write，可读写；
#sync：文件同时写入硬盘和内存；
#async：文件暂存于内存，而不是直接写入内存；
#no_root_squash：NFS客户端连接服务端时如果使用的是root的话，那么对服务端分享的目录来说，也拥有root权限。显然开启这项是不安全的。
#root_squash：NFS客户端连接服务端时如果使用的是root的话，那么对服务端分享的目录来说，拥有匿名用户权限，通常他将使用nobody或nfsnobody身份；
#all_squash：不论NFS客户端连接服务端时使用什么用户，对服务端分享的目录来说都是拥有匿名用户权限；
#anonuid：匿名用户的UID值，通常是nobody或nfsnobody，可以在此处自行设定；
#anongid：匿名用户的GID值。
exportfs -r

# 4. 列出nfs共享目录
showmount -e localhost

# 5. 挂载nfs
mkdir /mnt/nfs
mount -t nfs localhost:/dssg/test/protocol_test/nfs_data /mnt/nfs
