# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from media_base_table import MediaBaseTable
from conf.settings import RuleConfig
import sys
import string


class MediaAppCid(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(MediaAppCid, self).__init__()
        self.media_app_cid = {}
        self.__load_app_cid()

    def __load_app_cid(self):
        """
        加载媒资信息. {file_name: vid}
        :return:
        """
        if len(self.media_app_cid) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("mpp_app_cid")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 3:
                    (app_cid, app_c_name, cid_plat) = record[0:3]
                    self.media_app_cid[app_cid + "|" + cid_plat] = app_c_name
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def get_app_cid_name_by_cid(self, cid_list):
        """
        通过ott vid获取svid
        :param cid_list: vid list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(cid_list, list) or len(cid_list) != 2:
            return [1, "FORMAT_INPUT_ERR"]

        cid = cid_list[0]
        bid_name = cid_list[1]

        if not str(cid).isdigit():
            return [1, "ID_NOT_INT"]

        if "pad" in bid_name:
            platform = "pad"
        else:
            platform = "phone"

        m_info = self.media_app_cid.get(cid + "|" + platform)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, str(m_info).replace(',', '').strip()]

media_app_cid_client = MediaAppCid()