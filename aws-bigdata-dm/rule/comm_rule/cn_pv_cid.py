#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-18T16:31:57+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-20T18:13:34+08:00

from rule.rule import rule
from rule.dict_page.dict_mobile_page import mobile_page
from rule.dict_page.dict_mobile_page import mobile_page_id_type
from rule.dict_page.dist_mac_pagename import dist_mac_page_id
from rule.dict_page.dist_mac_pagename import dist_mac_page_type
from rule.dict_page.dist_win10_pagename import dist_win10_page_id
from rule.dict_page.dist_win10_pagename import dist_win10_page_type
from rule.dict_page.dict_win_pagename import dict_win_page_id
from rule.dict_page.dict_win_pagename import dict_win_page_type
from rule.dict_page.dict_ipad_page import ipad_page
from rule.dict_page.dict_ipad_page import ipad_page_id_type
from rule.dict_page.dict_mpp_cid import dict_mpp_cid

from rule.media_rule.media_vrs_cid_by_vid import MediaVRSCidByVid

dict_client_page = {
    "iphone": mobile_page,
    "aphone": mobile_page,
    "mac": dist_mac_page_type,
    "win10client": dist_win10_page_type,
    "pcclient": dict_win_page_type,
    "ipad": ipad_page
}
dict_client_page_id_type = {
    "aphone": mobile_page_id_type,
    "iphone": mobile_page_id_type,
    "mac": dist_mac_page_id,
    "win10client": dist_win10_page_id,
    "pcclient": dict_win_page_id,
    "ipad": ipad_page_id_type
}


class cn_pv_cid(rule):
    '''
    :PV CID转换类
    '''

    def __init__(self):
        pass


    def convert(self,fields):
        '''
        :PV CID转换类，CPN CPID CLIENTTP 根据不同端做对应的规则
        '''
        #FPN FPID为空
        if len(fields) < 3:
            return [1, "input_error"]
        else:
            if fields[0] is None or fields[0] == "" or fields[2] is None or fields[2] == "":
                return [2, "ERR_PARAM_PAGE_NUMBER"]
            else:
                if fields[2] in dict_client_page.keys():
                    _page_type_name = dict_client_page[fields[2]].get(fields[0])
                else:
                    return [1, "CLIENT_TYPE_NOT_INT_DICT"]

                if _page_type_name is None or _page_type_name == "":
                    return [0, "\N"]
                else:
                    # 如果发现了页面类型,则需要看页面类型对应的ID是否需要进行转换，如果需要进行转换则进行换算
                    # 点播和PT为0,直播PT为4
                    if fields[2] in dict_client_page_id_type.keys():
                        _page_type = dict_client_page_id_type[fields[2]].get(fields[0])
                    else:
                        return [1, "CLIENT_TYPE_NOT_INT_DICT_TYPE"]

                    if _page_type is None or _page_type == "":
                        return [0, '\N']
                    else:
                        # cpid为空时，cid\pid\vid置为 \N
                        if fields[1] is None or fields[1] == "" or str(fields[1]) == "0":
                            return [0, "\N"]

                        if _page_type == "vid":
                            _res = MediaVRSCidByVid().convert([fields[1]])
                        else:
                            return [0, "\N"]

                        if _res[0] == 0:
                            if _res[1] in dict_mpp_cid.keys():
                                return [0, dict_mpp_cid[_res[1]]]
                            return [0, _res[1]]
                        else:
                            return [0, "-1"]

