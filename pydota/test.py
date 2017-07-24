#!/usr/bin/env python
# encoding: utf-8

import os
import sys
if 'pydota' not in sys.modules and __name__ == '__main__':
    import pythonpathsetter

from pydota.format.format_base import FormatBase

if __name__ == '__main__':
    client = FormatBase("201512021000")
    a = client.formatLocation("123.150.107.0")
    for tmp in a:
        print tmp