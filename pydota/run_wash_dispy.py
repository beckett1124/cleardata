#!/usr/bin/env python
# encoding: utf-8

import os
import sys
if 'pydota' not in sys.modules and __name__ == '__main__':
    import pythonpathsetter

from pydota.format.format_pcweb_pv import PcWebPvFormat
from pydota.format.format_mobile_pv import MobilePvFormat
from pydota.format.format_iphone_pvs import IphonePvsFormat
from pydota.format.format_ott_pv import OttPvFormat
from pydota.format.format_msite_pv import MSitePvFormat
from pydota.format.format_mac_pv import MacPvFormat

from pydota.format.format_mpp_vv_pcweb import MppVVPcWebFormat
from pydota.format.format_mpp_vv_macclient_121_20151028 import MppVVMacClientFormat
from pydota.format.format_mpp_vv_mobile import MppVVMobileFormat
from pydota.format.format_mpp_vv_mobile_211_20151012 import MppVVMobile211Format
from pydota.format.format_mpp_vv_mobile_new_version import MppVVMobileNewVersionFormat
from pydota.format.format_mpp_vv_ott import MppVVOttFormat
from pydota.format.format_ott_vv_311_20151012 import OttVV311Format
from pydota.format.format_ott_vv_41 import OttVV41Format
from pydota.format.format_ott_vv_44 import OttVV44Format
from pydota.format.format_mpp_vv_padweb import MppVVPadWebFormat
from pydota.format.format_mpp_vv_pcclient import MppVVPcClientFormat
from pydota.format.format_mpp_vv_msite import MppVVMSiteFormat
from pydota.format.format_mpp_vv_win10client_511_20151030 import MppVVWin10ClientFormat
from pydota.format.format_macclient_vv_811_20151210 import MacClientVV811Format
from pydota.format.format_pcweb_1110_20151223 import PcWeb1110Format
from pydota.format.format_phonem_vod_4110_20160317 import PhoneMVod41110Format
from pydota.format.format_dau_ott_340 import DauOtt340Format

from pydota.format.format_mpp_vv_mobile_211_20151012_live import LiveMppVVMobile211Format
from pydota.format.format_macclient_live_8111_20160105 import MacClientLiveFormat
from pydota.format.format_mobile_live_2011_20151105 import MobileLive2011Format
from pydota.format.format_mobile_live_2111_20151225 import MobileLive2111Format
from pydota.format.format_mobile_live_2111_20151225_aws import MobileLive2111AwsFormat
from pydota.format.format_rt_live_pcweb import RtLivePcWebFormat
from pydota.format.format_ott_live import OttLiveFormat

from pydota.format.format_mglive_base import MgLiveBaseFormat
from pydota.format.format_mobile_offline_vv import MobileOffLineVVFormat

from pydota.commonlib.pydotalog import pydotalog
from pydota.format.pydota_common_new import write_to_file, close_files

topic_class_dict = {'pcweb_pv': PcWebPvFormat,
                    'mobile_pv': MobilePvFormat,
                    'mpp_vv_pcweb': MppVVPcWebFormat,
                    'mpp_vv_macclient_121_20151028': MppVVMacClientFormat,
                    'mpp_vv_mobile': MppVVMobileFormat,
                    'mpp_vv_mobile_211_20151012': MppVVMobile211Format,
                    'mpp_vv_mobile_new_version': MppVVMobileNewVersionFormat,
                    'mpp_vv_ott': MppVVOttFormat, 'dau_ott': MppVVOttFormat,
                    'ott_vv_311_20151012': OttVV311Format,
                    'ott_vv_41': OttVV41Format, 'dau_ott_41': OttVV41Format,
                    'ott_vv_44': OttVV44Format, 'dau_ott_44': OttVV44Format, 'dau_ott_340': DauOtt340Format,
                    'mpp_vv_padweb': MppVVPadWebFormat,
                    'mpp_vv_pcclient': MppVVPcClientFormat,
                    'mpp_vv_msite': MppVVMSiteFormat,
                    'mpp_vv_win10client_511_20151030': MppVVWin10ClientFormat,
                    'macclient_vv_811_20151210': MacClientVV811Format,
                    'pcweb_1110_20151223': PcWeb1110Format,
                    'mpp_vv_mobile_211_20151012_live': LiveMppVVMobile211Format,
                    'macclient_live_8111_20160105': MacClientLiveFormat,
                    'mobile_live_2011_20151105': MobileLive2011Format,
                    'mobile_live_2111_20151225': MobileLive2111Format,
                    'mobile_live_2111_20151225_aws': MobileLive2111AwsFormat,
                    'rt_live_pcweb': RtLivePcWebFormat,
                    'ott_live': OttLiveFormat,
                    'iphone_pvs': IphonePvsFormat, 'aphone_pvs': IphonePvsFormat,
                    'phonem_vod_4110_20160317': PhoneMVod41110Format,
                    'ott_pv': OttPvFormat, 'dau_ott_3111': OttPvFormat,
                    'msite_pv': MSitePvFormat,
                    'mac_pv': MacPvFormat, 'win10client_pv': MacPvFormat, 'pcclient_pv': MacPvFormat,
                    'mgliveaphone_vodplay': MgLiveBaseFormat, 'mgliveaphone_auplay': MgLiveBaseFormat, 'mgliveaphone_rmplay': MgLiveBaseFormat,
                    'mgliveiphone_vodplay': MgLiveBaseFormat, 'mgliveiphone_auplay': MgLiveBaseFormat, 'mgliveiphone_rmplay': MgLiveBaseFormat,
                    'mobile_offline_vv': MobileOffLineVVFormat}


def get_class_name(topic_name, start_time):
    if topic_name not in topic_class_dict.keys():
        return (-1, 'topic : %s format class not found' % topic_name)
    return (0, topic_class_dict.get(topic_name)(start_time, topic_name))


def process_main():
    for line in sys.stdin:
        res = format_client.processFormat(line)
        if res[0] == -1:
            write_to_file(res[1], topic_name, res[2], start_time, 'orig_err')
            continue
        elif res[0] == -2:
            write_to_file(res[1], topic_name, res[2], start_time, 'des_err')
        elif res[0] == 0:
            write_to_file(res[1], topic_name, res[2], start_time, 'des')
        # 批量上报的自己写入文件，不通过该程序写入
        elif res[0] == 99:
            continue

        if topic_name != "mpp_vv_mobile_211_20151012_live":
            write_to_file(line, topic_name, res[2], start_time, 'orig')

    close_files()


if __name__ == "__main__":

    log_dir = os.path.join(os.path.dirname(__file__), "../log/")
    pydotalog.init_logger(log_dir + "/pydota_run.log")

    if len(sys.argv) == 3:
        (di, topic_name, start_time) = sys.argv
        (rt, format_client) = get_class_name(topic_name, start_time)

        if rt != 0:
            pydotalog.error(format_client)
            sys.exit(-1)

        if len(start_time) != 12:
            pydotalog.error("topic:[%s] start_time format error, start_time: %s", topic_name, start_time)
            sys.exit(-1)

        process_main()

        i_rows = format_client.input_log_num
        o_rows = format_client.output_log_num
        e_rows = format_client.err_log_num
        s_rows = format_client.drop_log_num

        pydotalog.info("input_rows[%d], output_rows[%d], err_rows[%d], drop_rows[%d]", i_rows, o_rows, e_rows, s_rows)

        print '{0}\n{1}\n{2}\n{3}\n'.format(i_rows, o_rows, e_rows, s_rows)

    else:
        pydotalog.error('arg is topic_name date')
        sys.exit(-1)