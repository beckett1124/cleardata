#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-19T09:16:12+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-19T11:11:22+08:00
from rule.rule import rule
from rule.dict_page.dist_province import dist_province


class cn_province(rule):
    '''
    :将市份换算成ID
    '''


    def __init__(self):
        pass


    def convert(self,fields):
        '''
        :根据省份名称获取ID
        '''
        if len(fields)!=1:
            return [1,"input_error"]
        else:
            if fields[0] is None or fields[0]=="" or fields[0]=="*":
                return [0,dist_province.get("未知")]
            else:
                province_id=dist_province.get(fields[0])
                if province_id is None:
                    return [0,dist_province.get("未知")]
                else:
                    return [0,province_id]
