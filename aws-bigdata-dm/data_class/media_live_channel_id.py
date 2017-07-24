# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from media_base_table import MediaBaseTable
from conf.settings import RuleConfig
import sys
import string


class MediaLiveChannelId(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(MediaLiveChannelId, self).__init__()
        self.media_live_channel_id = {}
        self.__load_live_channel_id()

    def __load_live_channel_id(self):
        """
        加载媒资信息. {file_name: vid}
        :return:
        """
        if len(self.media_live_channel_id) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("live_channel_id")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 2:
                    (channel_id, channel_name) = record[0:2]
                    self.media_live_channel_id[channel_id] = channel_name
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def get_channel_name_by_channel_id(self, channel_id_list):
        """
        通过ott vid获取svid
        :param channel_id_list: vid list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(channel_id_list, list) or len(channel_id_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        channel_id = channel_id_list[0]

        if not str(channel_id).isdigit():
            return [1, "ID_NOT_INT"]

        m_info = self.media_live_channel_id.get(channel_id)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, str(m_info).replace(',', '')]

    def check_channel_id(self, channel_id_list):
        """
        校验channel_id
        :param channel_id_list: channelId list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(channel_id_list, list) or len(channel_id_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        channel_id = channel_id_list[0]

        if channel_id == "-" or channel_id == "":
            return [1, 'CHANNEL_ID_IS_NULL']

        if not str(channel_id).isdigit():
            return [1, "ID_NOT_INT"]

        if channel_id in self.media_live_channel_id:
            return [0, channel_id]
        else:
            return [1, "INFO_NOT_FOUND"]

media_live_channel_id_client = MediaLiveChannelId()