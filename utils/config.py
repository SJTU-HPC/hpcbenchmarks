#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
import os
from utils.app import App
from utils.execute import Execute
from utils.tool import Tool
from setting import ROOT_DIR

class Config:
    def __init__(self):
        self.exe = Execute()
        self.tool = Tool()
        self.meta_path = os.path.join(ROOT_DIR, App.meta_file)

    def switch_config(self, config_file):
        print(f"Switch config file to {config_file}")
        config_path = os.path.join(ROOT_DIR, config_file)
        if not os.path.isfile(config_path):
            print("config_path not found, switch failed.")
            return
        self.tool.write_file(self.meta_path, config_file.strip())
        print("Successfully switched. config file saved in file .meta")

