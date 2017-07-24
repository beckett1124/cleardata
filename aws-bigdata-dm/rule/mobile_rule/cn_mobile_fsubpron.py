#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-18T17:15:00+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-20T18:13:56+08:00

import re
import urllib

from rule.rule import rule
from rule.dict_page.dict_mobile_page import mobile_page
from rule.dict_page.dict_mobile_page import mobile_H5_pron_regex
from rule.dict_page.dict_mobile_page import mobile_pron_type
from rule.dict_page.dict_mobile_page import mobile_app_cid_map
from rule.dict_page.dict_mobile_page import mobile_pt_id_map


class cn_mobile_fsubpron(rule):
    '''
    :Mobile REF
    '''

    def __init__(self):
        pass

    def convert(self, fields):
        '''
        :Mobile ref_subpron转换类，FPN FPID PT根据版本做对应的规则
        '''
        #FPN FPID为空
        if len(fields) < 3:
            return [1, "input_error"]
        else:
            if fields[0] is None or fields[0] == "":
                return [0, "-1"]
            else:
                # 当cpn＝1 cpid=62 时，表示轮播/直播产品线 直接返回
                if str(fields[0]) == "1" and (str(fields[1]) == "62" or str(fields[1]) == "1011"):
                    return [0, 1000080]

                # 当cpn＝1 cpid=68 时，表示会员产品线 直接返回
                if str(fields[0]) == "1" and (str(fields[1]) == "68" or str(fields[1]) == "1024"):
                    return [0, 1000165]

                pron_type = mobile_pron_type.get(str(fields[0]))

                if pron_type is not None and pron_type == "app_cid_sub":
                    new_cid = mobile_app_cid_map.get(str(fields[1]))
                    if new_cid is None:
                        if str(fields[1]).isdigit():
                            return [0, fields[1]]
                        else:
                            return [0, "-1"]
                    else:
                        return [0, new_cid]

                if pron_type is not None and pron_type == "pt_sub":
                    # pt
                    if str(fields[2]).isdigit():
                        if len(fields) >= 4 and str(fields[3]) in ["imgotv-aphone-5.0.0_0_1", "imgotv-aphone-5.0.0_0_1.1"]:
                            if str(fields[2]) == "1":
                                fields[2] = "2"
                            elif str(fields[2]) == "2":
                                fields[2] = "1"
                        pt_id = mobile_pt_id_map.get(str(fields[2]))

                        # 不在展示列表中的pt 均算点播产品线 其他
                        if pt_id is None:
                            return [0, 1000170]
                        else:
                            return [0, pt_id]
                    else:
                        return [0, 1000170]

                # 56 特殊产品线
                if pron_type is not None and pron_type == "url_regex":
                    match_flag = False
                    pron = ""
                    for (key, value) in mobile_H5_pron_regex.items():
                        for regex in value:
                            pattern = re.compile(regex[0])
                            url_str = urllib.unquote(str(fields[1])).strip()
                            match = pattern.match(url_str)

                            if not match:
                                continue

                            match_flag = True
                            if len(regex) > 1:
                                pron = str(regex[1])
                            break

                        if match_flag:
                            if str(pron).isdigit():
                                return [0, pron]

                com_page = mobile_page

                _page_type_list = com_page.get(str(fields[0]))
                if _page_type_list is None or len(_page_type_list) < 3:
                    return [0, "-1"]
                else:
                    return [0, _page_type_list[2]]