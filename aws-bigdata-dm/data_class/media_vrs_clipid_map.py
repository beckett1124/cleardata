# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from media_base_table import MediaBaseTable
import sys
import string


class MediaVRSClipIdMap(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(MediaVRSClipIdMap, self).__init__()

        # 合集id
        self.clipId_name_map = {}

        self.__load_clipId_name_map()

    def __load_clipId_name_map(self):
        """
        加载媒资信息. clipId->[clip_name]
        :return:
        """
        if len(self.clipId_name_map) == 0 or len(self.clipId_name_map) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("asset_v_clips")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 2:
                    (clip_id, clip_name) = record[0:2]
                    self.clipId_name_map[clip_id] = [clip_name]
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def check_clip_id(self, clip_list):
        """
        校验clipId是否合法
        :param clip_list: 数字类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(clip_list, list) or len(clip_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        clip = clip_list[0]
        if clip == "-" or clip == "" or str(clip) == "0":
            return [0, '-1']

        if not str(clip).isdigit():
            return [1, "ID_NOT_INT"]

        m_info = self.clipId_name_map.get(clip)
        if m_info is not None:
            return [0, clip]
        else:
            return [1, "INFO_NOT_FOUND"]

media_vrs_clipid_map_client = MediaVRSClipIdMap()