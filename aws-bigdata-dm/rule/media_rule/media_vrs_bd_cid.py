# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_vrs_bdid_map import media_vrs_bdid_map_client
from rule.dict_page.dict_ott_cid import dict_ott_cid
from rule.dict_page.dict_mpp_cid import dict_mpp_cid


class MediaVrsBDCid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaVrsBDCid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(bdid|clienttp)
        :return: plid
        """
        if len(field) < 2:
            return [1, "input_err"]

        client = str(field[1])

        if str(field[0]).isdigit() and str(field[0]) != "0":
            cid_res = media_vrs_bdid_map_client.get_fstlvlid_by_bd_id([field[0]])

            if client in ["ott", "mui", "tvos"]:
                cid_dict = dict_ott_cid
            else:
                cid_dict = dict_mpp_cid

            if cid_res[0] != 0:
                return [0, "-1"]
            else:
                cid = str(cid_res[1])
                if cid in cid_dict.keys():
                    return [0, cid_dict[cid]]
                else:
                    return [0, cid]

        return [0, "-1"]