#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
import os
import subprocess
import threading
from loguru import logger
from datetime import datetime
from utils.tool import Tool


class CommandExecutionException(Exception):
    def __init__(self, cmd: str, exit_code: int) -> None:
        super().__init__(f"command executed fail with exit-code={exit_code}: {cmd}")


class TextReadLineThread(threading.Thread):
    def __init__(self, readline, callback, *args, **kargs) -> None:
        super().__init__(*args, **kargs)
        self.readline = readline
        self.callback = callback

    def run(self):
        for line in iter(self.readline, ""):
            if len(line) == 0:
                break
            self.callback(line)


class Execute:
    def __init__(self):
        self.cur_time = None
        self.end_time = None
        self.flags = '\n' + '*' * 80
        self.tool = Tool()

    def print_cmd(self, cmd):
        self.cur_time = self.tool.get_time_stamp()
        print(f"RUNNING AT {self.cur_time}:")
        cmd = self.flags + '\n' + cmd + self.flags
        return cmd

    # Execute, get output and don't know whether success or not
    def exec_popen(self, cmd):
        output = os.popen(f"bash -c '{cmd}'").readlines()
        return output

    def get_duration(self):
        time1 = datetime.strptime(self.cur_time, "%Y-%m-%d %H:%M:%S")
        time2 = datetime.strptime(self.end_time, "%Y-%m-%d %H:%M:%S")
        seconds = (time2 - time1).seconds
        return seconds

    def cmd_exec(self, cmd: str, ensure_success: bool=True, show: bool=True) -> int:
        if show: logger.info("executing command: {}".format(self.print_cmd(cmd)))

        process = subprocess.Popen(
            cmd,
            shell=True,
            text=True,
            executable="bash", 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )

        if show: logger.debug("started command")

        def log_warp(func):
            def _wrapper(line: str):
                return func("\t" + line.rstrip())
            return _wrapper

        read_stdout = TextReadLineThread(process.stdout.readline, log_warp(logger.info))
        read_stderr = TextReadLineThread(process.stderr.readline, log_warp(logger.warning))
        read_stdout.start()
        read_stderr.start()

        read_stdout.join()
        read_stderr.join()
        ret = process.wait()
        if show: logger.debug("process finish")

        logger.info("executed command with exit-code={}".format(ret))
        if ensure_success and ret != 0:
            raise CommandExecutionException(cmd=cmd, exit_code=ret)
        return ret

    # Execute, get whether success or not
    def exec_sys(self, cmd):
        cmd = self.tool.chomp_cmd(cmd)
        logger.info("executing command: {}".format(self.print_cmd(cmd)))
        state = os.system(f"bash -c '{cmd}'")
        self.end_time = self.tool.get_time_stamp()
        print(f"total time used: {self.get_duration()}s")
        if state:
            print(f"failed at {self.end_time}:{state}".upper())
            return False
        else:
            print(f"successfully executed at {self.end_time}, congradulations!!!".upper())
            return True

    def exec_raw(self, cmd, ensure_success=False, show=True):
        cmd = self.tool.chomp_cmd(cmd)
        state = self.cmd_exec(cmd, ensure_success, show)
        self.end_time = self.tool.get_time_stamp()
        if state:
            if show: print(f"failed at {self.end_time}:{state}".upper())
            return False
        else:
            if show: print(f"successfully executed at {self.end_time}, congradulations!!!".upper())
            return True
