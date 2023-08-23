#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
import os
import sys
from utils.tool import Tool
from utils.execute import Execute
from utils.app import App
from setting import ROOT_DIR, HPCbench_BENCHMARK


class Run:
    def __init__(self):
        self.app = App()
        self.exe = Execute()
        self.tool = Tool()
        self.hosts_list = self.tool.gen_list(App.hosts)

    def gen_hostfile(self, nodes):
        length = len(self.hosts_list)
        if nodes > length:
            print(f"You don't have {nodes} nodes, only {length} nodes available!")
            sys.exit()
        if nodes <= 1:
            return
        gen_nodes = '\n'.join(self.hosts_list[:nodes])
        print(f"HOSTFILE GENERATED:\n{gen_nodes}\n")
        self.tool.write_file('hostfile', gen_nodes)

    # single run
    def run(self):
        print(f"Start run {App.app_name}")
        nodes = int(App.run_cmd['nodes'])
        self.gen_hostfile(nodes)
        run_cmd = self.app.get_run_cmd()
        print(run_cmd)
        self.exe.exec_raw(run_cmd)

    def batch_run(self):
        batch_file = os.path.join(ROOT_DIR, 'batch_run.sh')
        print(f"Start batch run {App.app_name}")
        cmd = f'''\
            {self.app.get_env()}
            \ncd {App.case_dir}
            \n{App.batch_cmd}
        '''
        batch_content = self.tool.chomp_cmd(cmd)
        self.tool.write_file(batch_file, batch_content)
        run_cmd = f'''\
            chmod +x {batch_file}
            bash {batch_file}
        '''
        self.exe.exec_sys(run_cmd)

    def job_run(self):
        print(f"Start job run {App.app_name}")
        jobs_dir = HPCbench_BENCHMARK+'/jobs'
        self.tool.mkdirs(jobs_dir)
        for i, job_cmd in enumerate(App.job_cmd):
            job_file = os.path.join(jobs_dir, f'job_{App.app_name}_run{i}.sh')
            cmd = f'''\
                {job_cmd}
            '''
            job_content = self.tool.chomp_cmd(cmd)
            self.tool.write_file(job_file, job_content)
            run_cmd = f'''\
                {self.app.get_env()}
                sbatch {job_file}
            '''
            self.exe.exec_raw(run_cmd)

