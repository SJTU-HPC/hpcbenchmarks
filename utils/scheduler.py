#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
import argparse

from setting import IS_SMALL, IS_MEDIUM, IS_LARGE, IS_WINDOWS
from loguru import logger

from utils.app import App
from utils.machine import Machine
from utils.config import Config
from utils.download import Download
from utils.install import Install
from utils.build import Build
from utils.invoke import Run
from utils.score import get_score

if IS_WINDOWS:
    raise Exception("Sorry, not supported platform!")

class Scheduler:
    def __init__(self, args):
        self.machine = Machine()
        self.config = Config()
        self.download = Download()
        self.install = Install()
        self.build = Build()
        self.run = Run()
        self.app = App()
        self.args = args

    def main(self):
        if self.args.version:
            print("v1.0")
        
        if self.args.info:
            self.machine.output_machine_info()

        if self.args.list:
            self.install.list()

        if self.args.download:
            self.download.download()
        
        if self.args.depend:
            self.install.install_depend()

        if self.args.install:
            self.install.install(self.args.install)
        
        if self.args.remove:
            self.install.remove(self.args.remove[0])
        
        if self.args.find:
            self.install.find(self.args.find[0])
        
        if self.args.env:
            self.app.source_env()

        if self.args.clean:
            self.build.clean()

        if self.args.build:
            self.build.build()

        if self.args.job:
            self.run.job_run()

        if self.args.run:
            self.run.run()

        if self.args.rbatch:
            self.run.batch_run()
        
        if self.args.use:
            self.config.switch_config(self.args.use[0])

        if self.args.update:
            self.install.update()
        
        if self.args.check:
            self.install.check_download_url()

        if self.args.score:
            get_score()
