# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

import sys
import string
import json
import urllib2

from media_base_table import MediaBaseTable
from rule.comm_rule.cn_bid import cn_bid
from commonlib.pydotalog import pydotalog


class CnMppChannel(MediaBaseTable):
    """
    :媒资信息类
    """

    def __init__(self):
        super(CnMppChannel, self).__init__()
        self.mpp_channel_map = {}
        self.__load_mpp_channel_map()
        self.update_ch_url = "http://54.222.167.88/sync/insert_mpp_vender.action?device_id=%s&vender_source=%s&vender_level=%s"

    def __load_mpp_channel_map(self):
        """
        加载媒资信息. vid->[vid,p_lid,cid,v_name]
        :return:
        """
        if len(self.mpp_channel_map) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("mpp_channel_map")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            try:
                fp.next()
            except StopIteration:
                pass

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 10:
                    (ven_id, vend_source) = record[0:2]
                    device_name = record[4]
                    parent_vend_id = record[6]
                    vend_status = record[8]
                    parent_vend_type = record[9]
                    ven_key = vend_source + "|" + device_name
                    self.mpp_channel_map[ven_key] = [ven_id, parent_vend_id, vend_status, parent_vend_type]
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def get_ch_by_source(self, vend_source_list, source_vend_level, is_update=True):
        """
        通过渠道标示获取渠道id
        :param vend_source_list: 字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vend_source_list, list) or len(vend_source_list) != 2:
            return [1, "FORMAT_INPUT_ERR"]

        vend_source = vend_source_list[0]
        device_name = vend_source_list[1]

        if device_name == "aphone":
            device_name = "android"
        elif device_name == "mac":
            device_name = "macclient"

        if vend_source == "-" or vend_source == "":
            return [0, '']

        vend_key = vend_source + "|" + device_name

        m_info = self.mpp_channel_map.get(vend_key)

        if m_info is None:
            if is_update is False:
                return [0, '']
            return self.__update_mpp_ch_map(vend_source, device_name, source_vend_level, 1)
        else:
            return [0, m_info[0]]

    def get_sub_ch_by_source(self, vend_source_list, source_vend_level, is_update=True):
        """
        通过渠道标示获取渠道id
        :param vend_source_list: 字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vend_source_list, list) or len(vend_source_list) != 2:
            return [1, "FORMAT_INPUT_ERR"]

        vend_source = vend_source_list[0]
        device_name = vend_source_list[1]

        if device_name == "aphone":
            device_name = "android"
        elif device_name == "mac":
            device_name = "macclient"

        if vend_source == "-" or vend_source == "":
            return [0, '\N']

        vend_key = vend_source + "|" + device_name

        m_info = self.mpp_channel_map.get(vend_key)

        if m_info is None:
            # 不需要更新时 直接返回 \N
            if is_update is False:
                return [0, '\N']

            return self.__update_mpp_ch_map(vend_source, device_name, source_vend_level, 2)
        else:
            return [0, m_info[0]]

    def get_ch_by_source_level_2(self, vend_source_list, source_vend_level=2, is_update=True):
        """
        通过渠道标示获取渠道id
        :param vend_source_list: 字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vend_source_list, list) or len(vend_source_list) != 2:
            return [1, "FORMAT_INPUT_ERR"]

        vend_source = vend_source_list[0]
        device_name = vend_source_list[1]

        if device_name == "aphone":
            device_name = "android"
        elif device_name == "mac":
            device_name = "macclient"

        if vend_source == "-" or vend_source == "":
            return [0, '']

        vend_key = vend_source + "|" + device_name

        m_info = self.mpp_channel_map.get(vend_key)

        if m_info is None:
            # 不需要更新时 直接返回 空
            if is_update is False:
                return [0, '']

            return self.__update_mpp_ch_map(vend_source, device_name, source_vend_level, 1)
        else:
            return [0, m_info[1]]

    def get_vend_status_by_source(self, vend_source_list):
        """
        通过渠道标示获取渠道id
        :param vend_source_list: 字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vend_source_list, list) or len(vend_source_list) != 2:
            return [1, "FORMAT_INPUT_ERR"]

        vend_source = vend_source_list[0]
        device_name = vend_source_list[1]

        if device_name == "aphone":
            device_name = "android"
        elif device_name == "mac":
            device_name = "macclient"

        if vend_source == "-" or vend_source == "":
            return [0, '2']

        vend_key = vend_source + "|" + device_name

        m_info = self.mpp_channel_map.get(vend_key)

        if m_info is None:
            return [0, "2"]
        else:
            return [0, m_info[2]]

    def get_ch_type_by_source(self, vend_source_list, source_vend_level=1, is_update=True):
        """
        通过渠道标示获取渠道类型
        :param vend_source_list: 字符串list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vend_source_list, list) or len(vend_source_list) != 2:
            return [1, "FORMAT_INPUT_ERR"]

        vend_source = vend_source_list[0]
        device_name = vend_source_list[1]

        if device_name != "pcweb" and device_name != "phonem" and device_name != "padweb":
            return [0, "\N"]

        # 自身渠道类型
        if vend_source == "-" or vend_source == "":
            return [0, '0']

        vend_key = vend_source + "|" + device_name

        m_info = self.mpp_channel_map.get(vend_key)

        if m_info is None:
            # 不需要更新时 直接返回 \N
            if is_update is False:
                return [0, '\N']

            _res = self.__update_mpp_ch_map(vend_source, device_name, source_vend_level, 1)
            if _res[0] == 0:
                m_info_tmp = self.mpp_channel_map.get(vend_key)
                # 当更新渠道信息失败时，渠道状态无法知晓是否已经存在,无法给渠道类型赋默认值
                if m_info_tmp is None:
                    return [1, "UPDATE_CH_TYPE_FAILED"]
                if m_info_tmp[3] == 'NULL':
                    return [0, '2']
                return [0, m_info_tmp[3]]
            else:
                return _res
        else:
            if m_info[3] == 'NULL':
                return [0, '2']
            return [0, m_info[3]]

    def __update_mpp_ch_map(self, vend_source, device_name, source_vend_level, des_level):

        if device_name not in ["pcweb", "phonem", "padweb", "pcclient", "weixin"]:
            if des_level == 2:
                return [0, "\N"]
            else:
                return [0, ""]

        _res_device_id = cn_bid().convert([device_name])
        if _res_device_id[0] != 0:
            return [1, "GET_DEVICE_ID_ERR"]

        try:
            response = urllib2.urlopen(self.update_ch_url % (_res_device_id[1], vend_source, str(source_vend_level)))
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                pydotalog.warning("open url failed :%s" % e.reason)
            elif hasattr(e, "code"):
                pydotalog.warning("HTTP return failed Error code:[%s]" % e.code)

            return [1, "OPEN_URL_ERR"]

        if response.getcode() == 200:
            try:
                tmp_re = response.read()
                dict_ch = json.loads(tmp_re)
            except ValueError:
                return [1, 'UPDATE_RESULT_NOT_JSON']
        else:
            return [1, "RESPONSE_STATUS_FAILED"]

        if not isinstance(dict_ch, dict) or len(dict_ch) <= 0 or dict_ch.get("ven_id") is None:
            return [1, "UPDATE_CH_FAILED"]

        if not str(dict_ch["ven_id"]).isdigit() or int(dict_ch["ven_id"]) <= 0:
            return [1, "UPDATE_CH_FAILED"]
        else:
            key_list = dict_ch.keys()
            if "parent_vend_id" not in key_list or "vend_status" not in key_list or "vend_type" not in key_list:
                return [1, "RETURN_CH_INFO_ERR"]
            ch_id = dict_ch["ven_id"]
            pa_ch_id = dict_ch["parent_vend_id"]
            vend_key = vend_source + "|" + device_name
            self.mpp_channel_map[vend_key] = [ch_id, pa_ch_id, dict_ch["vend_status"], dict_ch["vend_type"]]
            return [0, ch_id]


cn_mpp_channel_client = CnMppChannel()
