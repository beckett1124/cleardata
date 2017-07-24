# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from media_base_table import MediaBaseTable
import sys
import string


class MediaVRSSeriesIdMap(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(MediaVRSSeriesIdMap, self).__init__()

        # 系列id
        self.seriesId_name_map = {}

        self.__load_seriesId_name_map()

    def __load_seriesId_name_map(self):
        """
        加载媒资信息. seriesId->[series_name]
        :return:
        """
        if len(self.seriesId_name_map) == 0 or len(self.seriesId_name_map) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("asset_v_clip_series")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 2:
                    (series_id, series_name) = record[0:2]
                    self.seriesId_name_map[series_id] = [series_name]
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def check_series_id(self, series_id_list):
        """
        校验seriesId是否合法
        :param series_id_list: 数字类字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(series_id_list, list) or len(series_id_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        series_id = series_id_list[0]
        if series_id == "-" or series_id == "" or str(series_id) == "0":
            return [0, '-1']

        if not str(series_id).isdigit():
            return [1, "ID_NOT_INT"]

        m_info = self.seriesId_name_map.get(series_id)
        if m_info is not None:
            return [0, series_id]
        else:
            return [1, "INFO_NOT_FOUND"]


media_vrs_seriesid_map_client = MediaVRSSeriesIdMap()