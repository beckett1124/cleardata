#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-18T16:31:57+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-20T18:13:34+08:00

from rule.rule import rule
from rule.dict_page.dict_mobile_page import mobile_page
from rule.dict_page.dict_mobile_page import mobile_page_id_type
from rule.dict_page.dict_ipad_page import ipad_page
from rule.dict_page.dict_ipad_page import ipad_page_id_type
from rule.media_rule.media_vrs_vid_name import MediaVrsVidName
from rule.media_rule.media_app_cid_name import MediaAppCidName
from rule.media_rule.media_app_zt_name import MediaAppZtName
from data_class.media_cms_cid_name_map import mpp_cms_cid_name_map_client
from data_class.media_live_source_id import media_live_source_id_client
from data_class.media_live_channel_id import media_live_channel_id_client
from data_class.cn_mobile_activity import cn_mobile_activity
from data_class.media_vrs_cid_for_client import media_vrs_cid_for_client_map_client
from data_class.media_vrs_fstlvlid_map import media_vrs_fstlvlid_map_client
from commonlib.common import get_version_num


class cn_mobile_url(rule):
    '''
    :Mobile REF转换类
    '''

    def __init__(self):
        pass

    def convert(self,fields):
        '''
        :Mobile REF转换类，FPN FPID,PT,VID,CHANNEL_ID,SOURCE_ID,VERSION 根据版本做对应的规则
        '''
        #FPN FPID为空
        if len(fields)<3:
            return [1,"input_error"]
        else:
            if fields[0] is None or fields[0]=="":
                return [2,"PARAM_FPN"]
            else:
                _ver = fields[2]
                if _ver is None:
                    return [1, "VERION"]

                if "pad" in str(_ver).lower():
                    device_name = "pad"
                    com_page = ipad_page
                    com_page_id_type = ipad_page_id_type
                else:
                    device_name = "phone"
                    com_page = mobile_page
                    com_page_id_type = mobile_page_id_type

                _page_type_name=com_page.get(fields[0])
                if _page_type_name is None or len(_page_type_name) < 1 or _page_type_name=="":
                    return [0,"未知"]
                else:
                    # 如果发现了页面类型,则需要看页面类型对应的ID是否需要进行转换，如果需要进行转换则进行换算
                    # 点播和PT为0,直播PT为4
                    _page_type_name = _page_type_name[0]

                    _page_type=com_page_id_type.get(fields[0])

                    if _page_type is None or _page_type=="":
                        return [0,_page_type_name]
                    else:
                        # 如果FPNID没有值 如果为离线播放(43) 返回type_name 其它报错
                        if str(fields[0]) == "43" or str(fields[0]) == "56":
                            if fields[1] is None or fields[1] == "":
                                return [0, _page_type_name]
                        else:
                            if fields[1] is None or fields[1] == "":
                                return [1,"CPNID_NO_VALUE"]

                        if _page_type=="app_cid":
                            _res=MediaAppCidName().convert([fields[1], device_name])
                            if _res[0] != 0:
                                _res = media_vrs_cid_for_client_map_client.get_c_name_by_cid_for_client([fields[1]])
                        elif _page_type=="cid":
                            #后续要加上
                            _res=mpp_cms_cid_name_map_client.get_c_name_by_cid([fields[1]])
                            if _res[0] != 0:
                                _res = media_vrs_fstlvlid_map_client.get_c_name_by_cid([fields[1]])
                        elif _page_type=="vid":
                            _res=MediaVrsVidName().convert([fields[1]])
                        elif _page_type=="source_id":
                            #直播,后续要加上
                            if _ver=="":
                                return [1,"VERION"]
                            else:
                                _ver = _ver.lower()
                                if _ver.find('iphone')>=0:
                                    # 针对42类型， >4.7.0 都通换source_ID换算,<=4.7.0是channel_ID
                                    if str(fields[0]) == "42":
                                        _re_version_num = get_version_num(_ver)
                                        if _re_version_num[0] == 0:
                                            if _re_version_num[1] < 470:
                                                _res = media_live_channel_id_client.get_channel_name_by_channel_id([fields[1]])
                                            else:
                                                _res = media_live_source_id_client.get_source_name_name_by_source_id([fields[1]])
                                        else:
                                            return _re_version_num
                                    else:
                                        _res = media_live_source_id_client.get_source_name_name_by_source_id([fields[1]])

                                elif _ver.find('aphone')>=0:
                                    _res=media_live_source_id_client.get_source_name_name_by_source_id([fields[1]])
                                elif _ver.find('pad')>=0:
                                    _res = media_live_source_id_client.get_source_name_name_by_source_id([fields[1]])
                                else:
                                    _res=[4,"VERSION_UNKOWN"]
                        elif _page_type=="ztid":
                            _res=MediaAppZtName().convert([fields[1], device_name])
                            if _res[0] != 0:
                                _res = media_vrs_cid_for_client_map_client.get_c_name_by_cid_for_client([fields[1]])
                        elif _page_type == "h5_url":
                            _res = cn_mobile_activity.get_activity_url(fields[1])
                        else:
                            _res=[4,"FPNID_TYPE_UNKWON"]
                        #判断值
                        if _res[0]==0:
                            if _page_type == "h5_url" and _res[1] == "":
                                return [0, _page_type_name]
                            else:
                                return [0,_page_type_name+"||"+_res[1]]
                        else:
                            return [1,_res[1]]
