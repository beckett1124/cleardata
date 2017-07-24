# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

from media_base_table import MediaBaseTable
from media_ott_cms_id_map import ott_cms_id_map_client
from conf.settings import RuleConfig
import sys
import string
import urllib


class OttFileIdMap(MediaBaseTable):

    """
    :媒资信息类
    """

    def __init__(self):
        super(OttFileIdMap, self).__init__()
        self.ott_file_id_map = {}
        self.ott_vid_map = {}
        self.ott_41_pid_url_map = {}
        self.__load_ott_file_id_map()

        # for ott_vv_41
        self.ott_41_nns_import_id_map = {}
        self.ott_41_clip_id_name_map = {}
        self.ott_41_vid_map = {}
        self.__load_ott_41_cms(self.ott_41_nns_import_id_map, 'ott_41_nns_import_id_map')
        self.__load_ott_41_cms(self.ott_41_clip_id_name_map, 'ott_41_clip_id_name_map')

    def __load_ott_41_cms(self, cms_map, name):
        """
        加载媒资信息. {file_name: [nns_id, nns_asset_import_id}
        加载媒资信息. {file_name: [name, sndlvl_id_list}
        :return:
        """
        if len(cms_map) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name(name)
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 2:
                    (key, value) = record[0:2]
                    cms_map[key] = value
                else:
                    continue

            fp.close()

    def __load_ott_file_id_map(self):
        """
        加载媒资信息. {file_name: [vid,pid,cid,is_full,duration,series_id]}
        :return:
        """
        if len(self.ott_file_id_map) == 0:
            file_path = MediaBaseTable.get_media_conf_file_name("ott_file_id_map")
            if file_path == "":
                sys.stderr.write("get file_path err!")
                sys.exit(-1)
            fp = open(file_path)

            # 跳过第一行
            fp.next()

            for line in fp:
                record = string.split(line.strip('\n'), "\t")
                if len(record) >= 7:
                    (file_name, vid, pid, cid, is_full, duration, series_id) = record[0:7]
                    self.ott_41_pid_url_map[pid + file_name] = vid
                    self.ott_file_id_map[file_name] = vid
                    self.ott_vid_map[vid] = [pid, cid, is_full, duration, series_id]
                else:
                    self.drop_record += 1
                    continue

            fp.close()

    def to_int_vid(self, vid_list):
        """
        ott 转换为mg媒资库vid
        :param vid_list:
        :return:
        """
        for i in range(len(vid_list)):
            vid = vid_list[i]
            if not vid.isdigit():
                vid = str(urllib.unquote(vid)).split('?')[0]
                if len(vid) == 32 and '/' not in str(vid):
                    res = ott_cms_id_map_client.get_svid_by_vid([vid])
                else:
                    res = self.get_vid_by_file_name([vid])

                if res[0] == 0:
                    vid_list[i] = res[1]
                else:
                    return res
            else:
                continue

        return [0, vid_list]

    def pid_to_int_pid(self, pid_list):
        """
        ott 转换为mg媒资库pid
        :param pid_list:
        :return:
        """
        for i in range(len(pid_list)):
            pid = pid_list[i]
            if not pid.isdigit():
                if len(pid) == 32 and '/' not in str(pid):
                    pid_tmp = self.ott_41_nns_import_id_map.get(pid, "")

                    if str(pid_tmp) != "":
                        pid_list[i] = pid_tmp
                else:
                    continue
            else:
                continue

        return [0, pid_list]

    def get_vid_by_file_name(self, file_name_l):
        """
        通过ott file name获取vid
        :param file_name_l: 文件名list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(file_name_l, list) or len(file_name_l) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        file_name = str(file_name_l[0]).strip()

        if file_name == "":
            return [1, "INPUT_IS_NULL"]

        m_info = self.ott_file_id_map.get(file_name)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info]

    def get_series_id_by_vid(self, vid_list):
        """
        通过ott vid获取series_id
        :param vid_list: vid
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vid_list, list) or len(vid_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        vid = vid_list[0]
        if vid == "-" or vid == "":
            return [0, '\N']

        if not str(vid).isdigit():
            return [1, "ID_NOT_INT"]
        m_info = self.ott_vid_map.get(vid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]

        if str(m_info[4]) == "0" or str(m_info[4]).lower() == "null" :
            return [0, '\N']
        else:
            return [0, m_info[4]]

    def get_pid_by_vid(self, vid_list):
        """
        通过ott file name获取vid
        :param vid_list: 文件名list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vid_list, list) or len(vid_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        vid = vid_list[0]
        if vid == "-" or vid == "":
            return [0, '\N']

        if not str(vid).isdigit():
            return [1, "ID_NOT_INT"]
        m_info = self.ott_vid_map.get(vid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info[0]]

    def get_cid_by_vid(self, vid_list):
        """
        通过ott file name获取vid
        :param vid_list: 文件名list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vid_list, list) or len(vid_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        vid = vid_list[0]
        if vid == "-" or vid == "":
            return [0, '\N']

        if not str(vid).isdigit():
            return [1, "ID_NOT_INT"]
        m_info = self.ott_vid_map.get(vid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info[1]]

    def get_is_full_by_vid(self, vid_list):
        """
        通过ott file name获取vid
        :param vid_list: 文件名list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vid_list, list) or len(vid_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        vid = vid_list[0]
        if vid == "-" or vid == "":
            return [0, '\N']

        if not str(vid).isdigit():
            return [1, "ID_NOT_INT"]
        m_info = self.ott_vid_map.get(vid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            if str(m_info[2]) == "2":
                return [0, 0]
            else:
                return [0, m_info[2]]

    def get_vts_by_vid(self, vid_list):
        """
        通过ott file name获取vid
        :param vid_list: 文件名list
        :return: [err_no, int_str or err_msg]
        """
        if not isinstance(vid_list, list) or len(vid_list) != 1:
            return [1, "FORMAT_INPUT_ERR"]

        vid = vid_list[0]
        if vid == "-" or vid == "":
            return [0, '\N']

        if not str(vid).isdigit():
            return [1, "ID_NOT_INT"]
        m_info = self.ott_vid_map.get(vid)

        if m_info is None:
            return [1, "INFO_NOT_FOUND"]
        else:
            return [0, m_info[3]]

    def get_ott41__vid(self, vid_list):
        """
          通过pid url 获取vid
          :param vid_list: 文件名list
          :return: [err_no, int_str or err_msg]
          """

        if not isinstance(vid_list, list) or len(vid_list) != 4:
            return [1, "FORMAT_INPUT_ERR"]

        vid = vid_list[0]
        plid = vid_list[1]
        url = str(urllib.unquote(vid_list[2])).split('?')[0]
        clientver = vid_list[3]

        if clientver == "-" or vid == "":
            return [0, '\N']

        if vid == "-" or vid == "":
            return [0, '\N']

        verlist = str(clientver).split('.')
        if len(verlist) == 0 or clientver.lower() == '4.1.0.219.2.CH.1.4_Release'.lower():
            return [2, [vid]]
        elif len(verlist) >= 6 and verlist[5].lower() == 'sx'.lower():
            return [2, [vid]]

        if plid == "-" or plid == "":
            return [0, '\N']

        # 用pid,url 从缓存中查找vid
        if plid + url in self.ott_41_vid_map:
            return [0, self.ott_41_vid_map[ plid + url ]]

        if plid not in self.ott_41_nns_import_id_map:
            return [1, "VId_NOT_IN_OTT_41_NNS_IMPORT_ID_MAP"]
        nns_import_id = self.ott_41_nns_import_id_map.get(plid)
        if nns_import_id is None:
            return [1, "VId_NOT_IN_OTT_41_NNS_IMPORT_ID_MAP"]

        if url not in self.ott_41_clip_id_name_map:
            return [1, "URL_NOT_INOTT_41_CLIP_ID_NAME_MAP"]
        idlist = self.ott_41_clip_id_name_map.get(url)

        if '|' in str(idlist):
            idarray = str(idlist).split('|')
            for id  in idarray:
                if id == nns_import_id:
                    vid_list[0] = nns_import_id
                    break
        else:
            if str(nns_import_id) == str(idlist):
                vid_list[0] = nns_import_id
            else:
                return [1, "NNS_IMPORT_ID_NOT_EQUALS_CLIP_ID_"]

        if vid_list is None:
            return [1, "VId_NOT_IN_OTT_41_NNS_IMPORT_ID_MAP"]

        if str(vid_list[0]) + url in self.ott_41_pid_url_map:
            self.ott_41_vid_map[ plid + url] = self.ott_41_pid_url_map[str(vid_list[0]) + url]
            return [0, self.ott_41_pid_url_map[str(vid_list[0]) + url]]
        else:
            return [1, "PIDURL_NOT_IN_OTT_41_PID_URL_MAP"]

ott_file_id_map_client = OttFileIdMap()
