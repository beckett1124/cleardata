# encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-19T12:15:07+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-19T12:23:07+08:00

import re

# 19表示规则不能匹配的站内地址, 20表示站外其他
dist_pcweb_page_type = {
    "0": [["http://(www.)?(mgtv|hunantv|imgo).(com|tv)/?(#.*)?$", 1000001, 5], ["http://www.mgtv.com/beta/?(#.*)?$", 1000001, 5]],
    "1": [["http://www.mgtv.com/(beta/)?show/?(#.*)?$", 1000001, 6],
          ["http://www.mgtv.com/(beta/)?tv/?(#.*)?$", 1000001, 4],
          ["http://www.mgtv.com/(beta/)?movie/?(#.*)?$", 1000001, 9],
          ["http://www.mgtv.com/(beta/)?cartoon/?(#.*)?$", 1000001, 8],
          ["http://www.mgtv.com/(beta/)?child/?(#.*)?$", 1000001, 10],
          ["http://www.mgtv.com/(beta/)?news/?(#.*)?$", 1000001, 51],
          ["http://www.mgtv.com/(beta/)?music/?(#.*)?$", 1000001, 12],
          ["http://www.mgtv.com/(beta/)?live/?(#.*)?$", 1000034, 1000035],
          ["http://www.mgtv.com/(beta/)?girl/?(#.*)?$"],
          ["http://www.mgtv.com/(beta/)?ori/?(#.*)?$", 1000001, 113],
          ["http://www.mgtv.com/(beta/)?life/?(#.*)?$", 1000001, 110],
          ["http://www.mgtv.com/(beta/)?doc/?(#.*)?$", 1000001, 111],
          ["http://www.mgtv.com/(beta/)?edu/?(#.*)?$", 1000001, 109],
          ["http://www.mgtv.com/(beta/)?game/?(#.*)?$", 1000001, 112],
          ["http://live.mgtv.com/?(#.*)?$", 1000034, 1000161],
          ["http://www.mgtv.com/d/\d+.html(#\w+=\d+)?(#.*)?$"],
          ["http://tv.hunantv.com/live/?(#.*)?$", 1000034, 1000035]],
    "2": [["http://www.mgtv.com/v/\d+/(\d+)(/index.html|/)?(#.*)?$"],
          ["http://www.mgtv.com/h/(\d+).html(#\w+=\d+)?(#.*)?$"]],
    "3": [["http://www.mgtv.com/v/\d+/\d+/f/(\d+).html(#.*)?$", 1000015, 1000168],
          ["http://www.mgtv.com/v/\d+/\d+/c/(\d+).html(#.*)?$", 1000015, 1000168],
          ["http://www.mgtv.com/s/(\d+).html(#\w+=\d+)?(#.*)?$", 1000015, 1000019],
          ["http://www.mgtv.com/l/(\d+).html(#\w+=\d+)?(#.*)?$", 1000015, 1000018],
          ["http://www.mgtv.com/l/\d+/(\d+).html(#\w+=\d+)?(#.*)?$", 1000015, 1000018],
          ["http://www.mgtv.com/b/\d+/(\d+).html(#\w+=\d+)?(#.*)?$", 1000015, 1000017],
          ["http://www.mgtv.com/r/\w+.html(#\w+=\d+)?(#.*)?$", 1000015, 1000016],
          ["http://www.mgtv.com/r/\w+/\w+.html(#\w+=\d+)?(#.*)?$", 1000015, 1000016],
          ["http://www.mgtv.com/b/(\d+)/?(#.*)?$", 1000015, 1000017]],
    "4": [["http://www.mgtv.com/(z|liveshow)/\d+.html(#.*)?$"],
          ["http://show.mgtv.com/live.html?dynamicId=\w+&e_type=e_userLive(#.*)?"],
          ["http://www.mgtv.com/rz/.*html(#.*)?"],
          ["http://www.mgtv.com/live/pay/?(#.*)?$"],
          ["http://www.mgtv.com/live/pay/list.html.*(#.*)?$"],
          ["http://www.mgtv.com/live/pay/.*(#.*)?$"],
          ["http://www.mgtv.com/z/\d+/\d+.html(#.*)?$"]],
    "5": [["http://so.mgtv.com/.*(#.*)?$", 1000032, 1000033]],
    "6": [["http://list.mgtv.com/\d+/.*html(#.*)?$", 1000038, 1000039]],
    "7": [["http://i.mgtv.com/my/(record|watch)/?(#.*)?$", 1000020, 1000021],
          ["http://i.mgtv.com/my/sub/?(#.*)?$", 1000020, 1000022],
          ["http://i.mgtv.com/sub/?(#.*)?$", 1000020, 1000022],
          ["http://i.mgtv.com/my/card/?(#.*)?$", 1000020, 1000166],
          ["http://i.mgtv.com/my/order/?(#.*)?$", 1000020, 1000167],
          ["http://i.mgtv.com/?(#.*)?$", 1000020, 1000023],
          ["http://i.mgtv.com/account/login/?(#.*)?$", 1000020, 1000023],
          ["http://i.mgtv.com/my/message(/.*)?(#.*)?$", 1000020, 1000024],
          ["http://i.mgtv.com/my/fav/?(#.*)?$", 1000020, 1000025],
          ["http://i.mgtv.com/my/(setting|avatar|password|thirdparty)/?(#.*)?$", 1000020, 1000026],
          ["http://i.mgtv.com/my/pay/?(#.*)?$", 1000020, 1000028],
          ["http://i.mgtv.com/vip/exchange/page/?(#.*)?$", 1000020, 1000027],
          ["http://i.mgtv.com/account/emaillink/?(#.*)?$", 1000020, 1000029],
          ["http://www.mgtv.com/bdsfm/login(/.*)?(#.*)?$", 1000020, 1000171],
          ["http://www.mgtv.com/bdsfm/playlist(/.*)?(#.*)?$", 1000020, 1000172],
          ["http://www.mgtv.com/bdsfm/message(/.*)?(#.*)?$", 1000020, 1000173],
          ["http://i.mgtv.com/(?!feedback.html).*(#.*)?$"]],
    "9": [["http://www.mgtv.com/(beta/)?vip(/pianku)?/?(#.*)?$", 1000030, 1000031],
          ["http://order.mgtv.com/pay/pc/(index|supervip).html(#.*)?$", 1000030, 1000031]],
    "11": [["http://www.mgtv.com/app/?\S+(#.*)?$"]],
    "12": [["http://i.mgtv.com/feedback.html(#.*)?$"]],
    "13": [["http://www.mgtv.com/t/\d+-\d+.html(#.*)?$"]],
    "14": [["http://www.mgtv.com/v/2\d{3}/idol/?.*(#.*)?$", 1000001, 11], ["http://www.mgtv.com/v/2\d{3}/\w+/?.*(#.*)?$"]],
    "16": [["http://www.mgtv.com/top/.*$", 1000036, 1000037], ["http://www.mgtv.com/top(#.*)?$", 1000036, 1000037]],
    "17": [["http://www.mgtv.com/topic/\w+.html(#.*)?$"]],
    "18": [["http://v.mgtv.com/p/\d+.html(#.*)?$"]],
    "21": [["http://www.mgtv.com/hz/.*$"]],
    "22": [["http://www.mgtv.com/404.html"]]
}

pcweb_pron_type = {
    "1000015": "pt_sub"
}

pcweb_pt_id_map = {
    "1": "1000017",
    "2": "1000018",
    "3": "1000019",
    "4": "1000016"
}

dict_pcweb_page_re_type = {}
for (key, value) in dist_pcweb_page_type.items():
        dict_pcweb_page_re_type[key] = {}
        for regex in value:
            pattern = re.compile(regex[0])
            dict_pcweb_page_re_type[key][regex[0]] = pattern
