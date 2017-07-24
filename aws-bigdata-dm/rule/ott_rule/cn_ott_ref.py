#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-19T21:03:53+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-20T18:17:58+08:00
from rule.rule import rule
from rule.dict_page.dict_ott_page_type import ott_page_id_type
from rule.dict_page.dict_ott_page_type import ott_page
from data_class.media_vrs_cid_for_client import media_vrs_cid_for_client_map_client
from data_class.media_vrs_vid_map import media_vrs_vid_map_client


class cn_ott_ref(rule):
    '''
    :MAC的URL换算
    '''

    def __init__(self):
        pass

    def convert(self,fields):
        '''
        :MAC URL 换算
        '''
        if len(fields) != 2:
            return [1, "input_error"]
        else:
            if fields[0] is None or fields[0] == "" or fields[0] == "-":
                return [0, ""]
            else:
                _res_cpn = ott_page.get(fields[0])
                if _res_cpn is None or len(_res_cpn) == 0:
                    return [0, "未知"]
                else:
                    _res_cpn_type_id = ott_page_id_type.get(fields[0])

                    if _res_cpn_type_id is None or _res_cpn_type_id == "":
                        return [0, _res_cpn[0]]
                    else:
                        if _res_cpn_type_id == "app_cid":
                            if fields[1] is None or fields[1] == "":
                                return [1, "CPNID_NO_VALUE"]
                            _res = media_vrs_cid_for_client_map_client.get_c_name_by_cid_for_client([fields[1]])
                        elif _res_cpn_type_id == "vid":
                            if str(fields[1]).isdigit():
                                _res = media_vrs_vid_map_client.get_v_name_by_vid([fields[1]])
                            else:
                                return [0, _res_cpn[0]]
                        else:
                            _res = [4, "FPNID_TYPE_UNKWON"]

                        if _res[0] == 0:
                            return [0, _res_cpn[0] + "||" + _res[1]]
                        else:
                            return [1, _res[1]]
