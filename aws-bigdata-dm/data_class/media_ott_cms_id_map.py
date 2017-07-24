# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from media_base_table import MediaBaseTable
from conf.settings import RuleConfig
import sys
import string


class OttCmsIdMap(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(OttCmsIdMap, self).__init__()
        self.ott_cms_id_map = {}
        self.__load_ott_cms_id_map()

    def __load_ott_cms_id_map(self):
        """
        加载媒资信息. {file_name: vid}
        :return:
        """
        if len(self.ott_cms_id_map) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("ott_cms_id_map")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 2:
                    (vid, s_vid) = record[0:2]
                    self.ott_cms_id_map[s_vid] = vid
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def get_svid_by_vid(self, vid_32_list):
        """
        通过ott 32位vid获取纯数字svid
        :param vid_list: vid list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vid_32_list, list) or len(vid_32_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        vid_32 = vid_32_list[0]

        m_info = self.ott_cms_id_map.get(vid_32)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info]

ott_cms_id_map_client = OttCmsIdMap()