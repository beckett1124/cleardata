# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_ott_file_id_map import ott_file_id_map_client


class MediaOttSeriesid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaOttSeriesid, self).__init__()

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
        else:
            res = ott_file_id_map_client.to_int_vid(field)

        # res = ott_file_id_map_client.to_int_vid(field)
        if res[0] != 0:
            return res

        return ott_file_id_map_client.get_series_id_by_vid(res[1])

