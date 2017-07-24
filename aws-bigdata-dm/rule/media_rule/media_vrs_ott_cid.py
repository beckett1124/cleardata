# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_vrs_vid_map import media_vrs_vid_map_client
from rule.dict_page.dict_ott_cid import dict_ott_cid


class MediaVRSOttCid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaVRSOttCid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field vid
        :return: cid
        """
        res = media_vrs_vid_map_client.get_fstlvlid_by_vid([field[0]])

        if res[0] != 0:
            return [0, "-1"]
        else:
            cid = str(res[1])
            if cid in dict_ott_cid.keys():
                return [0, dict_ott_cid[cid]]
            else:
                return [0, cid]
