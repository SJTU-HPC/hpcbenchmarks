HPCBench是一个高性能集群计算性能评测工具集，本评测工具集引入与使用场景相关的性能指标，通过综合评分方法，为集群的计算、存储、网络和效率等关键维度，分别给出评价分数。    
评测工具集准备了6大评测维度的工具模块，分别为：1.计算性能维度 2.AI计算性能 3.存储性能维度 4.网络性能维度 5.系统能效维度 6.系统平衡性维度    
用户可简单根据自己集群配置修改模板文件，即可对集群进行评测。

# 评测工具集使用方法
## 依赖环境
HPCBench在下列环境已通过测试：  
系统环境：CentOS7   
运行环境：Python3   
CPU : Intel(R) Xeon(R) Platinum 8358   
GPU ：NVIDIA A100   
编译器：GCC-11.2.0  
MPI：OpenMPI-4.1.1  
调度系统：slurm
## 安装HPCBench
可以使用以下命令将HPCBench仓库克隆到本地，并安装必须的依赖。
$ git clone
$ pip3 install -r requirements.txt
```    
项目文件夹内包含以下几个文件和目录：
```
#模块测试目录
benchmark 
#数据下载目录
downloads
#配置文件目录
templates
#测试结果目录
result
#软件安装目录
software
#初始环境文件
init.sh
#主程序
hpcbench
```
## 初始化环境
使用以下命令进行初始化环境操作：
```
$ source init.sh
```
用户需要根据具体集群配置简单修改初始环境文件，包括录入集群信息，以及调用GCC和OpenMPI命令
## 简单运行测试
初始化完后，就可以执行HPCBench的简单命令：
```
$ ./hpcbench -h
usage: hpcbench [-h] [--build] [--clean] [...]

please put me into CASE directory, used for App Compiler/Clean/Run

options:
  -h, --help            show this help message and exit
  -v, --version         get version info
  -use USE, --use USE   Switch config file...
  -i, --info            get machine info
  -l, --list            get installed package info
  -install INSTALL [INSTALL ...], --install INSTALL [INSTALL ...]
                        install dependency
  -remove REMOVE, --remove REMOVE
                        remove software
  -find FIND, --find FIND
                        find software
  -dp, --depend         App dependency install
  -e, --env             set environment App
  -b, --build           compile App
  -cls, --clean         clean App
  -r, --run             run App
  -j, --job             run job App
  -rb, --rbatch         run batch App
  -d, --download        Batch Download...
  -u, --update          start update hpcbench...
  -check, --check       start check hpcbench download url...
  -s, --score           Calculate the score and output benchmark report

```
## 模块测试示例
下面以``COMPUTE``测试模块中的``HPL``为例进行测试介绍，该模块以两节点，每节点64核心配置进行计算，用户可根据实际情况自行修改配置文件。
### 调用配置文件
```
./hpcbench -use templates/compute/hpl.linux64.config
Switch config file to templates/compute/hpl.linux64.config
Successfully switched. config file saved in file .meta
```
### 下载依赖文件
```
./hpcbench -d
```
### 安装依赖库
```
./hpcbench -dp
```
### 安装HPL
```
./hpcbench -b
```
### 提交作业
```
./hpcbench -j
```
### 查看测试结果
计算完成后，在result/compute路径下会生成hpl.txt文件,查看可得知浮点计算速度为6303Gflops，符合精度要求
```
$ tail -n30 result/compute/hpl.txt
Column=000175872 Fraction=99.6% Gflops=6.307e+03
Column=000176128 Fraction=99.7% Gflops=6.307e+03
Column=000176384 Fraction=99.9% Gflops=6.307e+03
==============================================================
T/V     N         NB     P     Q       Time      Gflops
--------------------------------------------------------------
WR00R2R4  176640 256    8     16      582.89    6.3037e+03
HPL_pdgesv() start time Tue Aug 22 00:24:39 2023

HPL_pdgesv() end time   Tue Aug 22 00:34:21 2023

--VVV--VVV--VVV--VVV--VVV--VVV--VVV--VVV--VVV--VVV--VVV--VVV--VVV--VVV--VVV-
Max aggregated wall time rfact . . . :               3.56
+ Max aggregated wall time pfact . . :               2.67
+ Max aggregated wall time mxswp . . :               2.50
Max aggregated wall time update  . . :             533.48
+ Max aggregated wall time laswp . . :              56.77
Max aggregated wall time up tr sv  . :               0.26
--------------------------------------------------------------
||Ax-b||_oo/(eps*(||A||_oo*||x||_oo+||b||_oo)*N)=   8.52254435e-04 ...... PASSED
===========================================================
```
## 完成所有模块测试
