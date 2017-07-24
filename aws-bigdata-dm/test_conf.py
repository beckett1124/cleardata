# encodingfrom utf-8

import importlib
import sys
from conf.settings import AppConfig
from commonlib.common import write_to_file
from rule.rule import rule
from commonlib.pydotalog import pydotalog
from commonlib.common import resolve_url


from rule.comm_rule.cn_null import cn_null
from rule.comm_rule.com_date_year import com_date_year
from rule.comm_rule.com_date_month import com_date_month
from rule.comm_rule.com_date_day import com_date_day
from rule.comm_rule.com_time_ms import com_time_ms
from rule.comm_rule.com_time_hour import com_time_hour
from rule.ip_rule.cn_isp import cn_isp
from rule.comm_rule.cn_url import cn_url
from rule.ip_rule.cn_province_by_ip import cn_province_by_ip
from rule.ip_rule.cn_city_by_ip import cn_city_by_ip
from rule.ip_rule.cn_isp_by_ip import cn_isp_by_ip
from rule.comm_rule.com_time_hour_playtime import com_time_hour_playtime
from rule.ip_rule.cn_country import cn_country
from rule.ip_rule.cn_country_by_ip import cn_country_by_ip
from rule.ip_rule.cn_check_domestic import cn_check_domestic
from rule.ip_rule.cn_check_domestic_by_ip import cn_check_domestic_by_ip
from rule.comm_rule.cn_lower import cn_lower
from rule.mobile_rule.cn_fix_iphone_md import CnFixIPhoneMod
from rule.pcweb_rule.cn_fix_web_pix import CnFixWebPix
from rule.comm_rule.cn_bid import cn_bid
from rule.media_rule.media_app_cid_name import MediaAppCidName
from rule.media_rule.media_app_zt_name import MediaAppZtName
from rule.media_rule.media_plid import MediaPLid
from rule.media_rule.media_cid import MediaCid
from rule.media_rule.media_cid_name import MediaCidName
from rule.media_rule.media_plid_name import MediaPidName
from rule.media_rule.media_ott_cid import MediaOttCid
from rule.media_rule.media_live_channel_name import MediaLiveChannelName
from rule.media_rule.media_live_source_name import MediaLiveSourceName
from rule.media_rule.media_ott_pid import MediaOttPid
from rule.media_rule.media_ott_svid import MediaOttSVid
from rule.media_rule.media_ott_vid import MediaOttVid
from rule.mobile_rule.cn_mobile_ref import cn_mobile_ref
from rule.mobile_rule.cn_mobile_url import cn_mobile_url
from rule.ip_rule.cn_city import cn_city
from rule.ip_rule.cn_province import cn_province
from rule.media_rule.media_phone_version_id import MediaPhoneVersionId
from rule.media_rule.media_series_id import MediaSeriesId
from rule.ott_rule.cn_ott_vender_id import CnOttVendId
from rule.ott_rule.cn_ott_version_id import CnOttVersionId
from rule.ott_rule.cn_ott_open_type import CnOttOpenType
from rule.ott_rule.cn_ott_sub_vender_id import CnOttSubVendId
from rule.comm_rule.cn_pv_cid import cn_pv_cid
from rule.comm_rule.cn_pv_pid import cn_pv_pid
from rule.comm_rule.cn_pv_vid import cn_pv_vid
from rule.pcclient_rule.cn_mac_ref import cn_mac_ref
from rule.pcclient_rule.cn_mac_url import cn_mac_url
from rule.pcclient_rule.cn_win10_ref import cn_win10_ref
from rule.pcclient_rule.cn_win10_url import cn_win10_url
from rule.pcclient_rule.cn_win_ref import cn_win_ref
from rule.pcclient_rule.cn_win_url import cn_win_url
from rule.pcweb_rule.cn_pcweb_page_num import cn_pcweb_page_num
from rule.pcweb_rule.cn_pcweb_fpn import cn_pcweb_ref_page_num
from rule.pcweb_rule.cn_refsitetype import cn_refsitetype
from rule.media_rule.media_is_full import MediaIsFull
from rule.media_rule.media_vts import MediaVts
from rule.ott_rule.cn_ott_vender_name import CnOttVendName
from rule.msite_rule.cn_msite_page_num import cn_msite_page_num
from rule.msite_rule.cn_msite_fpn import cn_msite_ref_page_num
from rule.pcweb_rule.cn_pcweb_sub_ch import CnPcWebSubCh
from rule.pcweb_rule.cn_pcweb_ch import CnPcWebCh
from rule.comm_rule.cn_mpp_vend_status import CnMppVendStatus
from rule.pcweb_rule.cn_pcweb_vend_status import CnPcWebVendStatus
from rule.comm_rule.cn_mpp_such import CnMppSubCh
from rule.comm_rule.cn_mpp_ch import CnMppCh
from rule.comm_rule.cn_sid import cn_sid
from rule.pcweb_rule.cn_pcweb_page_id import cn_pcweb_page_id
from rule.media_rule.media_ott_is_full import MediaOttIsFull
from rule.media_rule.media_ott_vts import MediaOttVts
from rule.media_rule.media_ott_series_id import MediaOttSeriesid
from rule.mobile_rule.cn_mobile_vv_ref import cn_mobile_vv_ref

