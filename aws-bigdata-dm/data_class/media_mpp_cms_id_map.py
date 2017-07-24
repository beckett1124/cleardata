# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from media_base_table import MediaBaseTable
from conf.settings import RuleConfig
import sys
import string


class MppCmsIdMap(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(MppCmsIdMap, self).__init__()
        self.mpp_cms_id_map = {}
        self.__load_mpp_cms_id_map()

    def __load_mpp_cms_id_map(self):
        """
        加载媒资信息. vid->[vid,p_lid,cid,v_name]
        :return:
        """
        if len(self.mpp_cms_id_map) == 0:
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
                    (vid, v_name, series_id, pid, p_name, is_full, duration, cid, c_name) = record[0:9]
                    self.mpp_cms_id_map[vid] = [pid, cid, series_id, is_full, duration]
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def get_p_lid_by_vid(self, vid_list):
        """
        通过vid获取p_lid
        :param vid_list: 数字类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vid_list, list) or len(vid_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        vid = vid_list[0]
        if vid == "-" or vid == "":
            return [0, '\N']

        if not str(vid).isdigit():
            return [1, "ID_NOT_INT"]
        m_info = self.mpp_cms_id_map.get(vid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            # 合集id为10,表示单视频－播单注入cms归属合集，无需展示
            if str(m_info[0]) == "10":
                return [0, '-1']
            else:
                return [0, m_info[0]]

    def get_c_id_by_vid(self, vid_list):
        """
        通过vid获取p_lid
        :param vid_list: 数字类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vid_list, list) or len(vid_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        vid = vid_list[0]
        if vid == "-" or vid == "":
            return [0, '\N']

        if not str(vid).isdigit():
            return [1, "ID_NOT_INT"]
        m_info = self.mpp_cms_id_map.get(vid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info[1]]

    def get_s_id_by_vid(self, vid_list):
        """
        通过vid获取p_lid
        :param vid_list: 数字类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vid_list, list) or len(vid_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        vid = vid_list[0]
        if vid == "-" or vid == "":
            return [0, '\N']

        if not str(vid).isdigit():
            return [1, "ID_NOT_INT"]
        m_info = self.mpp_cms_id_map.get(vid)

        if m_info is None:
            return [0, "\N"]
        else:
            sid = ('\N' if str(m_info[2]) == '0' else m_info[2])
            return [0, sid]

    def get_is_full_by_vid(self, vid_list):
        """
        通过vid获取p_lid
        :param vid_list: 数字类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vid_list, list) or len(vid_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        vid = vid_list[0]
        if vid == "-" or vid == "":
            return [0, '\N']

        if not str(vid).isdigit():
            return [1, "ID_NOT_INT"]
        m_info = self.mpp_cms_id_map.get(vid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info[3]]

    def get_vts_by_vid(self, vid_list):
        """
        通过vid获取p_lid
        :param vid_list: 数字类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vid_list, list) or len(vid_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        vid = vid_list[0]
        if vid == "-" or vid == "":
            return [0, '\N']

        if not str(vid).isdigit():
            return [1, "ID_NOT_INT"]
        m_info = self.mpp_cms_id_map.get(vid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info[4]]


mpp_cms_id_map_client = MppCmsIdMap()