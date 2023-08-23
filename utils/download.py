#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
import os
from utils.app import App
from utils.execute import Execute
from utils.tool import Tool
from setting import ROOT_DIR
from pprint import pprint

class Download:
    def __init__(self):
        self.app = App()
        self.exe = Execute()
        self.tool = Tool()
        self.download_list = self.tool.gen_list(App.download_list)
        self.download_path = os.path.join(ROOT_DIR, 'downloads')
        self.package_path = os.path.join(ROOT_DIR, 'package')

    def gen_wget_url(self, out_dir='./downloads', url='', filename=''):
        head = "wget --no-check-certificate"
        file_path = os.path.join(out_dir, filename)
        download_url = f'{head} {url} -O {file_path}'
        print(download_url)
        return download_url

    def download(self):
        print(f"start download")
        filename_url_map = {}
        self.tool.mkdirs(self.download_path)
        download_flag = False
        # create directory
        for url_info in self.download_list:
            url_list = url_info.split(' ')
            if len(url_list) < 2:
                continue
            url_link = url_list[1].strip()
            filename = os.path.basename(url_link)
            if len(url_list) == 3:
                filename = url_list[2].strip()
            filename_url_map[filename] = url_link
            
        pprint(filename_url_map)
        # start download
        for filename, url in filename_url_map.items():
            download_flag = True
            file_path = os.path.join(self.download_path, filename)
            if os.path.exists(file_path):
                self.tool.prt_content(f"FILE {filename} already DOWNLOADED")
                continue
            download_url = self.gen_wget_url(self.download_path, url, filename)
            self.tool.prt_content("DOWNLOAD " + filename)
            output = os.popen(download_url)
            data = output.read()
            output.close()

        if not download_flag:
            print("The download list is empty!")
