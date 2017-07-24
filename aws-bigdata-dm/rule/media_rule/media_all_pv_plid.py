# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from rule.media_rule.media_plid import MediaPLid
from data_class.media_vrs_clipid_map import media_vrs_clipid_map_client


class MediaAllPvPlid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaAllPvPlid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid|plid)
        :return: plid
        """
        if len(field) != 2:
            return [1, "INUT_ERR"]

        if str(field[0]) == "-" or str(field[0]) == "" or str(field[0]) == "0":
            return [0, '-1']
        if str(field[0]).isdigit():
            _res = MediaPLid().convert([field[0]])
            if _res[0] != 0:
                return media_vrs_clipid_map_client.check_clip_id([field[1]])
            else:
                return _res
        else:
            return [0, -1]

