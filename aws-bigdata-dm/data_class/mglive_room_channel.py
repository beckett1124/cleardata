# encoding: utf-8
# @Author: gibbs
# @Date:   2016-08-10T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-08-10T19:29:22+08:00

from media_base_table import MediaBaseTable
import sys
import string


class MgliveRoomChannel(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(MgliveRoomChannel, self).__init__()
        self.mglive_room_channel_map = {}
        self.__load_mglive_room_channel_map()

    def __load_mglive_room_channel_map(self):
        """
        加载媒资信息. {file_name: channel}
        :return:
        """
        if len(self.mglive_room_channel_map) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("mglive_room_channel")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 2:
                    (room_id, channel_id) = record[0:2]
                    self.mglive_room_channel_map[room_id] = channel_id
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def check_room_id(self, room_channel_list):
        """
        通过 32位channel获取纯数字auto_id
        :param room_channel_list: channel list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(room_channel_list, list) or len(room_channel_list) != 2:
            return [1, "FORMAT_INPUT_ERR"]

        room_id = str(room_channel_list[0]).strip()
        channel_id = room_channel_list[1]

        m_info = self.mglive_room_channel_map.get(room_id)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            if str(m_info) == str(channel_id):
                return [0, room_channel_list[0]]
            else:
                return [1, "ROOM_NOT_EQUAL_CHANNEL"]

mglive_room_channel_client = MgliveRoomChannel()