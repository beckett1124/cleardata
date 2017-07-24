# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_vrs_bdid_map import media_vrs_bdid_map_client
from data_class.media_ott_file_id_map import ott_file_id_map_client
from rule.dict_page.dict_ott_cid import dict_ott_cid


class MediaOttBDCid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaOttBDCid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(plid|bdid)
        :return: plid
        """
        if len(field) < 1:
            return [1, "input_err"]

        # 默认plid为bd_id

        _res = ott_file_id_map_client.pid_to_int_pid([field[0]])
        bd_id = _res[1][0]

        if len(field) >= 2 and str(field[1]).isdigit():
            _res = media_vrs_bdid_map_client.check_bd_id([field[1]])

            # 上报的bdid是正确后，替换原bdid
            if _res[0] == 0:
                bd_id = str(field[1])

        if bd_id.isdigit() and bd_id != "0":
            _cid_res = media_vrs_bdid_map_client.get_fstlvlid_by_bd_id([bd_id])
            if _cid_res[0] != 0:
                return [0, "-1"]
            else:
                bd_cid_id = str(_cid_res[1])
                if bd_cid_id in dict_ott_cid.keys():
                    return [0, dict_ott_cid[bd_cid_id]]
                else:
                    return [0, bd_cid_id]

        return [0, "-1"]