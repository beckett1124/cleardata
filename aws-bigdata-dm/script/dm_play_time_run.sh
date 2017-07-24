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
s3_playtime_des_root_path="s3://dota-archive/dota/playtime"

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

#获取数组中给定元素的下标
#参数：1 数组; 2 元素
#返回：元素在数组中的下标，从 0 开始；-1 表示未找到
#例子：
#    获取数组 xrsh_array 中元素 i3 的下标
#    xrsh_array=(i1 i2 i3)
#    xrsh_tmp=`echo ${xrsh_array[*]}`
#    xrsh_arritemidx "$xrsh_tmp" "i3"
#    返回 2
#注意：数组作为参数使用时需要先转换
function xrsh_arritemidx()
{
  local _xrsh_tmp
  local _xrsh_cnt=0
  local _xrsh_array=`echo "$1"`
  for _xrsh_tmp in ${_xrsh_array[*]}; do
    if test "$2" = "$_xrsh_tmp"; then
      return ${_xrsh_cnt}
    fi
    _xrsh_cnt=$(( $_xrsh_cnt + 1 ))
  done
  return -1
}


get_val_by_name(){
    name=$1
    val=$(eval "echo \$${name}")
    echo ${val}
}

send_error_mess(){
    mess=$1
    localhost=`LC_ALL=C /sbin/ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'`
    error_mess="所在机器:"${localhost}"  "${mess}
    #echo $error_mess
    curl -X POST --data-urlencode "payload={\"text\":\"${error_mess}\"}" https://hook.bearychat.com/=bw7by/incoming/71a4dcf2093e6b443a8b8f33d48fdac8
}

function download_s3_raw_data() {
    des_topic=$1
    process_time=$2

    s3_des_path=${s3_playtime_des_root_path}/${des_topic}/${process_time:0:4}/${process_time:4:2}/${process_time:6:2}/${process_time:8:2}/
    local_file_path="${des_root_path}/${des_topic}/${process_time:0:4}/${process_time:4:2}/${process_time:6:2}/${process_time:8:2}"
    mkdir -p ${local_file_path} 2>/dev/null
    rm ${local_file_path}/*

    s3_des_files_num=`aws s3 ls "${s3_des_path}"|wc -l`

    echo "[${des_topic}][${process_time}]s3's file number:[${s3_des_files_num}]."

    s3_file_num=$(($s3_file_num+$s3_des_files_num))

    if [[ ${s3_des_files_num} -gt 0 ]];then
        msg=`aws s3 sync ${s3_des_path} ${local_file_path}  2>&1`
    fi
}

function get_time(){
    hour=$1
    echo `date -d "${hour:0:4}-${hour:4:2}-${hour:6:2} ${hour:8:2}:00:00" +%s`
    if [[ $? -eq 0 ]];then
        return 0
    else
        echo "get time error:"${hour}
        exit
    fi
}

function get_des(){

    start_time=`get_time ${start_hour}`
    end_time=`get_time ${end_hour}`

    topics_tmp=`echo ${topic_list[*]}`

    while [[ ${start_time} -le ${end_time} ]]
    do
        start_time_tmp=`date -d @${start_time} "+%Y%m%d%H"`
        echo "scp time:"${start_time_tmp}

        year_tmp=${start_time_tmp:0:4}
        month_tmp=${start_time_tmp:4:2}
        day_tmp=${start_time_tmp:6:2}
        hour_tmp=${start_time_tmp:8:2}

        while true
        do
            len=${#topic_list[@]}
            if [ ${len} -eq 0 ];then
                break
            fi

            scp_md5_path=${md5_root_path}/${start_hour:0:4}/${start_hour:4:2}/

            for topic_name in ${topic_list[@]}
            do
                echo "拷贝topic:"${topic_name}

                #判断s3上_SUCCESS文件是否存在
                done_name="${s3_playtime_des_root_path}/${topic_name}/${year_tmp}/${month_tmp}/${day_tmp}/${hour_tmp}/_SUCCESS"
                file_done=`aws s3 --region cn-north-1 ls "${done_name}"`;
                if [ "${file_done}" ];then
                    echo "${done_name} file exist"
                else
                    echo "${done_name} file not exist!!"
                    continue
                fi

                download_s3_raw_data "${topic_name}" "${start_time_tmp}"

                xrsh_arritemidx "$topics_tmp" "${topic_name}"
                i=$?
                if [ ${i} -ge 0 ]; then
                    unset topic_list[${i}]
                fi

                dowload_file_num=`ls ${local_file_path}/*|wc -l`

                if [[ ${dowload_file_num} -ne ${s3_file_num} ]];then
                    echo "[${topic_name}][${dm_fact}]sync s3 to local failed: [${start_time_tmp}]."
                    send_error_mess "[${topic_name}][${dm_fact}]sync s3 to local failed: [${start_time_tmp}]."
                else
                    md5_path=${md5_root_path}/${year_tmp}/${month_tmp}
                    mkdir -p ${md5_path} 2>/dev/null
                    touch ${md5_path}/${topic_name}_${start_time_tmp}.done
                fi

                dowload_file_num=0
                s3_file_num=0

            done

            if [ ${#topic_list[@]} -ne 0 ];then
                sleep 120
            fi

        done
        start_time=`expr ${start_time} + 3600`
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
    -s|--start_hour)
        start_hour="$1"
        shift
        ;;
    -e|--end_hour)
        end_hour="$1"
        shift
        ;;
    -m|--dm_fact)
        dm_fact="$1"
        shift
        ;;
    -d|--delay_hour)
        delay_hour="$1"
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

if [[ ${start_hour} == "" ]]; then
    if [[ ${delay_hour} == "" ]]; then
        start_hour=`date --date="$DATE - 1 hour" +%Y%m%d%H`
    else
        start_hour=`date --date="$DATE - $delay_hour hour" +%Y%m%d%H`
    fi
fi
if [[ ${end_hour} == "" ]]; then
    end_hour=${start_hour}
fi

run_dm_topics=(${topic_list[*]})
echo "topic_list:"${topic_list[*]}  "dm_fact:"${dm_fact} "scp开始日志时间:"${start_hour} "scp终止日志时间:"${end_hour}
get_des

for topic in ${run_dm_topics[@]}; do
    cd $HOME/aws-bigdata-dm/script
    sh dm_process_playtime_lplay.sh -t ${topic} -p pv -m ${dm_fact} -s ${start_hour} &
done

# vim: set ts=2 sw=2: #

