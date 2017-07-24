# encoding: utf-8
# @Author: gibbs
# @Date:   2016-08-10T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-08-10T19:29:22+08:00

import sys
import string
import urllib2
from commonlib.pydotalog import pydotalog
from media_base_table import MediaBaseTable
import urllib
import re


class CnMobileActivity(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(CnMobileActivity, self).__init__()
        self.mobile_activity_id_map = {}
        self.__load_mobile_activity_id_map()
        self.activity_regex = "^(http|https)://www.(mgtv|hunantv).com/v/(\d{4})/([^/]+)/?"
        self.activity_pattern = re.compile(self.activity_regex)
        self.mobile_activity_url = "http://54.222.167.88/bi/h5act.action?name=%s"

    def __load_mobile_activity_id_map(self):
        """
        加载媒资信息. {file_name: channel}
        :return:
        """
        if len(self.mobile_activity_id_map) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("mobile_activity_url")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 2:
                    (activity_id, activity_url) = record[0:2]
                    self.mobile_activity_id_map[activity_url.strip()] = activity_id
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def get_activity_id(self, activity_list):
        """
        通过 32位channel获取纯数字auto_id
        :param activity_list: channel list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(activity_list, list) or len(activity_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        activity_url = str(activity_list[0]).strip()

        a_info = self.mobile_activity_id_map.get(activity_url)

        if a_info is None:
            return self.__update_activity_id_map(activity_url)
        else:
            return [0, a_info]

    def get_activity_url(self, page_url):
        """
        通过page_url获取活动_url
        :param page_url:
        :return:
        """
        url_str = urllib.unquote(page_url).strip()
        index_url = url_str.find("?")
        if index_url >= 0:
            url_str = url_str[0:index_url]

        match = self.activity_pattern.match(url_str)
        if not match:
            return [0, ""]

        if len(match.groups()) >= 4:
            activity_url = match.groups()[2] + "/" + match.groups()[3]
        else:
            return [0, ""]

        _res = self.get_activity_id([activity_url])
        if _res[0] == 0:
            return [0, activity_url.replace("/", "_")]
        else:
            return [0, ""]

    def __update_activity_id_map(self, activity_url):
        """
        :param activity_url: string
        :return: [err_no, activity_id or err_msg]
        """
        try:
            response = urllib2.urlopen(self.mobile_activity_url % activity_url)
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                pydotalog.warning("open url failed :%s" % e.reason)
            elif hasattr(e, "code"):
                pydotalog.warning("HTTP return failed Error code:[%s]" % e.code)

            return [1, "OPEN_URL_ERR"]

        if response.getcode() == 200:
            activity_id = response.read()
        else:
            return [1, "RESPONSE_STATUS_FAILED"]

        if activity_id is None or activity_id < 0:
            return [1, "UPDATE_ACTIVITY_ID_FAILED"]
        else:
            self.mobile_activity_id_map[activity_url] = activity_id
            return [0, activity_id]


cn_mobile_activity = CnMobileActivity()