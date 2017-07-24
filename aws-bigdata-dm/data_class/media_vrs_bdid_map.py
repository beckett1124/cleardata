# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from media_base_table import MediaBaseTable
import sys
import string


class MediaVRSBdIdMap(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(MediaVRSBdIdMap, self).__init__()

        # 播单id
        self.bdId_name_map_name_map = {}

        self.__load_bdId_name_map_name_map()

    def __load_bdId_name_map_name_map(self):
        """
        加载媒资信息. bdid->[bd_name]
        :return:
        """
        if len(self.bdId_name_map_name_map) == 0 or len(self.bdId_name_map_name_map) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("asset_v_playlist")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 3:
                    (bd_id, bd_name, fstlvlid) = record[0:3]
                    self.bdId_name_map_name_map[bd_id] = [bd_name, fstlvlid]
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def check_bd_id(self, bd_id_list):
        """
        校验bd_id是否合法
        :param bd_id_list: 数字类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(bd_id_list, list) or len(bd_id_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        bd_id = bd_id_list[0]
        if bd_id == "-" or bd_id == "" or str(bd_id) == "0":
            return [0, '-1']

        if not str(bd_id).isdigit():
            return [1, "ID_NOT_INT"]

        m_info = self.bdId_name_map_name_map.get(bd_id)

        if m_info is not None:
            return [0, bd_id]
        else:
            return [1, "INFO_NOT_FOUND"]

    def get_bd_name_by_bd_id(self, bd_id_list):
        """
        通过bd_id_list获取名字
        :param bd_id_list: 数字类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(bd_id_list, list) or len(bd_id_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        bd_id = bd_id_list[0]

        if not str(bd_id).isdigit():
            return [1, "ID_NOT_INT"]
        m_info = self.bdId_name_map_name_map.get(bd_id)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, str(m_info[0]).replace(',', '').strip()]

    def get_fstlvlid_by_bd_id(self, bd_id_list):
        """
        通过bd_id_list获取名字
        :param bd_id_list: 数字类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(bd_id_list, list) or len(bd_id_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        bd_id = bd_id_list[0]

        if not str(bd_id).isdigit():
            return [1, "ID_NOT_INT"]
        m_info = self.bdId_name_map_name_map.get(bd_id)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, str(m_info[1]).strip()]


media_vrs_bdid_map_client = MediaVRSBdIdMap()