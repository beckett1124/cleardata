# encoding: utf-8
from rule.rule import rule


class cn_border_bid(rule):
    '''
    :换算日志的BID
    '''

    def __init__(self):
        pass

    def convert(self, client):
        '''
        :根据 clienttp输出BID字段
        '''

        if len(client) != 1:
            return [1, "input_error"]

        client_str = client[0]

        if client_str.find("mobile-android") >= 0 or client_str.find("aphone") >= 0:
            return [0, 9]
        elif client_str.find("pad-ios") >= 0 or client_str.find("ipad") >= 0:
            return [0, 11]
        elif client_str.find("pcclient-macosx") >= 0 or client_str.find("macclient") >= 0:
            return [0, 6]
        elif client_str.find("phonem") >= 0:
            return [0, 4]
        elif client_str.find("ott") >= 0:
            return [0, 1]
        elif client_str.find("pcweb") >= 0:
            return [0, 2]
        elif client_str.find("pcclient-windows") >= 0 or client_str.find("pcclient") >= 0:
            return [0, 8]
        elif client_str.find("pad-android") >= 0:
            return [0, 10]
        elif client_str.find("mobile-ios") >= 0 or client_str.find("iphone") >= 0:
            return [0, 12]
        elif client_str.find("mui") >= 0:
            return [0, 13]
        else:
            return [0, '-1']
