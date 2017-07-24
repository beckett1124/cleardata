#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-17T20:02:02+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-19T10:06:18+08:00
import importlib
import sys
from conf.settings import AppConfig
from commonlib.common import write_to_file
from rule.rule import rule
from commonlib.pydotalog import pydotalog
from commonlib.common import resolve_url

rule_dict = {
    100: ["rule.comm_rule.cn_null", "cn_null"],
    101: ["rule.comm_rule.com_date_year", "com_date_year"],
    102: ["rule.comm_rule.com_date_month", "com_date_month"],
    103: ["rule.comm_rule.com_date_day", "com_date_day"],
    104: ["rule.comm_rule.com_time_ms", "com_time_ms"],
    105: ["rule.comm_rule.com_time_hour", "com_time_hour"],
    106: ["rule.ip_rule.cn_isp", "cn_isp"],
    107: ["rule.comm_rule.cn_url", "cn_url"],
    108: ["rule.ip_rule.cn_province_by_ip", "cn_province_by_ip"],
    109: ["rule.ip_rule.cn_city_by_ip", "cn_city_by_ip"],
    110: ["rule.ip_rule.cn_isp_by_ip", "cn_isp_by_ip"],
    111: ["rule.comm_rule.com_time_hour_playtime", "com_time_hour_playtime"],
    112: ["rule.ip_rule.cn_country", "cn_country"],
    113: ["rule.ip_rule.cn_country_by_ip", "cn_country_by_ip"],
    114: ["rule.ip_rule.cn_check_domestic", "cn_check_domestic"],
    115: ["rule.ip_rule.cn_check_domestic_by_ip", "cn_check_domestic_by_ip"],
    116: ["rule.comm_rule.cn_lower", "cn_lower"],
    117: ["rule.mobile_rule.cn_fix_iphone_md", "CnFixIPhoneMod"],
    118: ["rule.pcweb_rule.cn_fix_web_pix", "CnFixWebPix"],
    119: ["rule.mobile_rule.cn_fix_mobile_mf", "CnFixMobileMf"],
    201: ["rule.comm_rule.cn_bid", "cn_bid"],
    203: ["rule.media_rule.media_app_cid_name", "MediaAppCidName"],
    204: ["rule.media_rule.media_app_zt_name", "MediaAppZtName"],
    205: ["rule.media_rule.media_plid", "MediaPLid"],
    206: ["rule.media_rule.media_cid", "MediaCid"],
    207: ["rule.media_rule.media_cid_name", "MediaCidName"],
    208: ["rule.media_rule.media_plid_name", "MediaPidName"],
    209: ["rule.media_rule.media_ott_cid", "MediaOttCid"],
    210: ["rule.media_rule.media_live_channel_name", "MediaLiveChannelName"],
    211: ["rule.media_rule.media_live_source_name", "MediaLiveSourceName"],
    213: ["rule.media_rule.media_ott_pid", "MediaOttPid"],
    214: ["rule.media_rule.media_ott_svid", "MediaOttSVid"],
    215: ["rule.media_rule.media_ott_vid", "MediaOttVid"],
    216: ["rule.mobile_rule.cn_mobile_ref", "cn_mobile_ref"],
    217: ["rule.mobile_rule.cn_mobile_url", "cn_mobile_url"],
    218: ["rule.ip_rule.cn_city", "cn_city"],
    219: ["rule.ip_rule.cn_province", "cn_province"],
    220: ["rule.media_rule.media_phone_version_id", "MediaPhoneVersionId"],
    221: ["rule.media_rule.media_series_id", "MediaSeriesId"],
    222: ["rule.ott_rule.cn_ott_vender_id", "CnOttVendId"],
    223: ["rule.ott_rule.cn_ott_version_id", "CnOttVersionId"],
    224: ["rule.ott_rule.cn_ott_open_type", "CnOttOpenType"],
    225: ["rule.ott_rule.cn_ott_sub_vender_id", "CnOttSubVendId"],
    226: ["rule.comm_rule.cn_pv_cid", "cn_pv_cid"],
    227: ["rule.comm_rule.cn_pv_pid", "cn_pv_pid"],
    228: ["rule.comm_rule.cn_pv_vid", "cn_pv_vid"],
    229: ["rule.pcclient_rule.cn_mac_ref", "cn_mac_ref"],
    230: ["rule.pcclient_rule.cn_mac_url", "cn_mac_url"],
    231: ["rule.pcclient_rule.cn_win10_ref", "cn_win10_ref"],
    232: ["rule.pcclient_rule.cn_win10_url", "cn_win10_url"],
    233: ["rule.pcclient_rule.cn_win_ref", "cn_win_ref"],
    234: ["rule.pcclient_rule.cn_win_url", "cn_win_url"],
    235: ["rule.pcweb_rule.cn_pcweb_page_num", "cn_pcweb_page_num"],
    236: ["rule.pcweb_rule.cn_pcweb_fpn", "cn_pcweb_ref_page_num"],
    237: ["rule.pcweb_rule.cn_refsitetype", "cn_refsitetype"],
    238: ["rule.media_rule.media_is_full", "MediaIsFull"],
    239: ["rule.media_rule.media_vts", "MediaVts"],
    240: ["rule.ott_rule.cn_ott_vender_name", "CnOttVendName"],
    241: ["rule.msite_rule.cn_msite_page_num", "cn_msite_page_num"],
    242: ["rule.msite_rule.cn_msite_fpn", "cn_msite_ref_page_num"],
    243: ["rule.pcweb_rule.cn_pcweb_sub_ch", "CnPcWebSubCh"],
    244: ["rule.pcweb_rule.cn_pcweb_ch", "CnPcWebCh"],
    245: ["rule.comm_rule.cn_mpp_vend_status", "CnMppVendStatus"],
    246: ["rule.pcweb_rule.cn_pcweb_vend_status", "CnPcWebVendStatus"],
    247: ["rule.comm_rule.cn_mpp_such", "CnMppSubCh"],
    248: ["rule.comm_rule.cn_mpp_ch", "CnMppCh"],
    249: ["rule.comm_rule.cn_sid", "cn_sid"],
    250: ["rule.pcweb_rule.cn_pcweb_page_id", "cn_pcweb_page_id"],
    251: ["rule.media_rule.media_ott_is_full", "MediaOttIsFull"],
    252: ["rule.media_rule.media_ott_vts", "MediaOttVts"],
    253: ["rule.media_rule.media_ott_series_id", "MediaOttSeriesid"],
    254: ["rule.mobile_rule.cn_mobile_vv_ref", "cn_mobile_vv_ref"],

    255: ["rule.pcweb_rule.cn_pcweb_url_protocol", "cn_pcweb_url_protocol"],
    256: ["rule.pcweb_rule.cn_pcweb_url_site", "cn_pcweb_url_site"],
    257: ["rule.pcweb_rule.cn_pcweb_url", "cn_pcweb_url"],
    258: ["rule.pcweb_rule.cn_pcweb_chtype", "CnPcWebChType"],
    259: ["rule.mglive_rule.cn_mglive_auid", "CnMgliveAuid"],
    260: ["rule.mglive_rule.cn_mglive_auid_vod", "CnMgliveAuidVod"],
    261: ["rule.mglive_rule.cn_mglive_channel", "CnMgliveChannel"],
    262: ["rule.mglive_rule.cn_mglive_room", "CnMgliveRoom"],
    263: ["rule.mobile_rule.cn_mobile_activity_by_url", "cn_mobile_activity_by_url"],
    264: ["rule.mobile_rule.cn_mobile_handle_h5_url_protocol", "cn_mobile_handle_h5_url_protocol"],
    265: ["rule.mobile_rule.cn_mobile_handle_h5_url_site", "cn_mobile_handle_h5_url_site"],
    266: ["rule.mobile_rule.cn_mobile_handle_h5_url", "cn_mobile_handle_h5_url"],

    267: ["rule.media_rule.media_vrs_vid", "MediaVRSVid"],
    268: ["rule.media_rule.media_vrs_clip_id", "MediaVRSClipId"],
    269: ["rule.media_rule.media_vrs_series_id", "MediaVRSSeriesId"],
    270: ["rule.media_rule.media_vrs_bd_id", "MediaVRSBDid"],
    271: ["rule.media_rule.media_vrs_c_id", "MediaVRSCid"],
    272: ["rule.media_rule.media_vrs_vts", "MediaVRSVts"],
    273: ["rule.media_rule.media_vrs_is_full", "MediaVRSIsFull"],
    274: ["rule.media_rule.media_vrs_pv_vid", "MediaVRSPvVid"],
    275: ["rule.media_rule.media_vrs_pv_bdid", "MediaVRSPvBDid"],
    276: ["rule.media_rule.media_vrs_check_series_id", "MediaVRSCheckSid"],

    283: ["rule.ip_rule.cn_check_domesticid_by_ip", "cn_check_domesticid_by_ip"],
    284: ["rule.ip_rule.cn_countryid_by_ip", "cn_countryid_by_ip"],
    285: ["rule.ip_rule.cn_provinceid_by_ip", "cn_provinceid_by_ip"],
    286: ["rule.ip_rule.cn_cityid_by_ip", "cn_cityid_by_ip"],
    287: ["rule.ip_rule.cn_ispid_by_ip", "cn_ispid_by_ip"],

    277: ["rule.media_rule.media_all_pv_cid", "MediaAllPvCid"],
    278: ["rule.media_rule.media_all_pv_plid", "MediaAllPvPlid"],
    279: ["rule.media_rule.media_vrs_ott_series_id", "MediaVRSOttSeriesId"],
    280: ["rule.ott_rule.cn_ott_ref", "cn_ott_ref"],
    281: ["rule.ott_rule.cn_ott_url", "cn_ott_url"],
    282: ["rule.ott_rule.cn_ott_pagenum", "cn_ott_page_num"],

    288: ["rule.mobile_rule.cn_mobile_fpron", "cn_mobile_fpron"],
    289: ["rule.mobile_rule.cn_mobile_fsubpron", "cn_mobile_fsubpron"],
    290: ["rule.mobile_rule.cn_mobile_pron", "cn_mobile_pron"],
    291: ["rule.mobile_rule.cn_mobile_subpron", "cn_mobile_subpron"],

    292: ["rule.pcweb_rule.cn_pcweb_fpron", "cn_pcweb_fpron"],
    293: ["rule.pcweb_rule.cn_pcweb_fsubpron", "cn_pcweb_fsubpron"],
    294: ["rule.pcweb_rule.cn_pcweb_pron", "cn_pcweb_pron"],
    295: ["rule.pcweb_rule.cn_pcweb_subpron", "cn_pcweb_subpron"],

    296: ["rule.msite_rule.cn_msite_fpron", "cn_msite_fpron"],
    297: ["rule.msite_rule.cn_msite_fsubpron", "cn_msite_fsubpron"],
    298: ["rule.msite_rule.cn_msite_pron", "cn_msite_fpron"],
    299: ["rule.msite_rule.cn_msite_subpron", "cn_msite_subpron"],

    300: ["rule.ott_rule.cn_ott_fpron", "cn_ott_fpron"],
    301: ["rule.ott_rule.cn_ott_fsubpron", "cn_ott_fsubpron"],
    302: ["rule.ott_rule.cn_ott_pron", "cn_ott_pron"],
    303: ["rule.ott_rule.cn_ott_subpron", "cn_ott_subpron"],

    304: ["rule.mobile_rule.cn_mobile_check_5", "cn_mobile_check_5"],
    305: ["rule.ott_rule.cn_ott_check_5", "cn_ott_check_5"],

    306: ["rule.msite_rule.cn_msite_fix_ch", "cn_msite_fix_ch"],

    307: ["rule.media_rule.media_offline_pid", "MediaOfflinePLid"],
    308: ["rule.media_rule.media_offline_bdid", "MediaOfflineBDid"],

    309: ["rule.msite_rule.cn_msite_ch", "CnMSiteCh"],
    310: ["rule.msite_rule.cn_msite_chtype", "CnMSiteChType"],

    311: ["rule.media_rule.media_check_live_channel_id", "MediaCheckLiveChannelId"],
    312: ["rule.media_rule.media_offline_cid", "MediaOfflineCid"],

    313: ["rule.mobile_rule.cn_mobile_old_net", "cn_mobile_old_net"],
    314: ["rule.comm_rule.cn_abnormal_check", "cn_abnormal_check"],

    315: ["rule.media_rule.media_bd_cid", "MediaBDCid"],
    316: ["rule.media_rule.media_ott_bd_cid", "MediaOttBDCid"],

    317: ["rule.oth_client_rule.cn_tvos_url", "cn_tvos_url"],
    318: ["rule.media_rule.media_vrs_cid_by_vid", "MediaVRSCidByVid"],
    319: ["rule.media_rule.media_vrs_clipid_by_vid", "MediaVRSClipIdByVid"],
    320: ["rule.media_rule.media_vrs_seriesid_by_vid", "MediaVRSSeriesIdByVid"],
    321: ["rule.comm_rule.cn_fix_vv_cpn", "cn_fix_vv_cpn"],
    322: ["rule.media_rule.media_vrs_ott_vid", "MediaVRSOTTVid"],

    323: ["rule.media_rule.media_vrs_bd_cid", "MediaVrsBDCid"],
    324: ["rule.pcclient_rule.cn_pcclient_ch", "CnPcClientCh"],

    325: ["rule.media_rule.media_vrs_ott_cid", "MediaVRSOttCid"],
    326: ["rule.oth_client_rule.cn_weixin_ch", "CnWeiXinCh"],
    327: ["rule.ott_rule.cn_fix_ott_mf", "CnFixOTTMf"],
    328: ["rule.oth_client_rule.cn_weixin_url", "CnWeiXinUrl"],

    329: ["rule.boss_order.cn_border_bid", "cn_border_bid"],
    330: ["rule.boss_order.cn_border_ch", "CnBOrderCh"],
    331: ["rule.boss_order.cn_border_chtype", "CnBOrderChType"],
    332: ["rule.boss_order.cn_border_subch", "CnBOrderSubCh"],
    333: ["rule.boss_order.cn_border_version", "CnBOrderVersionId"],

    334: ["rule.boss_order.cn_border_country_by_ip", "cn_border_countryid_by_ip"],
    335: ["rule.boss_order.cn_border_provin_by_ip", "cn_border_provinceid_by_ip"],
    336: ["rule.boss_order.cn_border_city_by_ip", "cn_border_border_cityid_by_ip"],
    337: ["rule.boss_order.cn_border_isp_by_ip", "cn_border_ispid_by_ip"],
    338: ["rule.boss_order.cn_border_domes_by_ip", "cn_border_check_domesticid_by_ip"],

    339: ["rule.media_rule.media_ott_bdid", "MediaOTTBDid"],

    340: ["rule.ott_rule.cn_ott_big_ver", "cn_ott_big_ver"],
    341: ["rule.mobile_rule.cn_mobile_big_ver", "cn_mobile_big_ver"],
    342: ["rule.comm_rule.cn_mpp_big_ver", "cn_mpp_big_ver"],
    343: ["rule.pcclient_rule.cn_mac_big_ver", "cn_mac_big_ver"],

    344: ["rule.ott_rule.cn_fix_ott_os", "CnFixOTTOs"],

}


