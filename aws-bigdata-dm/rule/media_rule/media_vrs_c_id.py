# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_vrs_fstlvlid_map import media_vrs_fstlvlid_map_client
from commonlib.common import get_version_num
from rule.media_rule.media_cid import MediaCid
from rule.dict_page.dict_mpp_cid import dict_mpp_cid
from rule.dict_page.dict_mpp_cid import mpp_cid
from commonlib.common import is_mg_vod


class MediaVRSCid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaVRSCid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field cid|cpn|clientver|vid
        :return: cid
        """
        # cpn=3 个人点播 cid置为9999
        if len(field) >= 2 and is_mg_vod(str(field[1])):
            return [0, 9999]

        # 版本校验 MPP

        # phone 版本5.0.0 以下 通过vid反查
        if len(field) == 4:
            _ver = str(field[2]).lower()
            if "iphone" in _ver or "aphone" in _ver:
                _re_version_num = get_version_num(_ver)

                if _re_version_num[0] != 0:
                    return MediaCid().convert([field[3]])

                # 待核查确认是否是500
                if _re_version_num[1] < 500 or str(field[1]) == "-":
                    if "iphone-4.9.9" not in _ver:
                        return MediaCid().convert([field[3]])
            else:
                return MediaCid().convert([field[3]])

        if len(field) == 0:
            return [1, "INPUT_FAILED"]
        if field[0] in dict_mpp_cid.keys():
            return [0, dict_mpp_cid[field[0]]]
        elif field[0] in mpp_cid:
            return [0, field[0]]
        else:
            return media_vrs_fstlvlid_map_client.check_fstlvl_id([field[0]])

