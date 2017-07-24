# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_live_channel_id import media_live_channel_id_client
from data_class.mglive_id_auid import mglive_id_auid_client


class MediaCheckLiveChannelId(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaCheckLiveChannelId, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(vid)
        :return: plid
        """
        if str(field[0]).isdigit():
            return media_live_channel_id_client.check_channel_id(field)
        else:
            return mglive_id_auid_client.get_id_by_auid(field)

