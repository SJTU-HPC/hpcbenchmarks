#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
import os
import re
import platform

from utils.tool import Tool
from loguru import logger
from setting import APP_CONFIG
from setting import ROOT_DIR
from utils.execute import Execute

class Singleton(type):

    def __init__(self, name, bases, dictItem):
        super(Singleton,self).__init__(name,bases, dictItem)
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super(Singleton,self).__call__(*args, **kwargs)
        return self._instance

class App(object, metaclass=Singleton):
    # Hardware Info
    hosts = ''

    # Dependent Info
    dependency = ''
    modules = ''
    env_file = 'env.sh'

    # Application Info
    app_name = ''
    build_dir = ''
    binary_dir =  ''
    case_dir = ''
    binary_file = ''
    binary_para = ''

    # CMD info
    build_cmd = ''
    clean_cmd = ''
    run_cmd = {}
    batch_cmd = ''
    job_cmd = []

    # Other Info
    config_file = 'data.config'
    meta_file = '.meta'
    download_list = ''

    def __init__(self):
        self.tool = Tool()
        self.exe = Execute()
        self.data_process()

    def get_abspath(self, file):
        return os.path.join(ROOT_DIR, file)

    '''
    APP_CONFIG -> .meta文件 -> data.config
    '''
    def get_config_file(self):
        if APP_CONFIG is not None:
            logger.info(f"Load Config file from ENV: {APP_CONFIG}")
            return APP_CONFIG
        if not os.path.exists(App.meta_file):
            return App.config_file
        return self.tool.read_file(App.meta_file)

    def get_config_data(self):
        config_file = self.get_config_file()
        file_path = self.get_abspath(config_file)
        if not os.path.exists(file_path):
            logger.info("config file not found, switch to default data.config.")
            file_path = self.get_abspath(App.config_file)
        with open(file_path, encoding='utf-8') as file:
            contents = file.read()
            return contents.strip()

    def is_empty(self, content):
        return len(content) == 0 or content.isspace() or content == '\n'

    def read_rows(self, rows, start_row, needs_strip=True):
        data = ''
        row = rows[start_row]
        if needs_strip:
            row = row.strip()
        while not row.startswith('['):
            if not self.is_empty(row):
                data += row + '\n'
            start_row += 1
            if start_row == len(rows):
                break
            row = rows[start_row]
            if needs_strip:
                row = row.strip()
        return start_row, data

    def read_rows_kv(self, rows, start_row):
        data = {}
        row = rows[start_row].strip()
        while not row.startswith('['):
            if '=' in row:
                key, value = row.split('=', 1)
                data[key.strip()] = value.strip()
            start_row += 1
            if start_row == len(rows):
                break
            row = rows[start_row].strip()
        return start_row, data

    def set_app_info(self, data):
        App.app_name = data['app_name']
        App.build_dir = data['build_dir']
        App.binary_dir = data['binary_dir']
        App.case_dir = data['case_dir']

    def split_two_part(self, data):
        split_list = data.split(' ', 1)
        first = split_list[0]
        second = ''
        if len(split_list) > 1:
            second = split_list[1]
        return (first, second)

    def data_integration(self, config_data):
        App.hosts = config_data.get('[SERVER]','')
        App.download_list = config_data.get('[DOWNLOAD]','')
        App.dependency = self.tool.chomp_cmd(config_data.get('[DEPENDENCY]',''), flag=False)
        App.modules = config_data.get('[ENV]','')
        App.build_cmd = config_data.get('[BUILD]','')
        App.clean_cmd = config_data.get('[CLEAN]','')
        App.run_cmd = config_data.get('[RUN]','')
        App.batch_cmd = config_data.get('[BATCH]','')
        data = config_data.get('[APP]','')
        self.set_app_info(data)
        App.binary_file, App.binary_para = self.split_two_part(App.run_cmd['binary'])

    def data_process(self):
        contents = self.get_config_data()
        rows = contents.split('\n')
        rowIndex = 0
        handlers = {
            '[SERVER]': lambda rows, rowIndex: self.read_rows(rows, rowIndex+1),
            '[DOWNLOAD]': lambda rows, rowIndex: self.read_rows(rows, rowIndex+1, False),
            '[DEPENDENCY]': lambda rows, rowIndex: self.read_rows(rows, rowIndex+1, False),
            '[ENV]': lambda rows, rowIndex: self.read_rows(rows, rowIndex+1),
            '[APP]': lambda rows, rowIndex: self.read_rows_kv(rows, rowIndex+1),
            '[BUILD]': lambda rows, rowIndex: self.read_rows(rows, rowIndex+1, False),
            '[CLEAN]': lambda rows, rowIndex: self.read_rows(rows, rowIndex+1),
            '[RUN]': lambda rows, rowIndex: self.read_rows_kv(rows, rowIndex+1),
            '[BATCH]': lambda rows, rowIndex: self.read_rows(rows, rowIndex+1, False),
        }
        config_data = {}
        while rowIndex < len(rows):
            row = rows[rowIndex].strip()
            if row in handlers.keys():
                rowIndex, config_data[row] = handlers[row](rows, rowIndex)
            else:
                rowIndex += 1
        self.data_integration(config_data)
        self.get_jobs(contents)

    def get_env(self):
        cmd = f'''
            source ./init.sh
            ./hpcbench -e
            source ./{App.env_file}
        '''
        return self.tool.chomp_cmd(cmd, flag=True)

    def source_env(self):
        print(f"Set environment for {App.app_name}")
        env_file = os.path.join(ROOT_DIR, App.env_file)
        self.tool.write_file(env_file, App.modules)
        print(f"ENV FILE {App.env_file} GENERATED.")
        self.exe.exec_raw(f'chmod +x {App.env_file}', show=False)

    def get_run_cmd(self):
        hostfile = ''
        nodes = int(App.run_cmd['nodes'])
        if nodes > 1:
            hostfile = f'--hostfile {ROOT_DIR}/hostfile'
        cmd = App.run_cmd['run']
        if 'mpi' in cmd:
            cmd = cmd.replace('mpirun', f'mpirun {hostfile}')
        binary = os.path.join(App.binary_dir, App.binary_file)
        cmd = f'{cmd} {binary} {App.binary_para}'
        cmd = f'''\
            {self.get_env()}
            \ncd {App.case_dir}
            \n{cmd}
        '''
        run_cmd = self.tool.chomp_cmd(cmd)
        return run_cmd

    def get_jobs(self, contents):
        pattern = re.compile(r'(^\[)', re.M)
        all_starts = [match.start() for match in pattern.finditer(contents)]
        start_tag = '[JOB'

        i = 1
        while True:
            job_start = contents.find(start_tag + str(i))
            if job_start == -1:
                break
            job_end = contents.find(start_tag + str(i+1))
            if job_end == -1:
                for k, index in list(map(lambda x: (x > job_start, all_starts.index(x)), all_starts)):
                    if k:
                        job_end = all_starts[index]
                        break
                    else:
                        job_end = len(contents)
            
            job_content = contents[job_start+len(start_tag + str(i))+1:job_end].strip()
            i += 1
            
            App.job_cmd.append(job_content)
