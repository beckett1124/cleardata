# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from media_base_table import MediaBaseTable
import sys
import string


class MppCmsCidNameMap(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(MppCmsCidNameMap, self).__init__()
        self.cid_name_map = {}
        self.__load_mpp_cms_cid_name_map()

    def __load_mpp_cms_cid_name_map(self):
        """
        加载媒资信息. vid->[vid,p_lid,cid,v_name]
        :return:
        """
        if len(self.cid_name_map) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("mpp_cms_id_map")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 9:
                    cid = record[7]
                    c_name = record[8]
                    self.cid_name_map[cid] = c_name
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def get_c_name_by_cid(self, cid_list):
        """
        通过vid获取p_lid
        :param cid_list: 数字类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(cid_list, list) or len(cid_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        cid = cid_list[0]

        if not str(cid).isdigit():
            return [1, "ID_NOT_INT"]
        m_info = self.cid_name_map.get(cid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, str(m_info).replace(',', '').strip()]


mpp_cms_cid_name_map_client = MppCmsCidNameMap()