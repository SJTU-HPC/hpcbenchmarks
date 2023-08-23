#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
import argparse
from utils.scheduler import Scheduler

parser = argparse.ArgumentParser(description=f'please put me into CASE directory, used for App Compiler/Clean/Run',
            usage='%(prog)s [-h] [--build] [--clean] [...]')
parser.add_argument("-v","--version", help=f"get version info", action="store_true")
parser.add_argument("-use","--use", help="Switch config file...", nargs=1)
parser.add_argument("-i","--info", help=f"get machine info", action="store_true")
parser.add_argument("-l","--list", help=f"get installed package info", action="store_true")
parser.add_argument("-install","--install", help=f"install dependency", nargs='+')
parser.add_argument("-remove","--remove", help=f"remove software", nargs=1)
parser.add_argument("-find","--find", help=f"find software", nargs=1)
# dependency install
parser.add_argument("-dp","--depend", help=f"App dependency install", action="store_true")
parser.add_argument("-e","--env", help=f"set environment App", action="store_true")
parser.add_argument("-b","--build", help=f"compile App", action="store_true")
parser.add_argument("-cls","--clean", help=f"clean App", action="store_true")
parser.add_argument("-r","--run", help=f"run App", action="store_true")
parser.add_argument("-j","--job", help=f"run job App", action="store_true")
# batch run
parser.add_argument("-rb","--rbatch", help=f"run batch App", action="store_true")
# batch download
parser.add_argument("-d","--download", help="Batch Download...", action="store_true")
# update modulefile path
parser.add_argument("-u","--update", help="start update hpcbench...", action="store_true")
# check download url is good or not
parser.add_argument("-check","--check", help="start check hpcbench download url...", action="store_true")
parser.add_argument("-s","--score", help="Calculate the score and output benchmark report", action="store_true")
args = parser.parse_args()


if __name__ == '__main__':
    Scheduler(args).main()