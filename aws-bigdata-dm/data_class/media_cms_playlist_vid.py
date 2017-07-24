# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from media_base_table import MediaBaseTable
import sys
import string


class MediaCmsPlaylistVid(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(MediaCmsPlaylistVid, self).__init__()

        # 播单id
        self.playlist_vid_map = {}

        self.__load_playlist_vid_map()

    def __load_playlist_vid_map(self):
        """
        加载媒资信息. relation_id->[playlist_id,vid]
        :return:
        """
        if len(self.playlist_vid_map) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("hunantv_v_playlist_videos")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 3:
                    (relation_id, playlist_id, vid) = record[0:3]
                    self.playlist_vid_map[relation_id] = [playlist_id, vid]
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def get_playlist_id_by_rid(self, rid_list):
        """
        获取播单id
        :param rid_list: 数字类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(rid_list, list) or len(rid_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        rid = rid_list[0]
        if rid == "-" or rid == "" or str(rid) == "0":
            return [0, '']

        if not str(rid).isdigit():
            return [1, "ID_NOT_INT"]

        m_info = self.playlist_vid_map.get(rid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info[0]]

    def get_vid_by_rid(self, rid_list):
        """
        获取vid
        :param rid_list: 数字类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(rid_list, list) or len(rid_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        rid = rid_list[0]
        if rid == "-" or rid == "" or str(rid) == "0":
            return [0, '']

        if not str(rid).isdigit():
            return [1, "ID_NOT_INT"]

        m_info = self.playlist_vid_map.get(rid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info[1]]

media_cms_playlist_vid_map_client = MediaCmsPlaylistVid()