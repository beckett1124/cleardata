# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from media_base_table import MediaBaseTable
import sys
import string


class MediaVRSfstlvlIdMap(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(MediaVRSfstlvlIdMap, self).__init__()

        # 一级分类
        self.fstlvlId_name_map = {}

        self.__load_fstlvlId_name_map()

    def __load_fstlvlId_name_map(self):
        """
        加载媒资信息. fstlvlId->[fstlvl_name]
        :return:
        """
        if len(self.fstlvlId_name_map) == 0 or len(self.fstlvlId_name_map) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("asset_v_fstlvl_types")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 2:
                    (fstlvl_id, fstlvl_name) = record[0:2]
                    self.fstlvlId_name_map[fstlvl_id] = [fstlvl_name]
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def check_fstlvl_id(self, fstlvl_id_list):
        """
        校验fstlvlId是否合法
        :param fstlvl_id_list: 数字类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(fstlvl_id_list, list) or len(fstlvl_id_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        fstlvl_id = fstlvl_id_list[0]
        if fstlvl_id == "-" or fstlvl_id == "" or str(fstlvl_id) == "0":
            return [0, '-1']

        if not str(fstlvl_id).isdigit():
            return [1, "ID_NOT_INT"]

        m_info = self.fstlvlId_name_map.get(fstlvl_id)
        if m_info is not None:
            return [0, fstlvl_id]
        else:
            return [1, "INFO_NOT_FOUND"]

    def get_c_name_by_cid(self, cid_list):
        """
        通过cid获取频道名称
        :param cid_list: 数字类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(cid_list, list) or len(cid_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        cid = cid_list[0]

        if not str(cid).isdigit():
            return [1, "ID_NOT_INT"]
        m_info = self.fstlvlId_name_map.get(cid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, str(m_info[0]).replace(',', '').strip()]


media_vrs_fstlvlid_map_client = MediaVRSfstlvlIdMap()