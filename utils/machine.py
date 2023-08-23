#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
from utils.execute import Execute
from utils.tool import Tool

class Machine:
    def __init__(self):
        self.exe = Execute()
        self.tool = Tool()
        self.info2cmd = {
            'CHECK network adapter':'nmcli d',
            'CHECK Machine Bits':'getconf LONG_BIT',
            'CHECK OS':'cat /proc/version && uname -a',
            'CHECK GPU': 'lspci | grep -i nvidia',
            'CHECK Total Memory':'cat /proc/meminfo | grep MemTotal',
            'CHECK Total Disk Memory':'fdisk -l | grep Disk',
            'CHECK CPU info': 'cat /proc/cpuinfo | grep "processor" | wc -l && lscpu && dmidecode -t 4'
        }

    def get_info(self, content, cmd):
        self.tool.prt_content(content)
        self.exe.exec_raw(cmd)
    
    def output_machine_info(self):
        print("get machine info")
        for key, value in self.info2cmd.items():
            self.get_info(key, value)
