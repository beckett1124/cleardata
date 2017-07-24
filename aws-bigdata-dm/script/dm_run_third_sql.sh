############################################################################
##
## Copyright (c) 2013 hunantv.com, Inc. All Rights Reserved
## $Id: py_dota_get_recv_new.sh,v 0.0 <T_CREATE_DATE>  dongjie Exp $
##
############################################################################
#
###
# # @file   py_dota_get_recv_new.sh
# # @author dongjie<dongjie@e.hunantv.com>
# # @date   <T_CREATE_DATE>
# # @brief
# #
# ##
#!/bin/bash

des_root_path="$HOME/data/des"
md5_root_path="$HOME/data/md5_check"


dowload_file_num=0
s3_file_num=0

function show_help(){
    echo "  options:"
    echo "    -h, --help                        Show this help."
    echo "    -t, --topic list                  需要获取原始日志的topic列表,topic之间用逗号分割 (eg. pcweb_play_time,iphone_play_time)."
    echo "    -m, --dm fact                     写入事实表名称(playtime_fact)."
    echo "    -d, --delay_hour                  当前时间延迟时间,start_hour有值时,失效."
    echo "    -s, --start time                  获取这个小时的原始日志(eg.2016011301)."
    echo "    -e, --end time                    获取这个小时的原始日志(eg.2016011301)."
}


send_error_mess(){
    mess=$1
    localhost=`LC_ALL=C /sbin/ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'`
    error_mess="所在机器:"${localhost}"  "${mess}
    #echo $error_mess
    curl -X POST --data-urlencode "payload={\"text\":\"${error_mess}\"}" https://hook.bearychat.com/=bw7by/incoming/71a4dcf2093e6b443a8b8f33d48fdac8
}

function get_time(){
    day=$1
    echo "${day:0:4}-${day:4:2}-${day:6:2}"
    if [[ $? -eq 0 ]];then
        return 0
    else
        echo "get time error:"${day}
        exit
    fi
}

function check_des_file(){
    file_check=$1

    if [ ! -f "${file_check}" ]; then
        send_error_mess "文件不存在/生成失败:${file_check}"
        flag=1
        exit 1
    fi

    if [ ! -s "${file_check}" ];then
        send_error_mess "生成了空文件:${file_check}"
        flag=1
        exit 1
    fi
}

function get_des_from_mysql(){

    start_time=`get_time ${start_day}`
    end_time=`date -d "-1 day ago ${start_time}" +%Y-%m-%d`


    for topic_name in ${topic_list[@]}
    do
        local_file_path="${des_root_path}/${topic_name}/${start_day:0:4}/${start_day:4:2}/${start_day:6:2}"

        mkdir -p ${local_file_path} 2>/dev/null
        rm ${local_file_path}/*

        # 获取sql
        if [[ ${topic_name} == "boss_order_success" ]];then
            err_msg=`mysql -h10.27.106.230 -uMDS -P3306 -pflUsh232 boss --execute "select t.*,ac.passport,ch.open_type from (select o.paid_at,o.id,o.uuid,o.channel_id,o.business_id,o.platform_id,o.status,o.amount,o.account_id,o.relation_order_id,o.version,o.mac,o.uip,o.voucher_id,o.voucher_amount,o.cxid from boss.order o where o.status = 1 and o.paid_at >= '${start_time}' and o.paid_at < '${end_time}') t, boss.account as ac, boss.channel as ch where t.account_id = ac.id and t.channel_id = ch.id" \
            > ${local_file_path}/${start_day}_${topic_name}.csv`
            err_num=$?
        else
            send_error_mess "[${start_day}] 非法的topic: ${topic_name}"
            exit 1
        fi

        if [[ ${err_num} -ne 0 ]];then
            send_error_mess "[${start_day}] ${topic_name} 导出数据失败. err_msg:[${err_msg}]"
            exit 1
        fi

        check_des_file ${local_file_path}/${start_day}_${topic_name}.csv

        md5_path=${md5_root_path}/${start_day:0:4}/${start_day:4:2}
        mkdir -p ${md5_path} 2>/dev/null
        touch ${md5_path}/${topic_name}_${start_day}.done
    done


}

while [[ $# -gt 0 ]]; do
    opt="$1"
    shift

    case "$opt" in
    -h|\?|--help)
        show_help
        exit 0
        ;;
    -t|--topic_list)
        topic_list="$1"
        shift
	    ;;
    -s|--start_day)
        start_day="$1"
        shift
        ;;
    -m|--dm_fact)
        dm_fact="$1"
        shift
        ;;
    *)
        echo "option $opt"
        show_help
        exit 0
        ;;
    esac
done


if [[ ${dm_fact} == "" ]]; then
    echo "请输入事实表名称 -m"
    show_help
    exit
fi

if [[ ${topic_list} == "" ]]; then
    echo "请输入topic列表 -t"
    exit
else
    OLD_IFS="$IFS"
    IFS=","
    arr=(${topic_list})
    IFS="$OLD_IFS"
    topic_list=(${arr[@]})
fi

if [[ ${start_day} == "" ]]; then
    start_day=`date --date="$DATE - 1 day" +%Y%m%d`
fi

run_dm_topics=(${topic_list[*]})
echo "topic_list:"${topic_list[*]}  "dm_fact:"${dm_fact} "scp开始日志时间:"${start_day}

# 从mysql 导出数据
get_des_from_mysql

for topic in ${run_dm_topics[@]}; do
    cd $HOME/aws-bigdata-dm/script
    sh dm_process_third_sql.sh -t ${topic} -p pv -m ${dm_fact} -s ${start_day} &
done
