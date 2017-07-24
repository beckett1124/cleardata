# encoding: utf-8

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
import urllib
from user_agents import parse
from commonlib.mgtv_utils import get_web_cxid

if __name__ == '__main__':
    # for line in sys.stdin:
    #     # (ch, ref, client_type) = line.strip().split(",")
    #     # print get_web_cxid(ch, ref, client_type)
    #     test_line = json.loads(line.strip())
    #     print test_line
    #     resul = test_line['mf'].replace('\x00', '')
    #     print resul + "," + "aa"
    #     print len(resul)
    #     # print len(resul)
    # # str_tmp = "Dalvik/2.1.0 (Linux; U; Android 5.1; ￣ﾀﾀ￣ﾀﾀ Build/LMY47D)"
    # # print parse(str_tmp).device.brand
    regex = "^([\d\.]+).*"
    pattern = re.compile(regex)
    tmp_str = "V4.1.5+dd"
    match = pattern.match(tmp_str)
    if match:
        os_str = match.groups()[0]
    else:
        os_str = "wrong"

    print os_str

