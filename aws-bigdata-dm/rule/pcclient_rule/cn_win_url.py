# encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-19T22:10:43+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-20T18:16:56+08:00
from rule.rule import rule
from rule.dict_page.dict_win_pagename import dict_win_page_id
from rule.dict_page.dict_win_pagename import dict_win_page_type
from rule.media_rule.media_vrs_vid_name import MediaVrsVidName
from data_class.media_cms_cid_name_map import mpp_cms_cid_name_map_client
from data_class.media_vrs_fstlvlid_map import media_vrs_fstlvlid_map_client


class cn_win_url(rule):

    def __init__(self):
        pass

    def convert(self,fields):
        '''
        :URL 换算
        '''
        if len(fields)!=2:
            return [1,"input_error"]
        else:
            if fields[0] is None or fields[0]=="":
                return [1,"input_error_cpn"]
            else:
                _res_cpn=dict_win_page_type.get(fields[0])
                if _res_cpn is None or _res_cpn=="":
                    return [0, "未知"]
                else:
                    _res_cpn_type_id=dict_win_page_id.get(fields[0])

                    if _res_cpn_type_id is None or _res_cpn_type_id=="":
                        return [0,_res_cpn]
                    else:
                        # 如果FPNID没有值 如果为离线播放(5005) 返回type_name 其它报错
                        if str(fields[0]) == "5005":
                            if fields[1] is None or fields[1] == "":
                                return [0, _res_cpn]
                        else:
                            if fields[1] is None or fields[1] == "":
                                return [1, "CPNID_NO_VALUE"]

                        if _res_cpn_type_id == "cid":
                            #后续要加上
                            _res = mpp_cms_cid_name_map_client.get_c_name_by_cid([fields[1]])
                            if _res[0] != 0:
                                _res = media_vrs_fstlvlid_map_client.get_c_name_by_cid([fields[1]])
                        elif _res_cpn_type_id == "vid":
                            _res=MediaVrsVidName().convert([fields[1]])
                        else:
                            _res=[4,"FPNID_TYPE_UNKWON"]

                        if _res[0]==0:
                            return [0,_res_cpn+"||"+_res[1]]
                        else:
                            return [1,_res[1]]
