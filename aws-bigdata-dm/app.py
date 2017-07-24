#encoding: utf-8
# @Author: jeffrey
# @Date:   2016-05-17T18:45:24+08:00
# @Last modified by:   jeffrey
# @Last modified time: 2016-05-18T10:06:26+08:00
import os
import sys
from commonlib.pydotalog import pydotalog
from commonlib.global_var import global_var_client

log_dir=os.path.join(os.path.dirname(__file__),"./log/")
pydotalog.init_logger(log_dir+"/dm.log")
pydotalog.info("start dm wash")

from scheduling import scheduling


def process():
    '''
    :清洗数据
    '''

    # 开始时间填入全局,用于后续流程
    global_var_client.set_global_process_time(start_time)

    process_handler = scheduling(topicname, dm_name, start_time)

    for line in sys.stdin:        
        process_handler.proccess_line(line)


if __name__ == '__main__':
    if len(sys.argv) ==4:
        (di,topicname,dm_name,start_time)=sys.argv
        pydotalog.info("input parameter topicname:%s" % topicname)
        pydotalog.info("input parameter dm_name:%s" % dm_name)
        pydotalog.info("input parameter start_time:%s" % start_time)
        process()
    else:
        pydotalog.error("args is error")
