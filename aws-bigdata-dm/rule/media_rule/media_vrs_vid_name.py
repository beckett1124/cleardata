# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_vrs_vid_map import media_vrs_vid_map_client
from data_class.media_cms_playlist_vid import media_cms_playlist_vid_map_client
from data_class.media_mg_mediaid_map import media_mg_media_id_client


class MediaVrsVidName(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaVrsVidName, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid)
        :return: plid
        """
        if len(field) < 1:
            return [1, "input_err"]

        # 当vid大于1亿时, 表示是关系id, 需要通过改id查询vid、bdid
        if str(field[0]).isdigit() and int(field[0]) > 100000000:
            _res = media_cms_playlist_vid_map_client.get_vid_by_rid([field[0]])

            if _res[0] == 0:
                field[0] = _res[1]
            else:
                return _res
        _res = media_vrs_vid_map_client.get_v_name_by_vid(field)
        if _res[0] != 0:
            return media_mg_media_id_client.get_name_by_media_id(field)
        else:
            return _res

