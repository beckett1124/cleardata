# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_vrs_vid_map import media_vrs_vid_map_client
from data_class.media_mg_mediaid_map import media_mg_media_id_client


class MediaVRSOTTVid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaVRSOTTVid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data([vid, cpn])
        :return: vid
        """
        if len(field) == 3 and (str(field[1]) == "3" or str(field[2]) == "5"):
            return media_mg_media_id_client.get_mid_by_media_id([field[0]])
        else:

            return media_vrs_vid_map_client.check_vid([field[0]])