# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from media_base_table import MediaBaseTable
import sys
import string
import urllib2
from conf.settings import RuleConfig
from commonlib.pydotalog import pydotalog


class MediaIphoneVersion(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(MediaIphoneVersion, self).__init__()
        self.phone_version = {}
        self.__load_ott_file_id_map()
        self.version_url = "http://54.222.167.88/sync/insert_app_version.action?version_name=%s&device_id=%s&os_id=%s"

    def __load_ott_file_id_map(self):
        """
        加载媒资信息. {file_name: [vid,pid,cid,is_full,duration]}
        :return:
        """
        if len(self.phone_version) == 0:
            file_path = RuleConfig["Media_table_info"].get("app_version")
            if file_path is None or file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 3:
                    (ver_id, version, device_id) = record[0:3]
                    ver_key = str(version) + "|" + str(device_id)
                    self.phone_version[ver_key] = ver_id
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def get_ver_id_by_version(self, version_l, is_update=True):
        """
        通过ott file name获取vid
        :param version_l: 文件名list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(version_l, list) or len(version_l) != 2:
            return [1, "FORMAT_INPUT_ERR"]

        version = str(version_l[0]).strip()
        device_name = str(version_l[1]).strip()

        if version == "" or device_name == "":
            return [1, "INPUT_IS_NULL"]

        device_id = self.__get_device_id(device_name)

        m_key = str(version) + "|" + str(device_id)

        m_info = self.phone_version.get(m_key)

        # 获取失败时，调用接口添加版本。
        if m_info is None:
            #
            if is_update is False:
                return [1, "VERSION_NOT_FOUND"]
            os_id = self.__get_os_id(device_name)

            if device_id < 0:
                return [1, "CLIENT_INPUT_ERR"]

            try:
                response = urllib2.urlopen(self.version_url % (version, device_id, os_id))
            except urllib2.URLError, e:
                if hasattr(e, "reason"):
                    pydotalog.warning("open url failed :%s" % e.reason)
                elif hasattr(e, "code"):
                    pydotalog.warning("HTTP return failed Error code:[%s]" % e.code)

                return [1, "OPEN_URL_ERR"]

            if response.getcode() == 200:
                version_id = response.read()
            else:
                return [1, "RESPONSE_STATUS_FAILED"]

            if version_id is None or version_id < 0:
                return [1, "UPDATE_VERSION_FAILED"]
            else:
                self.phone_version[m_key] = version_id
                return [0, version_id]
        else:
            return [0, m_info]

    @staticmethod
    def __get_device_id(device_name):
        if device_name in ['android', 'iphone', 'aphone', ]:
            return 1
        elif device_name in ['ipad', 'apad']:
            return 2
        elif device_name in ['pcclient']:
            return 3
        elif device_name in ['win10client']:
            return 4
        elif device_name in ['macclient', 'mac']:
            return 5
        elif device_name in ['tvos']:
            return 6
        elif device_name == "未知":
            return 0
        else:
            return -1

    @staticmethod
    def __get_os_id(device_name):
        if device_name in ['android', 'aphone', 'apad']:
            return 1
        elif device_name in ['ipad', 'iphone']:
            return 2
        else:
            return ""


media_iphone_ver_client = MediaIphoneVersion()