from rule.pcweb_rule.cn_pcweb_url_protocol import cn_pcweb_url_protocol
from rule.pcweb_rule.cn_pcweb_url_site import cn_pcweb_url_site
from rule.pcweb_rule.cn_pcweb_url import cn_pcweb_url
from rule.pcweb_rule.cn_pcweb_chtype import CnPcWebChType
from rule.mglive_rule.cn_mglive_auid import CnMgliveAuid
from rule.mglive_rule.cn_mglive_auid_vod import CnMgliveAuidVod
from rule.mglive_rule.cn_mglive_channel import CnMgliveChannel
from rule.mglive_rule.cn_mglive_room import CnMgliveRoom
from rule.mobile_rule.cn_mobile_activity_by_url import cn_mobile_activity_by_url
from rule.mobile_rule.cn_mobile_handle_h5_url_protocol import cn_mobile_handle_h5_url_protocol
from rule.mobile_rule.cn_mobile_handle_h5_url_site import cn_mobile_handle_h5_url_site
from rule.mobile_rule.cn_mobile_handle_h5_url import cn_mobile_handle_h5_url

from rule.media_rule.media_vrs_vid import MediaVRSVid
from rule.media_rule.media_vrs_clip_id import MediaVRSClipId
from rule.media_rule.media_vrs_series_id import MediaVRSSeriesId
from rule.media_rule.media_vrs_bd_id import MediaVRSBDid
from rule.media_rule.media_vrs_c_id import MediaVRSCid
from rule.media_rule.media_vrs_vts import MediaVRSVts
from rule.media_rule.media_vrs_is_full import MediaVRSIsFull
from rule.media_rule.media_vrs_pv_vid import MediaVRSPvVid
from rule.media_rule.media_vrs_pv_bdid import MediaVRSPvBDid
from rule.media_rule.media_vrs_check_series_id import MediaVRSCheckSid

from rule.ip_rule.cn_check_domesticid_by_ip import cn_check_domesticid_by_ip
from rule.ip_rule.cn_countryid_by_ip import cn_countryid_by_ip
from rule.ip_rule.cn_provinceid_by_ip import cn_provinceid_by_ip
from rule.ip_rule.cn_cityid_by_ip import cn_cityid_by_ip
from rule.ip_rule.cn_ispid_by_ip import cn_ispid_by_ip

from rule.media_rule.media_all_pv_cid import MediaAllPvCid
from rule.media_rule.media_all_pv_plid import MediaAllPvPlid
from rule.media_rule.media_vrs_ott_series_id import MediaVRSOttSeriesId
from rule.ott_rule.cn_ott_ref import cn_ott_ref
from rule.ott_rule.cn_ott_url import cn_ott_url
from rule.ott_rule.cn_ott_pagenum import cn_ott_page_num

