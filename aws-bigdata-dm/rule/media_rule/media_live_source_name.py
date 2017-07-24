# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_live_source_id import media_live_source_id_client


class MediaLiveSourceName(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaLiveSourceName, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid)
        :return: plid
        """
        return media_live_source_id_client.get_source_name_name_by_source_id(field)

