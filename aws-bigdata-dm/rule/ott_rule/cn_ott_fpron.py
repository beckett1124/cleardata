#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-18T17:15:00+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-20T18:13:56+08:00

from rule.rule import rule
from rule.dict_page.dict_ott_page_type import ott_page
from rule.dict_page.dict_ott_page_type import ott_pron_type
from rule.dict_page.dict_ott_page_type import ott_so_cpid_map


class cn_ott_fpron(rule):
    '''
    :Mobile REF
    '''

    def __init__(self):
        pass

    def convert(self, fields):
        '''
        :OTT ref_pron转换类，FPN FPID 根据版本做对应的规则
        '''
        #FPN FPID为空
        if len(fields) < 2:
            return [1, "input_error"]
        else:
            if fields[0] is None or fields[0] == "":
                return [0, "-1"]
            else:
                # 当cpn＝A cpid=150 时，表示会员产品线 直接返回
                if str(fields[0]) == "A" and str(fields[1]) == "150":
                    return [0, 1000174]

                # 当cpn＝A cpid=59 时，表示s搜索产品线 直接返回
                if str(fields[0]) == "A" and str(fields[1]) == "59":
                    return [0, 1000143]

                # 当cpn＝A cpid=55 时，表示个人产品线 直接返回
                if str(fields[0]) == "A" and str(fields[1]) == "55":
                    return [0, 1000135]

                com_page = ott_page
                pron_type = ott_pron_type.get(str(fields[0]))

                if pron_type is not None and pron_type == "so_sub":
                    if str(fields[1]).isdigit():
                        so_id = ott_so_cpid_map.get(str(fields[1]))

                        if so_id is None:
                            return [0, -1]
                        else:
                            return [0, 1000143]
                    else:
                        return [0, -1]

                _page_type_list = com_page.get(str(fields[0]))
                if _page_type_list is None or len(_page_type_list) < 3:
                    return [0, "-1"]
                else:
                    return [0, _page_type_list[2]]