from rule.mobile_rule.cn_mobile_fpron import cn_mobile_fpron
from rule.mobile_rule.cn_mobile_fsubpron import cn_mobile_fsubpron
from rule.mobile_rule.cn_mobile_pron import cn_mobile_pron
from rule.mobile_rule.cn_mobile_subpron import cn_mobile_subpron

from rule.pcweb_rule.cn_pcweb_fpron import cn_pcweb_fpron
from rule.pcweb_rule.cn_pcweb_fsubpron import cn_pcweb_fsubpron
from rule.pcweb_rule.cn_pcweb_pron import cn_pcweb_pron
from rule.pcweb_rule.cn_pcweb_subpron import cn_pcweb_subpron

from rule.msite_rule.cn_msite_fpron import cn_msite_fpron
from rule.msite_rule.cn_msite_fsubpron import cn_msite_fsubpron
from rule.msite_rule.cn_msite_pron import cn_msite_fpron
from rule.msite_rule.cn_msite_subpron import cn_msite_subpron

from rule.ott_rule.cn_ott_fpron import cn_ott_fpron
from rule.ott_rule.cn_ott_fsubpron import cn_ott_fsubpron
from rule.ott_rule.cn_ott_pron import cn_ott_pron
from rule.ott_rule.cn_ott_subpron import cn_ott_subpron

from rule.mobile_rule.cn_mobile_check_5 import cn_mobile_check_5
from rule.ott_rule.cn_ott_check_5 import cn_ott_check_5

from rule.msite_rule.cn_msite_fix_ch import cn_msite_fix_ch

from rule.media_rule.media_offline_pid import MediaOfflinePLid
from rule.media_rule.media_offline_bdid import MediaOfflineBDid

from rule.msite_rule.cn_msite_ch import CnMSiteCh
from rule.msite_rule.cn_msite_chtype import CnMSiteChType

from rule.media_rule.media_check_live_channel_id import MediaCheckLiveChannelId
from rule.media_rule.media_offline_cid import MediaOfflineCid

from rule.mobile_rule.cn_mobile_old_net import cn_mobile_old_net
from rule.comm_rule.cn_abnormal_check import cn_abnormal_check

from rule.media_rule.media_bd_cid import MediaBDCid
from rule.media_rule.media_ott_bd_cid import MediaOttBDCid

from rule.oth_client_rule.cn_tvos_url import cn_tvos_url
from rule.media_rule.media_vrs_cid_by_vid import MediaVRSCidByVid
from rule.media_rule.media_vrs_clipid_by_vid import MediaVRSClipIdByVid
from rule.media_rule.media_vrs_seriesid_by_vid import MediaVRSSeriesIdByVid
from rule.comm_rule.cn_fix_vv_cpn import cn_fix_vv_cpn
from rule.media_rule.media_vrs_ott_vid import MediaVRSOTTVid

from rule.media_rule.media_vrs_bd_cid import MediaVrsBDCid
from rule.pcclient_rule.cn_pcclient_ch import CnPcClientCh

from rule.media_rule.media_vrs_ott_cid import MediaVRSOttCid
from rule.oth_client_rule.cn_weixin_ch import CnWeiXinCh
from rule.ott_rule.cn_fix_ott_mf import CnFixOTTMf
from rule.oth_client_rule.cn_weixin_url import CnWeiXinUrl

from rule.boss_order.cn_border_bid import cn_border_bid
from rule.boss_order.cn_border_ch import CnBOrderCh
from rule.boss_order.cn_border_chtype import CnBOrderChType
from rule.boss_order.cn_border_subch import CnBOrderSubCh
from rule.boss_order.cn_border_version import CnBOrderVersionId

from rule.boss_order.cn_border_country_by_ip import cn_border_countryid_by_ip
from rule.boss_order.cn_border_provin_by_ip import cn_border_provinceid_by_ip
from rule.boss_order.cn_border_city_by_ip import cn_border_border_cityid_by_ip
from rule.boss_order.cn_border_isp_by_ip import cn_border_ispid_by_ip
from rule.boss_order.cn_border_domes_by_ip import cn_border_check_domesticid_by_ip
