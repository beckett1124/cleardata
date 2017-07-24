# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from rule.rule import rule
from data_class.media_mg_mediaid_map import media_mg_media_id_client
from rule.media_rule.media_vrs_vid import MediaVRSVid


class MediaVRSPvVid(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(MediaVRSPvVid, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data([vid, cpn])
        :return: vid
        """
        if not isinstance(field, list) or len(field) == 0:
            return [1, "LEN_IS_ZERO"]
        if field[0] == "-" or field[0] == "" or str(field[0]) == "0":
            return [0, '\N']

        if str(field[0]).isdigit():
            return MediaVRSVid().convert([field[0]])
        else:
            return media_mg_media_id_client.get_mid_by_media_id([field[0]])