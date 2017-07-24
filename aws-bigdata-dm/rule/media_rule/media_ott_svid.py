# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_ott_cms_id_map import ott_cms_id_map_client


class MediaOttSVid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaOttSVid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid)
        :return: vid
        """
        return ott_cms_id_map_client.get_svid_by_vid(field)

