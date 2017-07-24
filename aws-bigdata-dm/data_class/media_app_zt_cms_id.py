# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from conf.settings import RuleConfig
from media_base_table import MediaBaseTable
import sys
import string


class MediaAppZTCmsId(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(MediaAppZTCmsId, self).__init__()
        self.media_app_zt_cms_id = {}
        self.__load_app_zt_cms_id()

    def __load_app_zt_cms_id(self):
        """
        加载媒资信息. vid->[vid,p_lid,cid,v_name]
        :return:
        """
        if len(self.media_app_zt_cms_id) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("app_zt_cms_id")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 3:
                    (zt_id, zt_name, zt_plat) = record[0:3]
                    self.media_app_zt_cms_id[zt_id + "|" + zt_plat] = zt_name
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def get_zt_name_by_zt_id(self, zt_id_list):
        """
        通过ott vid获取svid
        :param zt_id_list: vid list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(zt_id_list, list) or len(zt_id_list) != 2:
            return [1, "FORMAT_INPUT_ERR"]

        zt_id = zt_id_list[0]
        bid_name = zt_id_list[1]

        if not str(zt_id).isdigit():
            return [1, "ID_NOT_INT"]

        if "pad" in bid_name:
            platform = "pad"
        else:
            platform = "phone"

        m_info = self.media_app_zt_cms_id.get(zt_id + "|" + platform)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, str(m_info).replace(',', '').strip()]

media_app_zt_cms_id_client = MediaAppZTCmsId()