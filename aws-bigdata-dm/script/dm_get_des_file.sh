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

source ./dm_script.conf

des_root_path="$HOME/data/des"
md5_root_path="$HOME/data/md5_check"
md5_file_root_path="$HOME/data/file_md5_check"

wash_dm_topics=("msite_pv dau_ott dau_ott_41 dau_ott_44 dau_ott_340 dau_ott_3111 mpp_vv_ott ott_vv_41 ott_vv_311_20151012 mobile_offline_vv mpp_vv_mobile mpp_vv_mobile_new_version mpp_vv_mobile_211_20151012")

function show_help(){
    echo "  options:"
    echo "    -h, --help                        Show this help."
    echo "    -t, --topic list                  需要获取原始日志的topic列表,topic之间用逗号分割 (eg. mobile_pv,pcweb_pv)."
    echo "    -p, --platform                    (ott|mobile)."
    echo "    -m, --dm fact                     写入事实表名称(pv_fact|vv_fact)."
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


function md5_check(){
    logserver_md5_file=$1
    locacl_md5_file=$2
    err_md5_check=$3
    cat ${logserver_md5_file} ${locacl_md5_file} | awk '{print $1}' | sort | uniq -c | awk '{if($1!=2) print $0}' > ${err_md5_check}
    failed_num=`wc -l ${err_md5_check}|awk '{print $1}'`

    if [[ ${failed_num} -ge 1 ]];then
        cat ${logserver_md5_file} ${locacl_md5_file} | sort | uniq -c | awk '{if($1!=2) print $0}' > ${err_md5_check}
        failed_num=`wc -l ${err_md5_check}|awk '{print $1}'`
    fi
    return ${failed_num}
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

get_des_by_topic(){
    topic_name=$1
    start_hour=$2
    scp_ip=$3

    sub_year=${start_hour:0:4}
    sub_month=${start_hour:4:2}
    sub_day=${start_hour:6:2}
    sub_hour=${start_hour:8:2}

    md5_file_path=${md5_file_root_path}/${sub_year}/${sub_month}/
    md5_path=${md5_root_path}/${sub_year}/${sub_month}/
    mkdir -p ${md5_file_path} 2>/dev/null
    mkdir -p ${md5_path} 2>/dev/null

    scp_path=${des_root_path}/${sub_year}/${sub_month}/
    mkdir -p ${scp_path} 2>/dev/null

    scp_file_name="${start_hour}00*rawdata_${topic_name}_20*"

    if [[ ${scp_file_name} == "" ]];then
        echo "scp_file_name is null ,please check conf file"
        return 1
    fi

    scp_file_path=${scp_path}/${scp_file_name}

    #原始日志存储端文件md5值
    scp_md5_file=${md5_file_path}${start_hour}_${topic_name}"_logserver_md5"
    #原始日志本地存储文件md5值
    local_md5_file=${md5_file_path}/${start_hour}_${topic_name}"_local_md5"
    err_md5_file=${md5_file_path}/"err_"${start_hour}_${topic_name}"_md5_check"

    # 删除本地des文件
    rm ${scp_path}/${scp_file_name} 2>/dev/null

    echo "scp的ip:"${scp_ip}

    #验证路径是否存在
    ls_error_mess=`ssh "dota@${scp_ip}" "cd $scp_path&&ls $scp_file_name" 2>&1`
    dir_is_exit=$?

    if [[ ${dir_is_exit} -eq 0 ]];then
        scp_error_mess=`scp "dota@${scp_ip}:"${scp_file_path} ${scp_path}`
        scp_return_mess=$?
        if [[ ${scp_return_mess} -ne 0 ]];then
#            send_error_mess "$start_hour $scp_ip $topic_name scp失败 错误码:${scp_error_mess}"
            echo "$start_hour $scp_ip $topic_name scp失败 错误码:${scp_error_mess}"

            return 1
        fi
    elif [[ ${dir_is_exit} -eq 2 ]];then
        continue
    else
#        send_error_mess "$start_hour $scp_ip $topic_name scp路径不存在 错误码:${ls_error_mess}"
        echo "$start_hour $scp_ip $topic_name scp路径不存在 错误码:${ls_error_mess}"

        return 1
    fi

    rm ${scp_md5_file} 2>/dev/null

    ssh dota@${scp_ip} "cd ${scp_path} && md5sum ${scp_file_name}"  >> ${scp_md5_file}

    cd ${scp_path} && md5sum ${scp_file_name} > ${local_md5_file}
    md5_check ${scp_md5_file} ${local_md5_file} ${err_md5_file}
    md5_return=$?
    if [[ ${md5_return} -ge 1 ]];then
        md5_error=`cat ${err_md5_file}`
#        send_error_mess "$start_hour $scp_ip $topic_name md5校验失败 ${md5_error}"
        echo "$start_hour $scp_ip $topic_name md5校验失败 ${md5_error}"

    else
        # ott_vv_311 点播去掉5.0版本的点播日志
        if [[ ${topic_name} == "ott_vv_311_20151012" ]];then
            cd ${scp_path}
            scp_files=(`ls ${scp_file_name}`)
            for scp_file in ${scp_files[@]};do
                cat ${scp_file} |awk -F, '{if($23 !~ /^5\./)print }' > tmp_${scp_file}
                mv tmp_${scp_file} ${scp_file}
            done
        fi
        touch ${md5_path}"/.done_"${topic_name}_${start_hour}"00.md5"
    fi
}

get_time(){
    hour=$1
    echo `date -d "${hour:0:4}-${hour:4:2}-${hour:6:2} ${hour:8:2}:00:00" +%s`
    if [[ $? -eq 0 ]];then
        return 0
    else
        echo "get time error:"${hour}
        exit
    fi
}

get_des(){

    start_time=`get_time ${start_hour}`
    end_time=`get_time ${end_hour}`

    topics_tmp=`echo ${topic_list[*]}`

    while [[ ${start_time} -le ${end_time} ]]
    do
        start_time_tmp=`date -d @${start_time} "+%Y%m%d%H"`
        echo "scp time:"${start_time_tmp}

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
                scp_hosts_name=`get_val_by_name ${topic_name}"_scp_hosts"`
                scp_hosts=`get_val_by_name ${scp_hosts_name}`

                #判断md5 .done文件是否存在
                done_name=".done_${topic_name}_${start_hour}00.md5"
                ssh "dota@${scp_hosts}" "cd ${scp_md5_path} && ls $done_name"
                done_mess=$?
                if [ ${done_mess} -ne 0 ];then
                    echo "$start_hour scp_hosts $topic_name recv ${done_name}文件未生成 错误码:${done_mess}"
                    continue
                fi

                get_des_by_topic "${topic_name}" "${start_time_tmp}" "${scp_hosts}"

                xrsh_arritemidx "$topics_tmp" "${topic_name}"
                i=$?
                if [ ${i} -ge 0 ]; then
                    unset topic_list[${i}]
                fi
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
    -p|--platform)
        platform="$1"
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

if [[ ${platform} == "" ]]; then
    echo "请输入原始日志播放类型 -p"
    exit
fi

if [[ ${dm_fact} == "" ]]; then
    echo "请输入事实表名称 -m"
    show_help
    exit
fi
if [[ ${topic_list} == "" ]]; then
    echo "请输入topic列表 -t"
    exit
else
    if [[ ${topic_list} == "all" ]]; then
        case "$platform" in
            ott)
                topic_list=(${ott_topics})
                ;;
            mobile)
                topic_list=(${mobile_topics})
                ;;
            *)
                echo "illarg platform $platform"
                show_help
                exit
                ;;
        esac
    else
        OLD_IFS="$IFS"
        IFS=","
        arr=(${topic_list})
        IFS="$OLD_IFS"
        topic_list=(${arr[@]})
    fi
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
echo "topic_list:"${topic_list[*]}  "平台:"${platform} "scp开始日志时间:"${start_hour} "scp终止日志时间:"${end_hour}
get_des

for topic in ${run_dm_topics[@]}; do
    for dm_topic in ${wash_dm_topics[@]};do
        if [[ ${dm_topic} == ${topic} ]];then
            cd $HOME/aws-bigdata-dm/script

            sh dm_process_yg.sh -t ${topic} -p pv -m ${dm_fact} -s ${start_hour} &

            break
        fi
    done
done

# vim: set ts=2 sw=2: #

