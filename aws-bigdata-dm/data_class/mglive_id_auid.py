# encoding: utf-8
# @Author: gibbs
# @Date:   2016-08-10T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-08-10T19:29:22+08:00

from media_base_table import MediaBaseTable
import sys
import string


class MgliveIdAuId(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(MgliveIdAuId, self).__init__()
        self.mglive_id_auid_map = {}
        self.__load_mglive_id_auid_map()

    def __load_mglive_id_auid_map(self):
        """
        加载媒资信息. {file_name: auid}
        :return:
        """
        if len(self.mglive_id_auid_map) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("mglive_id_auid")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 3:
                    (id, auid) = record[0:2]
                    self.mglive_id_auid_map[auid] = id
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def get_id_by_auid(self, auid_32_list):
        """
        通过 32位auid获取纯数字id
        :param auid_32_list: auid list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(auid_32_list, list) or len(auid_32_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        auid = auid_32_list[0]

        m_info = self.mglive_id_auid_map.get(auid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info]

    def get_id_by_auid_for_vod(self, auid_32_list):
        """
        通过 32位auid获取纯数字id
        :param auid_32_list: auid list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(auid_32_list, list) or len(auid_32_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        auid = auid_32_list[0]

        m_info = self.mglive_id_auid_map.get(auid)

        if m_info is None:
            return [0, "0"]
        else:
            return [0, m_info]

mglive_id_auid_client = MgliveIdAuId()