# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_mpp_app_cid import media_app_cid_client


class MediaAppCidName(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaAppCidName, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid)
        :return: plid
        """
        return media_app_cid_client.get_app_cid_name_by_cid(field)

