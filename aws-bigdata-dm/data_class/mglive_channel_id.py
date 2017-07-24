# encoding: utf-8
# @Author: gibbs
# @Date:   2016-08-10T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-08-10T19:29:22+08:00

from media_base_table import MediaBaseTable
import sys
import string


class MgliveChannelId(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(MgliveChannelId, self).__init__()
        self.mglive_channel_id_map = {}
        self.__load_mglive_channel_id_map()

    def __load_mglive_channel_id_map(self):
        """
        加载媒资信息. {file_name: channel}
        :return:
        """
        if len(self.mglive_channel_id_map) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("mglive_channel_id")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 2:
                    (channel_id, auto_id) = record[0:2]
                    self.mglive_channel_id_map[channel_id] = auto_id
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def get_auto_id_by_channel(self, channel_32_list):
        """
        通过 32位channel获取纯数字auto_id
        :param channel_32_list: channel list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(channel_32_list, list) or len(channel_32_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        channel = str(channel_32_list[0]).strip()

        m_info = self.mglive_channel_id_map.get(channel)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info]

mglive_channel_id_client = MgliveChannelId()