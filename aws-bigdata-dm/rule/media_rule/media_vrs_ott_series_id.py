# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_vrs_seriesid_map import media_vrs_seriesid_map_client
from rule.media_rule.media_ott_series_id import MediaOttSeriesid


class MediaVRSOttSeriesId(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaVRSOttSeriesId, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(series_id)
        :return: series_id
        """
        if len(field) == 2 and str(field[1]).isdigit():
            return media_vrs_seriesid_map_client.check_series_id([field[1]])
        else:
            _res = MediaOttSeriesid().convert([field[0]])

            # 芒果媒资 返回-1
            if _res[0] != 0:
                return [0, -1]

            return _res


