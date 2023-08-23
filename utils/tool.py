#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
import time
import os
import json
import re
import textwrap
from setting import HPCbench_RESULT, ROOT_DIR, GPU_PARTITION, CPU_PARTITION, CPU_MAX_CORES, HADOOP_DATA, \
    BW_BURSTBUFFER, PARA_STORAGE_PATH, TOTAL_NODES, CLUSTER_BURSTBUFFER, CLUSTER_POWER


class Dict(dict):

    def __getattr__(self, key):
        return self.get(key)

    def __setattr__(self, key, value):
        self[key] = value

def dict_to_obj(obj):
    if not isinstance(obj, dict):
        return obj
    d = Dict()
    for k, v in obj.items():
        d[k] = dict_to_obj(v)
    return d

class Tool:
    def __init__(self):
        pass
    
    def prt_content(self, content):
        flags = '*' * 30
        print(f"{flags}{content}{flags}")

    def gen_list(self, data):
        return data.strip().split('\n')
    
    def chomp_cmd(self, cmd, flag=True):
        if flag:
            cmd = textwrap.dedent(cmd)
        # cmd = re.sub(r'^ +', '',cmd, flags=re.MULTILINE)
        cmd = cmd.replace("{{ HPCbench_RESULT }}", HPCbench_RESULT)
        cmd = cmd.replace("{{ GPU_PARTITION }}", GPU_PARTITION)
        cmd = cmd.replace("{{ CPU_PARTITION }}", CPU_PARTITION)
        cmd = cmd.replace("{{ CPU_MAX_CORES }}", CPU_MAX_CORES)
        cmd = cmd.replace("{{ HADOOP_DATA }}", HADOOP_DATA)
        cmd = cmd.replace("{{ BW_BURSTBUFFER }}", BW_BURSTBUFFER)
        cmd = cmd.replace("{{ PARA_STORAGE_PATH }}", PARA_STORAGE_PATH)
        cmd = cmd.replace("{{ TOTAL_NODES }}", TOTAL_NODES)
        cmd = cmd.replace("{{ CLUSTER_BURSTBUFFER }}", CLUSTER_BURSTBUFFER)
        cmd = cmd.replace("{{ CLUSTER_POWER }}", CLUSTER_POWER)
        cmd = cmd.strip()
        return cmd

    def get_scale(self, hpl_score):
        CLUSTER_SCALE = None
        if hpl_score <= 10:
            CLUSTER_SCALE = 'small'
        elif hpl_score > 30:
            CLUSTER_SCALE = 'large'
        else:
            CLUSTER_SCALE = 'medium'
        return CLUSTER_SCALE

    def get_time_stamp(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    
    def read_file(self, filename):
        content = ''
        try:
            with open(filename, encoding='utf-8') as f:
                content = f.read().strip()
        except IOError:
            return content
        return content

    def read_lines(self, filename):
        content = ''
        try:
            with open(filename, encoding='utf-8') as f:
                content = f.readlines()
        except IOError:
            return content
        return content

    def write_file(self, filename, content=""):
        with open(filename,'w') as f:
            f.write(content)
    
    def mkdirs(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
    
    def mkfile(self, path, content=''):
        if not os.path.exists(path):
            self.write_file(path, content)

    def check_url_isvalid(self,url):
        import requests
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                return True
            else:
                return False
        except requests.exceptions.RequestException as e:
            return False


class JSON:
    def __init__(self, filename):
        self.filename = filename
        self.app = self.read_file()

    # 读取 JSON 文件
    def read_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                f.write('{}')
        with open(self.filename, "r") as file:
            data = json.load(file)
        return data

    # 写入 JSON 文件
    def write_file(self):
        with open(self.filename, "w") as file:
            json.dump(self.app, file, indent=4)

    # 查询数据
    def query_data(self, key):
        if key in self.app:
            return self.app[key]
        else:
            return None

    # 添加数据
    def add_data(self, key, value):
        self.app[key] = value

    # 删除数据
    def delete_data(self, key):
        if key in self.app:
            del self.app[key]
        else:
            print("Key not found")

    # 修改数据
    def update_data(self, key, value):
        if key in self.app:
            self.app[key] = value
        else:
            print("Key not found")

    def json_transform(self, dict):
        return json.dumps(dict)