# encoding: utf-8
# @Author: gibbs
# @Date:   2016-06-12T12:15:07+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-06-12T12:23:07+08:00
import re

# 12表示规则不能匹配的站内地址
dict_msite_page_type = {
    "0": [["http://m.(beta.)?mgtv.com/#/channel/(home|143|1001)/?(#.*)?$", 1000084, 143]],
    "1": [["http://m.(beta.)?mgtv.com/#/splash.*", 1000195, 1000197]],
    "2": [["http://m.(beta.)?mgtv.com/#/channel/(show|144|1003)/?(#.*)?$", 1000084, 144],
          ["http://m.(beta.)?mgtv.com/#/channel/(tv|130|1004)/?(#.*)?$", 1000084, 130],
          ["http://m.(beta.)?mgtv.com/#/channel/(movie|131|1005)/?(#.*)?$", 1000084, 131],
          ["http://m.(beta.)?mgtv.com/#/channel/(cartoon|132|1006)/?(#.*)?$", 1000084, 132],
          ["http://m.(beta.)?mgtv.com/#/channel/(child|133|1021)/?(#.*)?$", 1000084, 133],
          ["http://m.(beta.)?mgtv.com/#/channel/(news|1010|134)/?(#.*)?$", 1000084, 134],
          ["http://m.(beta.)?mgtv.com/#/channel/(music|145|1007)/?(#.*)?$", 1000084, 145],
          ["http://m.(beta.)?mgtv.com/#/channel/(life|138)/?(#.*)?$", 1000084, 138],
          ["http://m.(beta.)?mgtv.com/#/channel/(idol|136|1030)/?(#.*)?$", 1000084, 136],
          ["http://m.(beta.)?mgtv.com/#/channel/(fun|135|1026)/?(#.*)?$", 1000084, 135],
          ["http://m.(beta.)?mgtv.com/#/channel/(174)/?(#.*)?$", 1000084, 174],
          ["http://m.(beta.)?mgtv.com/#/channel/(129|1031)/?(#.*)?$", 1000084, 129],
          ["http://m.(beta.)?mgtv.com/#/channel/(doc|137)/?(#.*)?$", 1000084, 137],
          ["http://m.(beta.)?mgtv.com/#/channel/(edu|140)/?(#.*)?$", 1000084, 140],
          ["http://m.(beta.)?mgtv.com/#/channel/(game|139)/?(#.*)?$", 1000084, 139],
          ["http://m.(beta.)?mgtv.com/#/channel/(live)/?(#.*)?$", 1000110, 1000111],
          ["http://m.(beta.)?mgtv.com/#/channel/.*"],
          ["http://m.(beta.)?mgtv.com/#/(subchannel|listchannel)/.*"]],
    "3": [["http://m.(beta.)?mgtv.com/#/play/.*", 1000100, 1000169],
          ["http://m.(beta.)?mgtv.com/#/s/.*", 1000100, 1000104],
          ["http://m.(beta.)?mgtv.com/#/l/.*", 1000100, 1000103],
          ["http://m.(beta.)?mgtv.com/#/b/.*", 1000100, 1000102]],
    "4": [["http://m.(beta.)?mgtv.com/#/search.*", 1000108, 1000109],
          ["http://m.(beta.)?mgtv.com/#/so/?(#.*)?$", 1000108, 1000109]],
    "5": [["http://m.(beta.)?mgtv.com/#/result/.*$", 1000108, 1000159]],
    "6": [["http://m.(beta.)?mgtv.com/#/sort/.*$", 1000112, 1000113]],
    "7": [["http://m.(beta.)?mgtv.com/#/topic/.*$"]],
    "8": [["http://m.(beta.)?mgtv.com/#/(list|h)/.*$"]],
    "9": [["http://m.(beta.)?mgtv.com/#/history.*$", 1000106, 1000107],
          ["http://m.(beta.)?mgtv.com/#/login(/.*)?(#.*)?$"],
          ["http://m.(beta.)?mgtv.com/#/reg(/.*)?(#.*)?$"],
          ["http://m.(beta.)?mgtv.com/#/protocol(/.*)?(#.*)?$"],
          ["http://m.(beta.)?mgtv.com/#/i(/.*)?(#.*)?$"]],
    "10": [["http://m.(beta.)?mgtv.com/#/thirdparty/.*$"]],
    "11": [["http://m.(beta.)?mgtv.com/#/livelanding/.*$"]]
}

msite_pron_type = {
    "1000100": "pt_sub"
}

msite_pt_id_map = {
    "1": "1000102",
    "2": "1000103",
    "3": "1000104",
    "4": "1000101"
}

dict_msite_page_re_type = {}
for (key, value) in dict_msite_page_type.items():
        dict_msite_page_re_type[key] = {}
        for regex in value:
            pattern = re.compile(regex[0])
            dict_msite_page_re_type[key][regex[0]] = pattern
