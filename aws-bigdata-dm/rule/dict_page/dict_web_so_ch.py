# encoding: utf-8

import re

dict_pcweb_so_ch_type = {
    "90f0zbamf": [["(http|https)://(www\.|video\.)?so.com/?.*", "914i9wclw"]],
    "94n3624ea": [["http://(www\.|v\.|tv\.)?sogou.com/?.*", "90fdk2mz8"]],
    "94l62sj44": [["http://(www\.)?cn.bing.com/?.*", "90f9ebjdg"], ["http://(www\.)?chianso.com/?.*", "90f12kwr8"],
                  ["http://(www\.)?so.le.com/?.*", "90f6m9z9w"], ["http://(www\.)?so.tv.sohu.com/?.*", "90fdk41jo"]],
    "90fe36tp1": [["http://(www\.)?v.qq.com/x/search/?.*", "90fe36x90"]],
    "90fdkdqrm": [["http://(www\.)?soku.com/?.*", "90fd092hg"]]
}


dict_phonem_so_ch_type = {
    "90f0zbamf": [["(http|https)://(m\.|m\.video\.)so.com/?.*", "914i9wclw"]],
    "94n3624ea": [["http://(m\.|m\.v\.)sogou.com/?.*", "90fdk2mz8"]],
    "94l62sj44": [["http://m\.le.com/?.*", "90f6m9z9w"], ["http://m\.tv.sohu.com/?.*", "90fdk41jo"]],
    "90fe36tp1": [["http://m\.v.qq.com/?.*", "90fe36x90"]],
    "90fdkdqrm": [["http://(www\.)?youku.com/?.*", "90fd092hg"]],
    "90fczxty2": [["http://so\.m.sm.cn/?.*", "90fdkb2dw"]]

}


dict_pcweb_so_re_type = {}
for (key, value) in dict_pcweb_so_ch_type.items():
        dict_pcweb_so_re_type[key] = {}
        for regex in value:
            pattern = re.compile(regex[0])
            dict_pcweb_so_re_type[key][regex[0]] = pattern

dict_phonem_so_re_type = {}
for (key, value) in dict_phonem_so_ch_type.items():
        dict_phonem_so_re_type[key] = {}
        for regex in value:
            pattern = re.compile(regex[0])
            dict_phonem_so_re_type[key][regex[0]] = pattern
