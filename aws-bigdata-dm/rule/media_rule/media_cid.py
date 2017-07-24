# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_mpp_cms_id_map import mpp_cms_id_map_client
from data_class.media_cms_playlist_vid import media_cms_playlist_vid_map_client
from commonlib.common import is_mg_vod


class MediaCid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaCid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid)
        :return: plid
        """
        if len(field) < 1:
            return [1, "input_err"]

        # cpn=3 个人点播 cid置为9999
        if len(field) >= 2 and is_mg_vod(str(field[1])):
            return [0, 9999]

        # 当vid大于1亿时, 表示是关系id, 需要通过改vid反查cid
        if str(field[0]).isdigit() and int(field[0]) > 100000000:
            _res = media_cms_playlist_vid_map_client.get_vid_by_rid([field[0]])

            if _res[0] == 0:
                field[0] = _res[1]
            else:
                return _res

        _res = mpp_cms_id_map_client.get_c_id_by_vid([field[0]])
        if _res[0] != 0:
            return [0, "-1"]
        else:
            return _res