class scheduling(object):
    '''
    :换算组装类
    '''

    def __init__(self,topicname,dm_name,recv_time):
        self.topicname=topicname
        self.dm_name=dm_name
        self.recv_time=recv_time
        self.input_config=AppConfig[topicname]['input_key_list']
        self.dm_config_output_key=AppConfig[topicname][dm_name]['output_key_list']
        self.dm_config_output_dict=AppConfig[topicname][dm_name]['output_dict']
        self.output_file_prefix=self.topicname+"_"+self.dm_name
        self.write_to_file=write_to_file
        self.my_rule_dict = {}

        # 初始化所需要模块
        self.init_import_module()

    def init_import_module(self):
        for _output_index in range(len(self.dm_config_output_key)):
            _output_field = self.dm_config_output_key[_output_index]
            _rule_config = self.dm_config_output_dict[_output_field]

            if _rule_config is None or len(_rule_config) < 2:
                pydotalog.error('%s,%s' % ("config_err", str(_rule_config)))
                sys.exit(-1)

            _rule_import_num = _rule_config[1]
            if _rule_import_num in [0, 1, 2, -1]:
                continue

            if _rule_import_num not in rule_dict.keys():
                pydotalog.error('This rule_id[%s] is not in rule_dict' % str(_rule_import_num))
                sys.exit(-1)

            _rule_import_list = rule_dict[_rule_import_num]
            if _rule_import_list is None or len(_rule_import_list) != 2:
                pydotalog.error('%s, rule_num:[%s]' % ("rule_dict_config_failed", str(_rule_import_num)))
                sys.exit(-1)

            _rule_import_module = _rule_import_list[0]
            _rule_class_name = _rule_import_list[1]

            try:
                module_name = importlib.import_module(_rule_import_module)
            except ImportError:
                pydotalog.error('%s, rule_module:[%s]' % ("import module failed ", str(_rule_import_module)))
                sys.exit(-1)

            _rule_class_str = getattr(module_name, _rule_class_name, "no_class")
            if _rule_class_str == "no_class":
                pydotalog.error('%s, rule_class:[%s]' % ("get module class failed ", _rule_class_name))
                sys.exit(-1)

            self.my_rule_dict[_rule_import_num] = _rule_class_str()

            if not isinstance(self.my_rule_dict[_rule_import_num], rule):
                pydotalog.error('%s,%s' % ("config_class_failed, not rule_class", _rule_class_name))
                sys.exit(-1)

    def proccess_line(self,line):
        '''
        :根据配置文件的情况处理数据
        '''
        if line is None or line=='':
            return [-1,'']

        #将数据转换成Dict
        _res=self.getDict(line)

        if _res[0]>0:
            #有字典转换错误
            self.write_to_file('%s,%s' % (_res[1],line),self.output_file_prefix,self.recv_time,self.recv_time,"dm_err")
            return


        #定义需要输出的数据List
        _output_list={}
        for _output_index in  range(len(self.dm_config_output_key)):
            #根据需要输入的字段获取Dict中的配置然后调用规则的脚本进行换算
            _output_field=self.dm_config_output_key[_output_index]
            _rule_config=self.dm_config_output_dict[_output_field]

            if _rule_config is None or len(_rule_config)<2:
                pydotalog.error('%s,%s' % ("config_no",line))
                return

            #判断是否有字段，和有对应的规则
            _rule_config_field=_rule_config[0]
            _rule_config_class=_rule_config[1]

            if _rule_config_field is None:
                pydotalog.error('%s,%s' % ("config_field",line))
                return

            if _rule_config_class == 0:
                _output_list[_output_field] = _res[1][_rule_config_field]
            elif _rule_config_class == 1:
                if str(_res[1][_rule_config_field]).isdigit():
                    _output_list[_output_field] = _res[1][_rule_config_field]
                else:
                    _output_list[_output_field] = '\N'
            elif _rule_config_class == 2:
                if str(_res[1][_rule_config_field]).isdigit():
                    _output_list[_output_field] = _res[1][_rule_config_field]
                else:
                    _output_list[_output_field] = '-1'
            elif _rule_config_class == -1:
                _output_list[_output_field] = _rule_config_field
            else:
                if _rule_config_field == "":
                    pydotalog.error('%s,%s' % ("config_field_null",line))
                    return

                if _rule_config_class not in self.my_rule_dict.keys():
                    pydotalog.error('This rule_id[%s] is failed to init to my_rule_dict ' % str(_rule_config_class))
                    return

                _rule_class = self.my_rule_dict[_rule_config_class]
                if _rule_config_class is None or not isinstance(_rule_class,rule):
                    pydotalog.error('%s,%s' % ("config_class",line))
                    return

                #如果config_field 包含了多个字段使用|进行分融
                _field_list=_rule_config_field.strip().split('|')

                #获取每个字段的值
                _field_values=[]

                for _field_list_index in range(len(_field_list)):
                    _field_values.append(_res[1][_field_list[_field_list_index]])


                #将拼装的各字段的值转给规则。并获取返回值
                _rule_res=_rule_class.convert(_field_values)

                if len(_rule_res)!=2:
                    self.write_to_file('%s,%s' % ("rule_return",line),self.output_file_prefix,self.recv_time,self.recv_time,"dm_err")
                    return

                if _rule_res[0] != 0:
                    self.write_to_file('rule_%s_%s,%s' % (_rule_config_class,_rule_res[1],line),self.output_file_prefix,self.recv_time,self.recv_time,"dm_err")
                    return

                _output_list[_output_field]=_rule_res[1]

        #字段解析完成并换算完成
        _write_res=self.gen_des_line(_output_list)
        if _write_res[0]!=0:
            self.write_to_file('analyze_%s,%s' % (_write_res[1],line),self.output_file_prefix,self.recv_time,self.recv_time,"dm_err")
        else:
            self.write_to_file(_write_res[1], self.output_file_prefix, self.recv_time, self.recv_time, 'des')

    def gen_des_line(self, des_dict):
        """
        将des_dict拼接成des line
        :param des_dict: 清洗完成后的des字典
        :type des_dict: dict
        :return: string
        """
        diff_key = list(set(self.dm_config_output_key).difference(set(des_dict)))
        if len(diff_key) != 0:
            return [-2, "topic_name:%s,des_dict not key:%s" % (self.topicname, str(diff_key))]
        result = ("{%s}" % ('},{'.join(self.dm_config_output_key))).format(**des_dict)

        # 替换换行符
        return [0, result.replace('\n', '')]

    def getDict(self, line):
        """
        :将一条数据解析为字典形性
        """
        _dict = {}
        _fields = line.strip().split(',')
        # 判断字典中的列数与配置的是否相等
        if len(self.input_config) > len(_fields):
            return [1, "len"]  # 要求字段长度大于des

        for index in range(len(self.input_config)):
            key = self.input_config[index]
            value = _fields[index]
            if key == "url" or key == "ref":
                _v_res = resolve_url(value)
                if _v_res[0] != 0:
                    return _v_res
                else:
                    value = _v_res[1]
            _dict[key] = value

        return [0, _dict]
