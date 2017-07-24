#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-18T14:20:17+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T15:28:03+08:00
from rule.rule import rule

class cn_bid(rule):
    '''
    :换算日志的BID
    '''

    def __init__(self):
        pass


    def convert(self,client):
        '''
        :根据 clienttp输出BID字段
        '''
        if len(client)!=1:
            return [1,"input_error"]

        if client[0].find("android")>=0 or client[0].find("aphone")>=0:
            return [0,9]
        elif client[0].find("ipad")>=0:
            return [0,11]
        elif client[0].find("macclient")>=0 or client[0].find("mac")>=0:
            return [0,6]
        elif client[0].find("phonem")>=0:
            return [0,4]
        elif client[0].find("ott")>=0:
            return [0,1]
        elif client[0].find("pcweb")>=0:
            return [0,2]
        elif client[0].find("mpp")>=0:
            return [0,0]
        elif client[0].find("pcclient")>=0:
            return [0,8]
        elif client[0].find("apad")>=0:
            return [0,10]
        elif client[0].find("iphone")>=0:
            return [0,12]
        elif client[0].find("padweb")>=0:
            return [0,5]
        elif client[0].find("mobile")>=0:
            return [0,3]
        elif client[0].find("win10client")>=0:
            return [0,7]
        elif client[0].find("tvos")>=0:
            return [0,13]
        elif client[0].find("weixin") >= 0:
            return [0, 14]
        else:
            return [1, 'NO_CLIENT']
