# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_vrs_seriesid_map import media_vrs_seriesid_map_client
from data_class.media_vrs_vid_map import media_vrs_vid_map_client


class MediaVRSSeriesIdByVid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaVRSSeriesIdByVid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(series_id)
        :return: series_id
        """
        if len(field) == 2 and str(field[1]).isdigit():
            return media_vrs_seriesid_map_client.check_series_id([field[1]])
        else:
            if str(field[0]).isdigit():
                _res = media_vrs_vid_map_client.get_seriesid_by_vid([field[0]])
                if _res[0] != 0:
                    return [0, '\N']
                else:
                    return _res
            else:
                # vid非int, 则为芒果直播media_id或者无效vid,直接置为-1
                return [0, -1]


