# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_ott_file_id_map import ott_file_id_map_client
from data_class.media_vrs_clipid_map import media_vrs_clipid_map_client


class MediaOttPid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaOttPid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid)
        :return: vid
        """
        if len(field) == 4:
            res41 = ott_file_id_map_client.get_ott41__vid(field)
            if res41[0] == 1:
                return res41
            elif res41[0] == 0:
               res = ott_file_id_map_client.to_int_vid([res41[1]])
            elif res41[0] == 2:
               res = ott_file_id_map_client.to_int_vid([field[0]])

        # 长度为5，走5.0媒资逻辑
        elif len(field) == 5:
            pid = str(field[0])
            cpn = str(field[1])
            clientver = str(field[2])
            vid = str(field[3])
            pt = str(field[4])

            # 个人点播 pid置为-1
            if cpn == "3":
                return [0, -1]

            # 个人媒资轮播,pid置为-1
            if pt == "5":
                return [0, -1]

            if clientver.startswith("5."):
                return media_vrs_clipid_map_client.check_clip_id([pid])
            else:
                res = ott_file_id_map_client.to_int_vid([vid])
        else:
            res = ott_file_id_map_client.to_int_vid(field)

        #res = ott_file_id_map_client.to_int_vid(field)
        if res[0] != 0:
            return res

        return ott_file_id_map_client.get_pid_by_vid(res[1])

