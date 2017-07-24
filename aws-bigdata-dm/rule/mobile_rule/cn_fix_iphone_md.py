# encoding: utf-8
# @Author: gibbs
# @Date:   2016-05-17T18:46:24+08:00
# @Last modified by:   gibbs
# @Last modified time: 2016-05-17T19:29:22+08:00

import urllib

from rule.rule import rule
from rule.dict_page.dict_iphone_model import dict_iphone_model_name, dict_ipad_model_name, dict_ipod_model_name


class CnFixIPhoneMod(rule):
    """
    :换算规则
    """

    def __init__(self):
        super(CnFixIPhoneMod, self).__init__()

    def convert(self, field):
        """
        :param field:  input field data(mod|client)
        :return: vid
        """

        if len(field) < 2:
            return [1, "input_error"]

        if str(field[1]).lower() == "iphone":
            mod = urllib.unquote(str(field[0])).replace(',', '_').lower()
            mod = mod.replace('-', '_')
            if "iphone" in mod:
                mod_tmp = dict_iphone_model_name.get(mod, '')
            elif "ipad" in mod:
                mod_tmp = dict_ipad_model_name.get(mod, '')
            else:
                mod_tmp = dict_ipod_model_name.get(mod, '')

            if mod_tmp != "":
                return [0, mod_tmp]
            else:
                return [0, mod.replace('_', ' ')]

        else:
            return [0, str(field[0]).lower()]


