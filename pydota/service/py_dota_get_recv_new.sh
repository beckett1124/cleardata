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
if [[ -n "$HOME" && -e "$HOME/.pydota_recv" ]]; then
  . "$HOME/.pydota_recv"
else
  source ./etc/pydota_recv.conf
fi

function show_help(){
    echo "  options:"
    echo "    -h, --help                        Show this help."
    echo "    -t, --topic list                  需要获取原始日志的topic列表,topic之间用逗号分割 (eg. mobile_pv,pcweb_pv)."
    echo "    -p, --Video playback type         (play|pv|live|pvs|mglive|dau|mobile_vv|other_vv)."
    echo "    -d, --delay_hour                  当前时间延迟时间,start_hour有值时,失效."
    echo "    -s, --start time                  获取这个小时的原始日志(eg.2016011301)."
    echo "    -e, --end time                    获取这个小时的原始日志(eg.2016011301)."
    echo "    -c, --                            服务器所属的状态(server/client)."
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

get_recv_by_topic(){
    topic_name=$1
    start_hour=$2
    scp_hosts_list=$3
    recv_hosts_list=$4
    location=$5

    sub_year=${start_hour:0:4}
    sub_month=${start_hour:4:2}
    sub_day=${start_hour:6:2}
    sub_hour=${start_hour:8:2}

    recv_localhost_path=${recv_root_path}/${sub_year}/${sub_month}/${topic_name}
    md5_path=${md5_root_path}/${sub_year}/${sub_month}/${topic_name}/
    mkdir -p ${md5_path} 2>/dev/null
    mkdir -p ${recv_localhost_path} 2>/dev/null

    recv_server_path=`get_val_by_name ${topic_name}"_path"`
    if [[ ${location} == "client" ]];then
        scp_path=${recv_localhost_path}
        log_ip_list=${scp_hosts_list}
    elif [[ ${location} == "server" ]];then
        scp_path=${recv_server_path}
        log_ip_list=${recv_hosts_list}
    else
        echo "请输入当前服务器作用(client/server) -c"
        exit
    fi
    #scp文件路径
    file_prefix=`get_val_by_name ${topic_name}"_file_name"`
    scp_file_name=`${file_prefix} ${sub_year} ${sub_month} ${sub_day} ${sub_hour}`

    if [[ ${scp_file_name} == "" ]];then
        echo "scp_file_name is null ,please check conf file"
        return 1
    fi

    scp_file_path=${scp_path}/${scp_file_name}

    #原始日志存储端文件md5值
    scp_md5_file=${md5_path}${start_hour}"_logserver_md5"
    #原始日志本地存储文件md5值
    local_md5_file=${md5_path}/${start_hour}"_local_md5"
    err_md5_file=${md5_path}/"err_"${start_hour}"_md5_check"
    rm ${recv_localhost_path}/${scp_file_name} 2>/dev/null

    for scp_ip in ${log_ip_list};do
        echo "scp的ip:"${scp_ip}
        #判断.done文件是否存在
        if [[ ${location} == "client" ]];then
            done_name=".done_${start_hour}_${topic_name}"
            ssh "dota@${scp_ip}" "cd $scp_path&&ls $done_name"
            done_mess=$?
            if [ ${done_mess} -ne 0 ];then
                send_error_mess "$start_hour $scp_ip $topic_name recv ${done_name}文件未生成 错误码:${done_mess}"
                return 1
            fi
        fi
        #验证路径是否存在
        ls_error_mess=`ssh "dota@${scp_ip}" "cd $scp_path&&ls $scp_file_name" 2>&1`
        dir_is_exit=$?

        if [[ ${dir_is_exit} -eq 0 ]];then
            scp_error_mess=`scp "dota@${scp_ip}:"${scp_file_path} ${recv_localhost_path}`
            scp_return_mess=$?
            if [[ ${scp_return_mess} -ne 0 ]];then
                send_error_mess "$start_hour $scp_ip $topic_name scp失败 错误码:${scp_error_mess}"
                return 1
            fi
            if [[ ${location} == "server" ]];then
                files=`ls ${recv_localhost_path}/${scp_file_name} | grep 'log$\|COMPLETED$\|log.ok$'`
                for file_tmp in ${files};do
                    mv ${file_tmp} ${file_tmp}_${scp_ip}
                done
            fi
        elif [[ ${dir_is_exit} -eq 2 ]];then
            continue
        else
            send_error_mess "$start_hour $scp_ip $topic_name scp路径不存在 错误码:${ls_error_mess}"
            return 1
        fi
    done

    rm ${scp_md5_file} 2>/dev/null
    for recv_ip in ${recv_hosts_list};do
        ssh dota@${recv_ip} "cd ${recv_server_path}&&md5sum ${scp_file_name}" | awk -v ip=${recv_ip} '{print $0"_"ip}' >> ${scp_md5_file}
    done
    cd ${recv_localhost_path}&&md5sum ${scp_file_name} > ${local_md5_file}
    md5_check ${scp_md5_file} ${local_md5_file} ${err_md5_file}
    md5_return=$?
    if [[ ${md5_return} -ge 1 ]];then
        md5_error=`cat ${err_md5_file}`
        send_error_mess "$start_hour $scp_ip $topic_name md5校验失败 ${md5_error}"
    else
        touch ${recv_localhost_path}"/.done_"${start_hour}"_"${topic_name}
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

get_recv(){
    topic_list=$1
    start_hour=$2
    end_hour=$3
    location=$4

    start_time=`get_time ${start_hour}`
    end_time=`get_time ${end_hour}`
    while [[ ${start_time} -le ${end_time} ]]
    do
        start_time_tmp=`date -d @${start_time} "+%Y%m%d%H"`
        echo "recv time:"${start_time_tmp}

        for topic_name in ${topic_list[@]}
        do
            echo "拷贝topic:"${topic_name}
            scp_hosts_name=`get_val_by_name ${topic_name}"_scp_hosts"`
            scp_hosts_list=`get_val_by_name ${scp_hosts_name}`

            recv_hosts_name=`get_val_by_name ${topic_name}"_recv_hosts"`
            recv_hosts_list=`get_val_by_name ${recv_hosts_name}`

            get_recv_by_topic "${topic_name}" "${start_time_tmp}" "${scp_hosts_list}" "${recv_hosts_list}" "${location}"
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
    -c)
        location="$1"
        shift
        ;;
    -c)
        location="$1"
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
if [[ ${topic_list} == "" ]]; then
    echo "请输入topic列表 -t"
    exit
else
    if [[ ${topic_list} == "all" ]]; then
        case "$platform" in
            pv)
                topic_list=${all_pv_topics}
                ;;
            live)
                topic_list=${all_live_topics}
                ;;
            play)
                topic_list=${all_play_topics}
                ;;
            pvs)
                topic_list=${all_pvs_topics}
                ;;
            mglive)
                topic_list=${all_mglive_topics}
                ;;
            dau)
                topic_list=${all_dau_topics}
                ;;
            mobile_vv)
                topic_list=${mobile_vv_topics}
                ;;
            other_vv)
                topic_list=${other_vv_topics}
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
if [[ ${location} == "" ]]; then
    echo "请输入当前服务器作用（server/client） -c"
    exit
fi

echo "topic_list:"${topic_list[*]}  "平台:"${platform} "scp开始日志时间:"${start_hour} "scp终止日志时间:"${end_hour} "服务器作用:"${location}
get_recv "$topic_list" "$start_hour" "$end_hour" "$location"

# vim: set ts=2 sw=2: #

