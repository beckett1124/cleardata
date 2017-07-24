# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_vrs_clipid_map import media_vrs_clipid_map_client
from commonlib.common import get_version_num
from rule.media_rule.media_plid import MediaPLid
from commonlib.common import is_mg_vod


class MediaVRSClipId(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaVRSClipId, self).__init__()

    def convert(self, field):
        """
        :param field:  input field plid|cpn|clientver|vid
        :return: clip_id
        """

        # cpn=3 个人点播 plid置为-1
        if len(field) >= 2 and is_mg_vod(str(field[1])):
            return [0, -1]

        # phone 版本5.0.0 以下 通过vid反查
        if len(field) == 4:
            _ver = str(field[2]).lower()
            if "iphone" in _ver or "aphone" in _ver:
                _re_version_num = get_version_num(_ver)

                if _re_version_num[0] != 0:
                    return MediaPLid().convert([field[3]])

                # 待核查确认是否是500
                if _re_version_num[1] < 500 or str(field[1]) == "-":
                    if "iphone-4.9.9" not in _ver:
                        return MediaPLid().convert([field[3]])
            else:
                return MediaPLid().convert([field[3]])

        return media_vrs_clipid_map_client.check_clip_id([field[0]])
