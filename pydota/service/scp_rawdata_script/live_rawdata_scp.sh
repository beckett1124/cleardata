#!/bin/sh
# livarawdata日志检验的topic名称
live_topics=("mobile_live_2011_20151105 ott_live mobile_live_2111_20151225 macclient_live_8111_20160105 rt_live_pcweb mobile_live_2111_20151225_aws")
#topics=("mpp_vv_pcweb")
local_host="10.100.5.4"
live_cp_host="10.100.1.3"

if [ $# -ge 1 ];then
    start_time=$1
else
    start_time=`date --date="$DATE - 4 hour" +%Y%m%d%H`
fi

sub_year=${start_time:0:4}
sub_month=${start_time:4:2}
sub_day=${start_time:6:2}
sub_hour=${start_time:8:2}

# 存在日志的目录
md5_path="/home/dota/data/md5_check/*/*/"
des_path="/home/dota/data/des/*/*/"
orig_path="/home/dota/data/orig/*/*/"
local_des_path="/home/dota/data/des/"
nfs_path="/data/nfs/dota/des/"
play_rawdata_check_path="/home/dota/data/play_rawdata_check/"

s3_root_path="s3://dota-archive/dota"
cp_flag=0

function index_err_log()
{
    index_topic=$1
    index_des_err_file_list=(`ls ${des_path}/err_*_${index_topic}_${start_time}00*`)

    echo "start index ${index_topic} err_log"

    if [ ${#index_des_err_file_list[@]} -ge 1 ];then

        # 发送错误日志 建立索引
        cat ${index_des_err_file_list[*]} | python ~/online/mgtv-bigdata-index/app.py wash ${topic} ${start_time}
    fi
}

echo "start scp liverawdata,date:${start_time}"

function send_error_mess(){
    mess=$1
    localhost=`LC_ALL=C /sbin/ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'`
    error_mess="所在机器:"${localhost}"  "${mess}
    #echo $error_mess
    curl -X POST --data-urlencode "payload={\"text\":\"${error_mess}\"}" https://hook.bearychat.com/=bw7by/incoming/71a4dcf2093e6b443a8b8f33d48fdac8
}

function cp_local_to_s3()
{
    d_file=$1
    des_topic=$2
    des_type=$3

    dir=`dirname ${d_file}`
    des_file_name=${d_file##*/}
    time_file_name=${des_file_name#*err_}


    s3_des_path=${s3_root_path}/${des_type}/${des_topic}/${time_file_name:0:4}/${time_file_name:4:2}/${time_file_name:6:2}/${time_file_name:8:2}/

    # cp to s3
    msg=`aws s3 cp ${d_file} ${s3_des_path}`
    s3_cp_return_mess=$?

    if [[ ${s3_cp_return_mess} -ne 0 ]];then
        # sleep 60s, retry
        sleep 60
        msg_1=`aws s3 cp ${d_file} ${s3_des_path}`
        s3_cp_return_mess_1=$?
        if [[ ${s3_cp_return_mess_1} -ne 0 ]];then
            cp_flag=1
            send_error_mess "cp ${d_file} to s3 faild"
        fi
    fi

}

function scp_des_to_local()
{
    topics=$1
    cp_host=$2

    for topic in ${topics};do
        #scp

        ssh "dota@"${cp_host} "ls ${md5_path}/.done_${topic}_${start_time}00.md5"
        done_mess=$?
        # 查看done文件失败后，报警通知
        if [ ${done_mess} -ne 0 ];then
            cp_flag=1
            err_msg_done="${cp_host}::${start_time}:${topic} 未生成done文件 .done_${topic}_${start_time}00.md5
            错误码:${done_mess}"
            send_error_mess ${err_msg_done}
            continue
        fi

        # des scp
        cp_file_name="*_playrawdata_${topic}_${start_time}00"
        cp_file_list=`ssh "dota@${cp_host}" "ls ${des_path}/${cp_file_name}" 2>&1`
        cp_msg=$?
        if [ ${cp_msg} -eq 0 ];then
            for fil in ${cp_file_list[*]};
            do
                echo ${fil}
                mkdir -p ${fil%/*}
                scp -l 800000 dota@${cp_host}:${fil} ${fil}

                # scp to s3
#                cp_local_to_s3 ${fil} ${topic} "des-test"

            done
        elif [ ${cp_msg} -eq 2 ];then
            echo ""
        else
            cp_flag=1
            err_msg="des_scp_error ${cp_host}::${start_time}:${topic}
            错误信息:${cp_file_list}
            错误码:${cp_msg}"
            send_error_mess ${err_msg}
        fi

        des_err_file_name="err_*_${topic}_${start_time}00*"
        des_err_file_list=`ssh "dota@${cp_host}" "ls ${des_path}/${des_err_file_name}" 2>&1`
        cp_msg=$?
        if [ ${cp_msg} -eq 0 ];then
            for fil in ${des_err_file_list[*]};
            do
                mkdir -p ${fil%/*}
                scp -l 800000 dota@${cp_host}:${fil} ${fil}

#                cp_local_to_s3 ${fil} ${topic} "err-test"

            done
        elif [ ${cp_msg} -eq 2 ];then
            echo ""
        else
            err_msg="des_err_scp_error ${cp_host}::${start_time}:${topic}
            错误信息:${des_err_file_list}
            错误码:${cp_msg}"
            send_error_mess ${err_msg}
        fi

    done
}

scp_des_to_local "${live_topics[*]}"  ${live_cp_host}


if [ ${cp_flag} -eq 0 ];then
    touch ${local_des_path}/${sub_year}/${sub_month}/.${start_time}_liverawdata.done


    for topic in ${live_topics};do
        index_err_log ${topic}
    done

fi
echo "end scp liverawdata,date:${start_time}"