# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_app_zt_cms_id import media_app_zt_cms_id_client


class MediaAppZtName(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaAppZtName, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid)
        :return: plid
        """
        return media_app_zt_cms_id_client.get_zt_name_by_zt_id(field)

