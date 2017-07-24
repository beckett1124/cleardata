# encoding: utf-8

from rule.dict_page.dict_web_so_ch import dict_pcweb_so_re_type, dict_pcweb_so_ch_type
from rule.dict_page.dict_web_so_ch import dict_phonem_so_re_type, dict_phonem_so_ch_type


dict_client_ch_type = {
    "pcweb": dict_pcweb_so_ch_type,
    "phonem": dict_phonem_so_ch_type,
    "padweb": dict_pcweb_so_ch_type
}
dict_client_re_type = {
    "pcweb": dict_pcweb_so_re_type,
    "phonem": dict_phonem_so_re_type,
    "padweb": dict_pcweb_so_re_type
}


def get_web_cxid(ch, ref, client_type):
    """
    :param ch: 原cxid
    :param ref: 来源url
    :param client_type: 端类型,string
    :return: [err_no, msg]
    """
    # url为空 或者 不以http开头的,均算为站内，非第三方站点
    if str(ch) == "" or str(ch) == "-":
        return [0, ""]

    if str(ref) == "" or not str(ref).startswith("http"):
        return [0, ch]

    client = str(client_type)
    ref_str = str(ref).strip()
    index_url = ref_str.find("?")
    if index_url >= 0:
        ref_str = ref_str[0:index_url]

    if client in dict_client_ch_type and client in dict_client_re_type:
        dict_ch_type = dict_client_ch_type[client]
        dict_re_type = dict_client_re_type[client]

        for (key, value) in dict_ch_type.items():
            for regex in value:
                pattern = dict_re_type[key][regex[0]]
                match = pattern.match(ref_str)

                if not match:
                    continue

                if len(regex) > 1:
                    return [0, regex[1]]

    return [0, ch]

