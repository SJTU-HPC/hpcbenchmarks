#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
from utils.app import App
from utils.execute import Execute
from utils.tool import Tool


class Build:
    def __init__(self):
        self.app = App()
        self.exe = Execute()
        self.tool = Tool()

    def clean(self):
        print(f"Start clean {App.app_name}")
        cmd = f'''\
            {self.app.get_env()}
            \ncd {App.build_dir}
            \n{App.clean_cmd}
        '''
        clean_cmd = self.tool.chomp_cmd(cmd)
        clean_file = 'clean.sh'
        self.tool.write_file(clean_file, clean_cmd)
        run_cmd = f'''\
            chmod +x {clean_file}
            bash ./{clean_file}
        '''
        self.exe.exec_raw(run_cmd)

    def build(self):
        print(f"Start build {App.app_name}")
        cmd = f'''\
            {self.app.get_env()}
            \ncd {App.build_dir}
            \n{App.build_cmd}
        '''
        build_cmd = self.tool.chomp_cmd(cmd)
        build_file = 'build.sh'
        self.tool.write_file(build_file, build_cmd)
        run_cmd = f'''\
            chmod +x {build_file}
            bash ./{build_file}
        '''
        self.exe.exec_raw(run_cmd)

