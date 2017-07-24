# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from rule.dict_page.dict_mpp_cid import dict_mpp_cid
from data_class.media_vrs_vid_map import media_vrs_vid_map_client
from commonlib.common import is_mg_vod


class MediaVRSCidByVid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaVRSCidByVid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field vid|cpn
        :return: cid
        """
        # cpn=3 个人点播 cid置为9999
        if len(field) == 2 and is_mg_vod(str(field[1])):
            return [0, 9999]

        # 输入3个参数、[vid|mt|bid] bid=24.1.1.0 专题活动vv mt为2芒果直播媒资 vts置为-1
        if len(field) == 3 and str(field[2]) == "24.1.1.0":
            if str(field[1]) == "2":
                return [0, 9999]
            else:
                return media_vrs_vid_map_client.get_fstlvlid_by_vid([field[0]])

        _res = media_vrs_vid_map_client.get_fstlvlid_by_vid([field[0]])

        if _res[0] == 0:
            cid = str(_res[1])
            if cid in dict_mpp_cid.keys():
                return [0, dict_mpp_cid[cid]]
            else:
                return [0, cid]
        else:
            return _res

