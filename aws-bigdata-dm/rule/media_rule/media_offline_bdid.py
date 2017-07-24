# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_vrs_bdid_map import media_vrs_bdid_map_client
from data_class.media_cms_playlist_vid import media_cms_playlist_vid_map_client


class MediaOfflineBDid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaOfflineBDid, self).__init__()

    def convert(self, field):
        """
        用于移动端离线 通过fpid是否大于99990000
        :param field:  input field data(fpid|vid|bdid)
        :return: plid
        """
        if len(field) < 3:
            return [1, "input_err"]

        if str(field[2]).isdigit() and str(field[2]) != "0":
            return media_vrs_bdid_map_client.check_bd_id([field[2]])

        if str(field[0]).isdigit() and int(field[0]) > 99990000:
            # 当查不到时，可能为关系id，获取播单id
            _res = media_vrs_bdid_map_client.check_bd_id([field[0]])
            if _res[0] != 0:
                _res = media_cms_playlist_vid_map_client.get_playlist_id_by_rid([field[0]])

                if _res[0] == 0:
                    return media_vrs_bdid_map_client.check_bd_id([_res[1]])
                else:
                    return _res
            else:
                return _res

        if str(field[1]).isdigit() and int(field[1]) > 100000000:
            _res = media_cms_playlist_vid_map_client.get_playlist_id_by_rid([field[1]])

            if _res[0] == 0:
                return media_vrs_bdid_map_client.check_bd_id([_res[1]])
            else:
                return _res
        else:
            return [0, "-1"]

