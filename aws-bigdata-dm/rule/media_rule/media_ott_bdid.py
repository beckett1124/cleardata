# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_ott_file_id_map import ott_file_id_map_client
from data_class.media_vrs_bdid_map import media_vrs_bdid_map_client


class MediaOTTBDid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaOTTBDid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(plid|bd_id)
        :return: bd_id
        """

        # 对于老版本，获取播单id，通过传入[plid, bd_id] list 来通过vid获取bdid

        # 当传入参数大于1个时,先使用上报bdid查询
        if len(field) >= 2 and str(field[1]).isdigit():
            _res = media_vrs_bdid_map_client.check_bd_id([field[1]])

            if _res[0] == 0:
                return _res

        # 当上报一个参数，或者上报bdid无效时,通过plid字段获取
        _res = ott_file_id_map_client.pid_to_int_pid([field[0]])
        _res_ch = media_vrs_bdid_map_client.check_bd_id(_res[1])

        if _res_ch[0] == 0:
            return _res_ch
        else:
            return [0, "-1"]

