# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from conf.settings import RuleConfig
import sys
import string


class CnOttVersion(object):
    """
    :媒资信息类
    """

    def __init__(self):
        super(CnOttVersion, self).__init__()
        self.ott_version = {}
        # self.vend_id_name_map = {}
        self.drop_record = 0
        self.__load_ott_file_id_map()

    def __load_ott_file_id_map(self):
        """
        加载媒资信息. {file_name: [ver_id,version,open_type,vend_id,vend_name,vend_parent_id]}
        :return:
        """
        if len(self.ott_version) == 0:
            file_path = RuleConfig["Media_table_info"].get("ott_version")
            if file_path is None or file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            for line in fp:
                record = string.split(line.strip('\n'), "\t")

                if len(record) >= 6:
                    (ver_id, version, open_type, vend_id, vend_name, vend_parent_id) = record[0:6]
                    self.ott_version[str(version).lower()] = [ver_id, vend_id, vend_name, open_type, vend_parent_id]

                    # if vend_id not in self.vend_id_name_map.keys():
                    #     self.vend_id_name_map[vend_id] = vend_name
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def get_ver_id_by_version(self, version_l):
        """
        通过ott file name获取vid
        :param version_l: 文件名list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(version_l, list) or len(version_l) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        version = str(version_l[0]).strip()

        if version == "":
            return [1, "INPUT_IS_NULL"]

        m_info = self.ott_version.get(version)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info[0]]

    def get_vend_id_by_version(self, version_l):
        """
        通过ott file name获取vid
        :param version_l: 文件名list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(version_l, list) or len(version_l) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        version = str(version_l[0]).strip()

        if version == "":
            return [1, "INPUT_IS_NULL"]

        m_info = self.ott_version.get(version)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            #  open_type =1 时, 取vend_parent_id
            if str(m_info[3]) == "1":
                return [0, m_info[4]]
            else:
                return [0, m_info[1]]

    def get_vend_name_by_version(self, version_l):
        """
        通过ott file name获取vid
        :param version_l: 文件名list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(version_l, list) or len(version_l) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        version = str(version_l[0]).strip()

        if version == "":
            return [1, "INPUT_IS_NULL"]

        m_info = self.ott_version.get(version)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info[2]]

    def get_open_type_by_version(self, version_l):
        """
        通过ott file name获取vid
        :param version_l: 文件名list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(version_l, list) or len(version_l) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        version = str(version_l[0]).strip()

        if version == "":
            return [1, "INPUT_IS_NULL"]

        m_info = self.ott_version.get(version)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info[3]]

    def get_sub_vend_id_by_version(self, version_l):
        """
        通过ott file name获取vid
        :param version_l: 文件名list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(version_l, list) or len(version_l) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        version = str(version_l[0]).strip()

        if version == "":
            return [1, "INPUT_IS_NULL"]

        m_info = self.ott_version.get(version)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info[1]]


cn_ott_ver_client = CnOttVersion()