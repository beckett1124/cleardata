#encoding: utf-8
# @Author: gibbs
# @Date:   2016-09-08
# @Last modified by:   gibbs
# @Last modified time: 2016-09-08
from rule.rule import rule
from rule.dict_page.dict_country import dict_country


class cn_country(rule):
    """
    :换算市列表
    """

    def __init__(self):
        pass

    def convert(self, fields):
        """
        :根据名称换算ID
        """
        if len(fields) != 1:
            return [1, "input_error"]
        else:
            if fields[0] is None or fields[0] == "" or fields[0] == "*":
                return [0, dict_country.get("未知")]
            else:
                country_id = dict_country.get(fields[0])
                if country_id is None:
                    return [0, dict_country.get("未知")]
                else:
                    return [0, country_id]
