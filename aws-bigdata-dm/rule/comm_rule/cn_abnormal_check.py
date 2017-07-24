#encoding: utf-8
# @Author: gibbs
# @Date:   2016-12-01T11:00:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-12-01T11:02:17+08:00

from rule.rule import rule
from rule.comm_rule.cn_bid import cn_bid
from data_class.cn_check_abnormal_log import cn_check_abnormal_log_client


class cn_abnormal_check(rule):
    """
    :根据异常流量检测
    """

    def __init__(self):
        pass

    def abnormal_check(self, fields):
        ip_field = [fields[4]]
        did_field = [fields[0]]
        _bid_res = cn_bid().convert([fields[1]])
        if _bid_res[0] != 0:
            return _bid_res
        did_field.append(str(_bid_res[1]))
        did_field.append(str(fields[2])+str(fields[3]))

        ip_field.append(str(_bid_res[1]))
        ip_field.append(str(fields[2])+str(fields[3]))

        _res = cn_check_abnormal_log_client.check_did_frequency(did_field)

        if _res[0] != 0:
            return _res
        elif str(_res[1]) != "0":
            return _res

        _res = cn_check_abnormal_log_client.check_did_city(did_field)

        if _res[0] != 0:
            return _res
        elif str(_res[1]) != "0":
            return _res

        _res = cn_check_abnormal_log_client.check_internal_ip([ip_field[0]])

        if _res[0] != 0:
            return _res
        elif str(_res[1]) != "0":
            return _res

        _res = cn_check_abnormal_log_client.check_ip_frequency(ip_field)

        if _res[0] != 0:
            return _res
        elif str(_res[1]) != "0":
            return _res

        return [0, "0"]

    def convert(self, fields):
        """
        :异常流量检测
        :param fields: [did, client, log_time_ymd, log_time_hms, ip]
        :return:
        """
        if len(fields) != 5:
            return [1, "input_error"]
        else:
            for field in fields:
                if field == "" or field == "-":
                    return [1, "input_error_url"]

            return self.abnormal_check(fields)
