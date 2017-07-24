# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_vrs_vid_map import media_vrs_vid_map_client
from data_class.media_cms_playlist_vid import media_cms_playlist_vid_map_client
from commonlib.common import is_mg_vod


class MediaVRSVts(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaVRSVts, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid)
        :return: vts
        """
        # cpn=3 个人点播 vts置为-1
        if len(field) == 2 and is_mg_vod(str(field[1])):
            return [0, -1]

        # 输入3个参数、[vid|mt|bid] bid=24.1.1.0 专题活动vv mt为2芒果直播媒资 vts置为-1
        if len(field) == 3 and str(field[2]) == "24.1.1.0" and str(field[1]) == "2":
            return [0, -1]

        # 当vid大于1亿时, 表示是关系id, 需要通过改id查询vid、bdid
        if str(field[0]).isdigit() and int(field[0]) > 100000000:
            _res = media_cms_playlist_vid_map_client.get_vid_by_rid([field[0]])

            if _res[0] == 0:
                field[0] = _res[1]
            else:
                return _res

        return media_vrs_vid_map_client.get_vts_by_vid([field[0]])

