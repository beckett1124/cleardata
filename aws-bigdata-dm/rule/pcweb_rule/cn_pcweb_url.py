#encoding: utf-8

import re
from rule.rule import rule


class cn_pcweb_url(rule):
    '''
    :根据URL获取PC WEB类型
    '''

    def __init__(self):
        self.imgoConditionNoEnd_WWW = re.compile("^(http|https)://www.imgo.tv/$")
        self.mgtvConditionNoEnd_WWW = re.compile("^(http|https)://www.(mgtv|hunantv).com/$")
        self.imgoConditionEnd_WWW = re.compile("^(http|https)://www.imgo.tv$")
        self.mgtvConditionEnd_WWW = re.compile("^(http|https)://www.(mgtv|hunantv).com$")
        self.mgtvImgoConditionSlash = re.compile("^(http|https)://(mgtv.com|hunantv.com|imgo.tv)/$")
        self.mgtvImgoConditionNoSlash = re.compile("^(http|https)://(mgtv.com|hunantv.com|imgo.tv)$")

    def endWithSpecial(self, url):
        error_char_List = ["#", "$" ,"\\"]

        lenth = len(str(url))
        for i in range(0, url.__len__())[::-1]:
            if url[i] not in error_char_List:
                lenth = i + 1
                break

        return url[0:lenth]

    def geturl(self, fields):
        url_tmp = str(fields[0])


        if self.mgtvConditionNoEnd_WWW.match(url_tmp) \
                or self.imgoConditionNoEnd_WWW.match(url_tmp) \
                or self.mgtvConditionEnd_WWW.match(url_tmp) \
                or self.imgoConditionEnd_WWW.match(url_tmp) \
                or self.mgtvImgoConditionSlash.match(url_tmp) \
                or self.mgtvImgoConditionNoSlash.match(url_tmp):
            return [0, "/"]

        urlSign = "://";
        slash = "/"
        url_tmp = str(url_tmp).replace(urlSign, "")
        siteRange_index = url_tmp.find(slash)
        # 分割符出现在最后
        if siteRange_index == -1 or siteRange_index == len(url_tmp) - 1 :
            return [0, ""]
        else:
            return [0, url_tmp[siteRange_index:]]

    def convert(self, fields):
        '''
        :空值校验
        '''
        if len(fields) != 1:
            return [1, "input_error"]
        else:
            url_str = fields[0]

            if url_str is None or url_str == "" or url_str == "-":
                return [0, ""]

            url_str = url_str.replace(',', '').replace('\\', '').replace('\x00', '')[0:2046]
            url_str = self.endWithSpecial(url_str)
            url_str = url_str.replace("\\", "")
            url_str = url_str.replace(" ", "")
            url_str = url_str.replace("\t", "")

            return self.geturl([url_str])


