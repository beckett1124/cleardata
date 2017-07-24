# encoding: utf-8
# @Author: gibbs

from rule.rule import rule
from data_class.cn_mpp_channel import cn_mpp_channel_client
from data_class.cn_ott_version import cn_ott_ver_client


class CnBOrderChType(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(CnBOrderChType, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(cxid|client|version)
        :return: plid
        """

        if not isinstance(field, list) or len(field) != 3:
            return [1, "INPUT_FILED_ERR"]

        version_str = str(field[2]).lower()
        client_str = str(field[1]).lower()
        cxid_str = str(field[0]).lower().split('?')[0]

        if client_str == "pcweb":
            cxid_list = cxid_str.split("_")

            if len(cxid_list) > 1:
                cxid_str = cxid_list[1]

            if str(cxid_str).isdigit():
                cxid_str = ""

        if client_str != 'ott':
            _res = cn_mpp_channel_client.get_ch_type_by_source([cxid_str, client_str], 1, False)
        else:
            _res = cn_ott_ver_client.get_open_type_by_version([version_str])

        if _res[0] != 0:
            return [0, '\N']
        else:
            return _res



