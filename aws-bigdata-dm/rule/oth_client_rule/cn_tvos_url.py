# encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-19T22:10:43+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-20T18:16:56+08:00
from rule.rule import rule
from rule.dict_page.dict_tvos_page_type import dict_tvos_page_type
from rule.dict_page.dict_tvos_page_type import dict_tvos_page_id
from rule.media_rule.media_vrs_vid_name import MediaVrsVidName


class cn_tvos_url(rule):

    def __init__(self):
        pass

    def convert(self, fields):
        '''
        :URL 换算
        '''
        if len(fields) != 2:
            return [1, "input_error"]
        else:
            if fields[0] is None or fields[0] == "":
                return [0, "\N"]
            else:
                _res_cpn = dict_tvos_page_type.get(fields[0])
                if _res_cpn is None or _res_cpn == "":
                    return [0, "未知"]
                else:
                    _res_cpn_type_id = dict_tvos_page_id.get(fields[0])

                    if _res_cpn_type_id is None or _res_cpn_type_id == "":
                        return [0, _res_cpn]
                    else:

                        if fields[1] is None or fields[1] == "":
                            return [0, _res_cpn]

                        if _res_cpn_type_id == "vid":
                            _res = MediaVrsVidName().convert([fields[1]])
                        else:
                            _res = [4, "FPNID_TYPE_UNKWON"]

                        if _res[0] == 0:
                            return [0, _res_cpn+"||"+_res[1]]
                        else:
                            return [1, _res[1]]
