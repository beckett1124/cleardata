# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_cms_playlist_vid import media_cms_playlist_vid_map_client
from data_class.media_vrs_bdid_map import media_vrs_bdid_map_client
from rule.dict_page.dict_mpp_cid import dict_mpp_cid


class MediaBDCid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaBDCid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid|bdid)
        :return: plid
        """
        if len(field) < 2:
            return [1, "input_err"]

        if str(field[1]).isdigit() and str(field[1]) != "0":
            _cid_res = media_vrs_bdid_map_client.get_fstlvlid_by_bd_id([field[1]])
            if _cid_res[0] != 0:
                return _cid_res
            else:
                bd_cid_id = str(_cid_res[1])
                if bd_cid_id in dict_mpp_cid.keys():
                    return [0, dict_mpp_cid[bd_cid_id]]
                else:
                    return [0, bd_cid_id]

        # 当vid大于1亿时, 表示是关系id, 需要通过改bdid反查cid
        if str(field[0]).isdigit() and int(field[0]) > 100000000:
            _res = media_cms_playlist_vid_map_client.get_playlist_id_by_rid([field[0]])

            if _res[0] == 0:
                _cid_res = media_vrs_bdid_map_client.get_fstlvlid_by_bd_id([_res[1]])
                if _cid_res[0] != 0:
                    return _cid_res
                else:
                    bd_cid_id = str(_cid_res[1])
                    if bd_cid_id in dict_mpp_cid.keys():
                        return [0, dict_mpp_cid[bd_cid_id]]
                    else:
                        return [0, bd_cid_id]
            else:
                return _res

        return [0, "-1"]