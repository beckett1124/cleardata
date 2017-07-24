# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_vrs_bdid_map import media_vrs_bdid_map_client
from data_class.media_cms_playlist_vid import media_cms_playlist_vid_map_client


class MediaVRSBDid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaVRSBDid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(bd_id)
        :return: bd_id
        """

        # 对于老版本，获取播单id，通过传入[bdid,vid] list 来通过vid获取bdid

        # 当vid大于1亿时, 表示是关系id, 需要通过改id查询vid、bdid
        if len(field) == 2 and str(field[1]).isdigit() and int(field[1]) > 100000000:
            _res = media_cms_playlist_vid_map_client.get_playlist_id_by_rid([field[1]])

            if _res[0] == 0:
                field[0] = _res[1]
            else:
                return _res
        return media_vrs_bdid_map_client.check_bd_id([field[0]])

