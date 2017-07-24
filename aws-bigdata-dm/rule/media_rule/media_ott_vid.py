# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_ott_file_id_map import ott_file_id_map_client
from data_class.media_mg_mediaid_map import media_mg_media_id_client
from data_class.media_vrs_vid_map import media_vrs_vid_map_client


class MediaOttVid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaOttVid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid)
        :return: vid
        """

        if len(field) == 4:
            res41 = ott_file_id_map_client.get_ott41__vid(field)
            if res41[0] == 1:
                return res41
            if res41[0] == 0:
                res = ott_file_id_map_client.to_int_vid([res41[1]])
            elif res41[0] == 2:
                res = ott_file_id_map_client.to_int_vid([field[0]])
         # 长度为5，走5.0媒资逻辑
        elif len(field) == 5:
            cpn = str(field[1])
            clientver = str(field[2])
            vid = str(field[3])
            pt = str(field[4])

            # 个人点播, 走芒果媒资
            if cpn == "3" or pt == "5":
                return media_mg_media_id_client.get_mid_by_media_id([field[0]])

            if clientver.startswith("5."):
                return media_vrs_vid_map_client.check_vid([vid])
            else:
                res = ott_file_id_map_client.to_int_vid([vid])

        else:
            res = ott_file_id_map_client.to_int_vid(field)

        if res[0] == 0 and len(res[1]) > 0 and res[1][0].isdigit():
            if res[1][0] == 0:
                return [0, '\N']
            else:
                return [0, res[1][0]]
        else:
            return res

        # return ott_file_id_map_client.to_int_vid(field)
