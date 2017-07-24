# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_iphone_version import media_iphone_ver_client


class MediaPhoneVersionId(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaPhoneVersionId, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid)
        :return: vid
        """
        return media_iphone_ver_client.get_ver_id_by_version(field)

