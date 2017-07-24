# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-18T18:59:26+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T19:54:25+08:00
from rule.rule import rule
import urllib
import re

class  cn_mobile_url_site(rule):
    '''
    :url 去掉?后缀
    '''


    def __init__(self):
        pass

    def endWithSpecial(self, url):
        error_char_List = ["#", "$" ,"\\"]

        if url is None or url == "" or url == "-":
            return [1, "input_error"]

        lenth = len(str(url))
        for i in range(0, url.__len__())[::-1]:
            if url[i] not in error_char_List:
                lenth = i + 1
                break

        return [0, url[0:lenth]]

    def gethost(self, fields):
        if fields[0] is None or fields[0] == "" or fields[0] == "-":
            return [0, "direct"]

        url_tmp = str(fields[0])
        try:
            url_tmp = urllib.unquote(fields[0]).decode('utf8')
        except UnicodeDecodeError:
            try:
                url_tmp = urllib.unquote(fields[0]).decode('gbk')
            except UnicodeDecodeError:
                return [1, "URL_DECODE_ERR"]

        url_tmp = url_tmp.replace(',', '').replace('\\', '').replace('\x00', '')[0:2046]
        url_tmp = url_tmp.replace("\\", "")
        url_tmp = url_tmp.replace(" ", "")
        url_tmp = url_tmp.replace("\t", "")

        fileCondition = "^imgotv:";
        pattern_zn = re.compile(fileCondition)
        match_zn = pattern_zn.match(url_tmp)
        if match_zn:
            host = "direct"
            return [0, "direct"]

        imgoConditionNoEnd_WWW = "^(http|https)://www.imgo.tv/$";
        mgtvConditionNoEnd_WWW = "^(http|https)://www.(mgtv|hunantv).com/$";
        imgoConditionEnd_WWW = "^(http|https)://www.imgo.tv$";
        mgtvConditionEnd_WWW = "^(http|https)://www.(mgtv|hunantv).com$";
        mgtvImgoConditionSlash = "^(http|https)://(mgtv.com|hunantv.com|imgo.tv)/$";
        mgtvImgoConditionNoSlash = "^(http|https)://(mgtv.com|hunantv.com|imgo.tv)$";
        MGTV = "mgtv.com";
        urlSign = "://";
        slash = "/"

        if re.match(imgoConditionNoEnd_WWW, url_tmp) \
                or re.match(mgtvConditionNoEnd_WWW, url_tmp) \
                or re.match(mgtvConditionEnd_WWW, url_tmp) \
                or re.match(imgoConditionEnd_WWW, url_tmp) \
                or re.match(mgtvImgoConditionSlash, url_tmp) \
                or re.match(mgtvImgoConditionNoSlash, url_tmp):
            siteName = MGTV;
            return [0, siteName]
        else:
            urlSign_index = url_tmp.find(urlSign)
            if urlSign_index == -1:
                urlSign_index = 0
            elif urlSign_index > 0:
                urlSign_index += 3
            siteRange_index = url_tmp.find(slash, urlSign_index)
            if siteRange_index == -1:
                siteRange_index = len(url_tmp)
            siteName = url_tmp[urlSign_index:siteRange_index]

            if siteName == "hunantv.com" or siteName == "imgo.tv":
                siteName = MGTV;

            return [0, siteName[0:63]]
            # re.match("^(http|https)://www.imgo.tv/$", )

    def convert(self, fields):
        '''
        :空值校验
        '''
        if len(fields) != 1:
            return [1, "input_error"]
        else:
            #url_str = url_str.replace(',', '').replace('\\', '').replace('\x00', '')[0:2046]
            return  self.gethost(fields)

