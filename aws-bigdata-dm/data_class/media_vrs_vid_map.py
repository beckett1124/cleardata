# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from media_base_table import MediaBaseTable
import sys
import string


class MediaVRSVidMap(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(MediaVRSVidMap, self).__init__()

        # 视频信息
        self.vid_map = {}

        self.__load_vid_id_map()

    def __load_vid_id_map(self):
        """
        加载媒资信息. vid->[v_name, is_full, duration]
        :return:
        """
        if len(self.vid_map) == 0 or len(self.vid_map) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("asset_v_parts")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 7:
                    (vid, v_name, duration, is_full, clipid, fstlvlid, seriesid) = record[0:7]
                    self.vid_map[vid] = [v_name, is_full, duration, clipid, fstlvlid, seriesid]
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def check_vid(self, vid_list):
        """
        校验vid是否合法
        :param vid_list: 数字类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vid_list, list) or len(vid_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        vid = vid_list[0]
        if vid == "-" or vid == "":
            return [-1, 'VID_IS_NULL']

        if not str(vid).isdigit():
            return [1, "ID_NOT_INT"]

        m_info = self.vid_map.get(vid)
        if m_info is not None:
            return [0, vid]
        else:
            return [1, "INFO_NOT_FOUND"]

    def get_v_name_by_vid(self, vid_list):
        """
        通过vid获取v_name
        :param vid_list: 数字类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vid_list, list) or len(vid_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        vid = vid_list[0]

        if not str(vid).isdigit():
            return [1, "ID_NOT_INT"]

        m_info = self.vid_map.get(vid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, str(m_info[0]).replace(',', '').strip()]

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
        m_info = self.vid_map.get(vid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            # 兼容老数据，is_full 为2，表示短片,老数据用0表示
            if str(m_info[1]) == "2":
                return [0, 0]
            else:
                return [0, m_info[1]]

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
        m_info = self.vid_map.get(vid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info[2]]

    def get_clipid_by_vid(self, vid_list):
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
        m_info = self.vid_map.get(vid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            if str(m_info[3]) == "0":
                return [0, "-1"]
            return [0, m_info[3]]

    def get_fstlvlid_by_vid(self, vid_list):
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
        m_info = self.vid_map.get(vid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            if str(m_info[4]) == "0" or str(m_info[4]) == "NULL":
                return [0, "-1"]
            return [0, m_info[4]]

    def get_seriesid_by_vid(self, vid_list):
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
        m_info = self.vid_map.get(vid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            if str(m_info[5]) == "0" or str(m_info[5]) == "NULL":
                return [0, "\N"]
            return [0, m_info[5]]

media_vrs_vid_map_client = MediaVRSVidMap()