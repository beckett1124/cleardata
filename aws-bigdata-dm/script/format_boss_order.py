# encoding: utf-8

import time
import sys


class FormatBossOrder(object):
    """
    :格式化订单 order表输出
    """

    def __init__(self):
        self.version_client_map = {
            "mobile-android": ["aphone", "imgotv-aphone-"],
            "mobile-ios": ["iphone", "imgotv-iphone-"],
            "ott": ["ott"],
            "pad-ios": ["ipad", "imgotv-ipad-"],
            "pcclient-macosx": ["macclient"],
            "pcclient-windows": ["pcclient"],
            "pcweb": ["pcweb"]
        }

    def process_line(self, line):

        line_list = str(line).strip().split('\t')
        len_list = len(line_list)
        result_list = []

        if len_list == 0:
            return

        for index in range(0, len_list):
            if str(line_list[index]) == "NULL":
                line_list[index] = ""
            if index == 0:
                try:
                    time_data = time.strptime(line_list[index], '%Y-%m-%d %H:%M:%S')
                    time_str = time.strftime('%Y%m%d%H%M%S', time_data)
                except ValueError:
                    return
                result_list.append(time_str[0:8])
                result_list.append(time_str[8:12])
            elif index == 10:
                version_list = line_list[index].split(',')
                client_str = str(version_list[0]).lower().strip()
                ver_prefix = ""

                if client_str in self.version_client_map:
                    tmp_list = self.version_client_map[client_str]

                    client_str = tmp_list[0]

                    if len(tmp_list) > 1:
                        ver_prefix = tmp_list[1]

                if len(version_list) > 1:
                    version_str = ver_prefix + str(version_list[1]).strip()
                else:
                    version_str = ''

                result_list.append(client_str)
                result_list.append(version_str)

            else:
                # 数据逗号替换
                result_list.append(line_list[index].replace(',', '^'))

        print ','.join(result_list)


if __name__ == "__main__":
    boss_order_client = FormatBossOrder()

    for line_str in sys.stdin:
        boss_order_client.process_line(line_str)