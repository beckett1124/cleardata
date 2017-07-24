# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00


class GlobalVar(object):
    """
    传递全局变量
    """
    def __init__(self):
        self.process_time = ""

    def set_global_process_time(self, input_time):
        self.process_time = input_time[0:10]

    def get_global_process_time(self):
        return self.process_time

global_var_client = GlobalVar()