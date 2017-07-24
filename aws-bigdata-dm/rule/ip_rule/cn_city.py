#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-19T09:16:52+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-19T11:07:11+08:00
from rule.rule import rule
from rule.dict_page.dist_city import dist_city


class cn_city(rule):
    '''
    :换算市列表
    '''


    def __init__(self):
        pass


    def convert(self,fields):
        '''
        :根据名称换算ID
        '''
        if len(fields)!=1:
            return [1,"input_error"]
        else:
            if fields[0] is None or fields[0]=="" or fields[0]=="*":
                return [0,dist_city.get("未知")]
            else:
                city_id=dist_city.get(fields[0])
                if city_id is None:
                    return [0,dist_city.get("未知")]
                else:
                    return [0,city_id]
