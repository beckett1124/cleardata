# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_vrs_bdid_map import media_vrs_bdid_map_client
from data_class.media_cms_playlist_vid import media_cms_playlist_vid_map_client
from rule.dict_page.dict_mpp_cid import dict_mpp_cid


class MediaOfflineCid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaOfflineCid, self).__init__()

    def get_cms_cid_by_bdid(self, bdid_list):
        _res_cid = media_vrs_bdid_map_client.get_fstlvlid_by_bd_id(bdid_list)

        if _res_cid[0] == 0:
            bd_cid_id = str(_res_cid[1])
            if bd_cid_id in dict_mpp_cid.keys():
                return [0, dict_mpp_cid[bd_cid_id]]
            else:
                return [0, bd_cid_id]
        else:
            return _res_cid

    def convert(self, field):
        """
        用于移动端离线 通过fpid是否大于99990000
        :param field:  input field data(fpid|vid|bdid)
        :return: plid
        """
        if len(field) < 3:
            return [1, "input_err"]

        if str(field[2]).isdigit() and str(field[2]) != "0":
            return self.get_cms_cid_by_bdid([field[2]])

        if str(field[0]).isdigit() and int(field[0]) > 99990000:
            # 当查不到时，可能为关系id，获取播单id
            _res = media_vrs_bdid_map_client.check_bd_id([field[0]])
            if _res[0] != 0:
                _res = media_cms_playlist_vid_map_client.get_playlist_id_by_rid([field[0]])

                if _res[0] == 0:
                    return self.get_cms_cid_by_bdid([_res[1]])
                else:
                    return _res
            else:
                return self.get_cms_cid_by_bdid([_res[1]])

        if str(field[1]).isdigit() and int(field[1]) > 100000000:
            _res = media_cms_playlist_vid_map_client.get_playlist_id_by_rid([field[1]])

            if _res[0] == 0:
                return self.get_cms_cid_by_bdid([_res[1]])
            else:
                return _res
        else:
            return [0, "-1"]

