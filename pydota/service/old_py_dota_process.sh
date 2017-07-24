#!/bin/sh

if [[ -n "$HOME" && -e "$HOME/.pydota_recv" ]]; then
  . "$HOME/.pydota_recv"
else
  source ./etc/pydota_recv.conf
fi


function show_help(){
    echo "  options:"
    echo "    -h, --help                        Show this help."
    echo "    -t, --topic list                  需要获取原始日志的topic列表,topic之间用逗号分割 (eg. mobile_pv,pcweb_pv)."
    echo "    -p, --Video playback type         (play|pv|live|pvs|mglive)."
    echo "    -d, --delay_hour                  当前时间延迟时间,start_hour有值时,失效."
    echo "    -s, --start time                  获取这个小时的原始日志(eg.2016011301)."
    echo "    -m, --multi process               (1|0)是否多进程处理.非1时，全为单进程"
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

while [[ $# -gt 0 ]]; do
    opt="$1"
    shift

    case "$opt" in
    -h|\?|--help)
        show_help
        exit 0
        ;;
    -t|--topics)
        topics="$1"
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
    -d|--delay_hour)
        delay_hour="$1"
        shift
        ;;
    -m|--is_multi)
        is_multi="$1"
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
if [[ ${topics} == "" ]]; then
    echo "请输入topic列表 -t"
    exit
else
    if [[ ${topics} == "all" ]]; then
        case "$platform" in
            pv)
                topics=(${all_pv_topics})
                ;;
            live)
                topics=(${all_live_topics} ott_live)
                ;;
            play)
                topics=(${all_play_topics} mpp_vv_mobile_211_20151012_live)
                ;;
            pvs)
                topics=(${all_pvs_topics})
                ;;
            mglive)
                topics=(${all_mglive_topics})
                ;;
            dau)
                topics=(${all_dau_topics} dau_ott_3111)
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
        arr_tmp=(${topics})
        IFS="$OLD_IFS"
        topics=(${arr_tmp[@]})
    fi
fi

if [[ ${start_hour} == "" ]]; then
    if [[ ${delay_hour} == "" ]]; then
        start_hour=`date --date="$DATE - 1 hour" +%Y%m%d%H`
    else
        start_hour=`date --date="$DATE - $delay_hour hour" +%Y%m%d%H`
    fi
fi

echo "topic_list:"${topics[*]}  "平台:"${platform} "wash开始日志时间:"${start_hour}


topics_tmp=`echo ${topics[*]}`

start_time=${start_hour}"00"
work_path="/home/dota/pydota_v2/pydota"
pydota_ott_live="/data/nfs/live_recv"

sub_year=${start_time:0:4}
sub_month=${start_time:4:2}
sub_day=${start_time:6:2}
sub_hour=${start_time:8:2}

# 存原始日志的本机目录,和logserver服务器文件名一样
recv_path="/home/dota/data/recv/"

cd ${work_path}

if [[ ${platform} == "live" ]];then
    mkdir -p ${recv_path}/${sub_year}/${sub_month}/ott_live 2>/dev/null
    ott_live_file=(`ls ${pydota_ott_live}/OTT_Live_recv_${start_time:0:10}*`)
    if [ ${#ott_live_file[@]} -gt 1 ];then
        cat ${ott_live_file[*]} > ${recv_path}/${sub_year}/${sub_month}/ott_live/${start_time:0:10}"_ott_live_log"
    fi
    # 当ott_live无数据时，也生成.done文件
    touch ${recv_path}/${sub_year}/${sub_month}/ott_live/".done_"${start_time:0:10}"_ott_live"
fi


while true
do
    for topic in ${topics[*]};
    do
        if [[ ${topic} == "mpp_vv_mobile_211_20151012_live" ]];then
            local_file_path=${recv_path}/${sub_year}/${sub_month}/mpp_vv_mobile_211_20151012/
            done_file=${local_file_path}".done_"${start_time:0:10}"_mpp_vv_mobile_211_20151012"
        elif [[ ${topic} == "dau_ott_3111" ]];then
            local_file_path=${recv_path}/${sub_year}/${sub_month}/ott_pv/
            done_file=${local_file_path}".done_"${start_time:0:10}"_ott_pv"
        else
            local_file_path=${recv_path}/${sub_year}/${sub_month}/${topic}/
            done_file=${local_file_path}".done_"${start_time:0:10}"_"${topic}
        fi

        if [ -f ${done_file} ];then
            if [[ ${is_multi} -eq 1 ]];then
                ./service/py_dota_rawdata_recv_mulprocess.sh ${topic} ${start_time} &
            else
                ./service/py_dota_rawdata_recv.sh ${topic} ${start_time} &
            fi
            xrsh_arritemidx "$topics_tmp" "$topic"
            i=$?
            if [ ${i} -ge 0 ]; then
                unset topics[${i}]
            fi
        fi
    done

    len=${#topics[@]}
    if [ ${len} -eq 0 ];then
        break
    fi

    sleep 60
done
