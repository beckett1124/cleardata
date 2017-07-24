# encoding=utf-8
"""
Created on 2015年11月24日

@author: Administrator
"""
import os
import yaml

ServerConf = yaml.load(file(os.path.join(os.path.dirname(__file__), "../conf/service.yml")))

if __name__ == '__main__':
    dict_list = ServerConf["recv_file"]["recv_file_name"]
    print dict_list["msite_pv"]
