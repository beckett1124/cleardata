# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from media_base_table import MediaBaseTable
import sys
import string


class MediaMgMediaMap(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(MediaMgMediaMap, self).__init__()

        # 芒果直播点播
        self.mg_mediaId_map = {}

        self.__load_mg_media_id_map()

    def __load_mg_media_id_map(self):
        """
        加载媒资信息. seriesId->[series_name]
        :return:
        """
        if len(self.mg_mediaId_map) == 0 or len(self.mg_mediaId_map) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("asset_v_vod_media_info")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 5:
                    int_id = record[0]
                    file_key = record[3]
                    file_name = record[4]
                    self.mg_mediaId_map[file_key] = [int_id, file_name]
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def get_mid_by_media_id(self, media_list):
        """
        通过media_id字符串获取int_id
        :param media_list: 字符类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(media_list, list) or len(media_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        media_id = media_list[0]
        if media_id == "-" or media_id == "":
            return [1, 'MEDIA_ID_IS_NULL']

        m_info = self.mg_mediaId_map.get(media_id)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info[0]]

    def get_name_by_media_id(self, media_list):
        """
        通过media_id字符串获取int_id
        :param media_list: 字符类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(media_list, list) or len(media_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        media_id = media_list[0]
        if media_id == "-" or media_id == "":
            return [1, 'MEDIA_ID_IS_NULL']

        m_info = self.mg_mediaId_map.get(media_id)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info[1]]


media_mg_media_id_client = MediaMgMediaMap()