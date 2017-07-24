# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_vrs_seriesid_map import media_vrs_seriesid_map_client


class MediaVRSCheckSid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaVRSCheckSid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(bd_id)
        :return: bd_id
        """
        if len(field) == 1 and str(field[0]).isdigit():
            return media_vrs_seriesid_map_client.check_series_id(field)
        else:
            return [0, '-1']

