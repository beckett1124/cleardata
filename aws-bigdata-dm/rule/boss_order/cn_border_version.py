# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_iphone_version import media_iphone_ver_client
from data_class.cn_ott_version import cn_ott_ver_client


class CnBOrderVersionId(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(CnBOrderVersionId, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(version|client)
        :return: vid
        """
        if len(field) != 2:
            return [1, "input_error"]

        version_str = str(field[0]).lower()
        client_str = str(field[1]).lower()

        if client_str == "ott":
            _res = cn_ott_ver_client.get_ver_id_by_version([version_str])
        else:
            _res = media_iphone_ver_client.get_ver_id_by_version(field, False)

        if _res[0] != 0:
            return [0, '-1']
        else:
            return _res

