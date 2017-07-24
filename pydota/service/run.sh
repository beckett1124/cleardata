#!/bin/bash
export WORK_PATH=$HOME/pydota_v2/pydota/service
CONF_LOG_FILE="$WORK_PATH/../../log/process_main.log"

pydota_root_des="$HOME/data/des"
pydota_root_orig="$HOME/data/orig"
pydota_root_recv="$HOME/data/recv"
pydota_root_check="$HOME/data/recv_check"
record_info_path="$HOME/data/record_info/"
pydota_s3_des="s3://dota-archive/dota/des-test"
pydota_s3_orig="s3://dota-archive/dota/orig-test"
pydota_s3_err="s3://dota-archive/dota/err-test"


run_time=""
task_id=""


LOG_FATAL=1
LOG_WARNING=2
LOG_NOTICE=4
LOG_TRACE=8
LOG_DEBUG=16
LOG_LEVEL_TEXT=(
	[1]="FATAL"
	[2]="WARNING"
	[4]="NOTICE"
	[8]="TRACE"
	[16]="DEBUG"
)

TTY_FATAL=1
TTY_PASS=2
TTY_TRACE=4
TTY_INFO=8
TTY_MODE_TEXT=(
	[1]="[FAIL ]"
	[2]="[WARNING ]"
	[4]="[NOTICE]"
	[8]="[TRACE]"
	[16]="[DEBUG]"
)

#0  OFF
#1  高亮显示
#4  underline
#5  闪烁
#7  反白显示
#8  不可见

#30  40  黑色
#31  41  红色
#32  42  绿色
#33  43  黄色
#34  44  蓝色
#35  45  紫红色
#36  46  青蓝色
#37  47  白色
TTY_MODE_COLOR=(
	[1]="1;31"
	[2]="1;32"
	[4]="0;36"
	[8]="1;33"
	[16]="1;35"
)

##! @BRIEF: print info to tty & log file
##! @IN[int]: $1 => tty mode
##! @IN[string]: $2 => message
##! @RETURN: 0 => sucess; 1 => failure
function Print()
{
	local tty_mode=$1
	local message="$2"
	local time=`date "+%m-%d %H:%M:%S"`
	echo "${LOG_LEVEL_TEXT[$tty_mode]}: $time: * $$ $message" >> ${CONF_LOG_FILE}
	echo -e "\e[${TTY_MODE_COLOR[$tty_mode]}m${TTY_MODE_TEXT[$tty_mode]} ${message}\e[m"
	return $?
}

function execshell()
{
	$@
	[[ $? != 0 ]] && {
		echo "$@失败"
		print_help
		exit 1
	}
	return 0
}

print_help()
{
	echo "samples:"
	echo "-----------------------------------------------------------------------------------"
	echo "sh run.sh"
	echo "-----------------------------------------------------------------------------------"
	return 0
}

send_error_mess(){
    mess=$1
    localhost=`LC_ALL=C /sbin/ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'`
    error_mess="所在机器:"${localhost}"  "${mess}
    #echo $error_mess
    curl -X POST --data-urlencode "payload={\"text\":\"${error_mess}\"}" https://hook.bearychat.com/=bw7by/incoming/71a4dcf2093e6b443a8b8f33d48fdac8
}

function md5_check(){
    dispy_md5_file=$1
    locacl_md5_file=$2
    err_md5_check=$3
    cat ${dispy_md5_file} ${locacl_md5_file} | awk '{print $3}' | sort | uniq -c | awk '{if($1!=2) print $0}' > ${err_md5_check}
    failed_num=`wc -l ${err_md5_check}|awk '{print $1}'`

    if [[ ${failed_num} -ge 1 ]];then
        cat ${dispy_md5_file} ${locacl_md5_file} | awk '{gsub(".*/","",$1);print $1" "$3}'|sort | uniq -c | awk '{if($1!=2) print $0}' > ${err_md5_check}
        failed_num=`wc -l ${err_md5_check}|awk '{print $1}'`
    fi
    return ${failed_num}
}


function get_recv_file()
{
    recv_file=$1
    local_recv_path=$2

	s3_scp_path=${recv_file%/*}
	file_name=${recv_file##*/}
    msg=`aws s3 sync ${s3_scp_path} ${local_recv_path} --exclude "*" --include "${file_name}" 2>&1`

    err_num=$?
    if [[ ${err_num} -ne 0 ]];then
        Print ${LOG_WARNING} "[${task_id}]---sync file from s3 failed: [${file_name}]."
    fi

	echo "${local_recv_path}/${file_name}"

}

function sync_local_file_to_s3()
{
    des_topic=$1
    data_tpye=$2
    if [[ ${data_tpye} == "des" ]];then
        desfiles=(`ls ${pydota_root_des}/*/*/*rawdata_${des_topic}_${run_time}00`)
        s3_root_path=${pydota_s3_des}
    elif [[ ${data_tpye} == "orig" ]];then
        desfiles=(`ls ${pydota_root_orig}/*/*/*${des_topic}_${run_time}00`)
        s3_root_path=${pydota_s3_orig}

    elif [[ ${data_tpye} == "des_err" ]];then
        desfiles=(`ls ${pydota_root_des}/*/*/err_*${des_topic}_${run_time}00_des_err`)
        s3_root_path=${pydota_s3_err}

    elif [[ ${data_tpye} == "orig_err" ]];then
        desfiles=(`ls ${pydota_root_orig}/*/*/err_*${des_topic}_${run_time}00_orig_err`)
        s3_root_path=${pydota_s3_err}

    else
        Print ${LOG_WARNING} "[${task_id}]-sync file to s3 failed: data_tpye[${data_tpye}] is illegal."
        return 1
    fi

    failed_des=()

	for fil in ${desfiles[*]};
	do
        dir=`dirname ${fil}`
        des_file_name=${fil##*/}
        time_file_name=${des_file_name#*err_}

        mv ${fil} ${fil}_${task_id}

        s3_des_path=${s3_root_path}/${des_topic}/${time_file_name:0:4}/${time_file_name:4:2}/${time_file_name:6:2}/${time_file_name:8:2}
	    msg=`aws s3 sync ${dir} ${s3_des_path} --exclude "*" --include "${des_file_name}_${task_id}" 2>&1`
        s3_sync_return_mess=$?
        if [[ ${s3_sync_return_mess} -ne 0 ]];then
            failed_des=(${failed_des[@]} ${fil})
        fi
	done

	# 重试, sync
	for fil_f in ${failed_des[*]};
	do
        dir=`dirname ${fil_f}`
        des_file_name_f=${fil_f##*/}
        time_file_name_f=${des_file_name_f#*err_}

        s3_des_path=${s3_root_path}/${des_topic}/${time_file_name_f:0:4}/${time_file_name_f:4:2}/${time_file_name_f:6:2}/${time_file_name_f:8:2}
	    msg_f=`aws s3 sync ${dir} ${s3_des_path} --exclude "*" --include "${des_file_name_f}_${task_id}" 2>&1`
        s3_sync_return_mess=$?
        if [[ ${s3_sync_return_mess} -ne 0 ]];then
            Print ${LOG_WARNING} "[${task_id}]---[${des_topic}]sync des to s3 failed: [${fil_f}]."
            Print ${LOG_WARNING} "[${task_id}]-err_msg:[${msg_f}]."
            send_error_mess "${des_topic}---${fil_f}: sync des to s3 失败 错误码:${s3_sync_return_mess}"
            return 1
        fi
	done

}

function send_info_dispy()
{
    info_file=$1

    curl_jobid=`sed -n "3p" ${info_file}`
    curl_taskid=`sed -n "2p" ${info_file}`
    curl_irows=`sed -n "1p" ${info_file}|awk '{print $1}'`
    curl_orows=`sed -n "1p" ${info_file}|awk '{print $2}'`
    curl_erows=`sed -n "1p" ${info_file}|awk '{print $3}'`
    curl_srows=`sed -n "1p" ${info_file}|awk '{print $4}'`

    curl_time=`sed -n "4p" ${info_file}`

    url_str="http://127.0.0.1:5355/sum/summary.action?jobid=${curl_jobid}&taskid=${curl_taskid}&irows=${curl_irows}&orows=${curl_orows}&erows=${curl_erows}&srows=${curl_srows}&time=${curl_time}"

    Print ${LOG_NOTICE} "[${task_id}]---info_url: ${url_str}"
    if [[ ${curl_jobid} == "" || ${curl_taskid} == "" || ${curl_irows} == "" || ${curl_orows} == "" ||  ${curl_erows} == "" || ${curl_srows} == "" || ${curl_time} == "" ]];then
        send_error_mess "[${task_id}]-get output info error"
        exit -1
    else
        curl_info=`curl "${url_str}"`
        Print ${LOG_NOTICE} "[${task_id}]---url_return: ${curl_info}"
    fi
}


function proncess_wash()
{
    dispy_file="$@"
	Print ${LOG_NOTICE} "[${task_id}]---process wash start: ${dispy_file}."
	if [ ! -f ${dispy_file} ];then
	    # 告警报错
	    Print ${LOG_FATAL} "[${task_id}]---dispy_file[${dispy_file}] not exist"
        send_error_mess "[${task_id}]---dispy_file[${dispy_file}] not exist"
        exit 1
	fi

    run_time=`sed -n "1p" ${dispy_file}`
    topic_name=`sed -n "2p" ${dispy_file}`
    job_id=`sed -n "3p" ${dispy_file}`
    task_id=`sed -n "4p" ${dispy_file}`
    if [[ ${run_time} == "" || ${topic_name} == "" || ${job_id} == "" || ${task_id} == "" ]];then
	    Print ${LOG_FATAL} "get dispy_file info wrong, please check [${dispy_file}]"
        send_error_mess "get dispy_file info wrong, please check [${dispy_file}]"
        # 告警报错
        exit -1
    fi

    check_path=${pydota_root_check}/${run_time:0:4}/${run_time:4:2}/${topic_name}

    mkdir -p ${check_path}

    dispy_md5_file=${check_path}/${run_time}_dispy_file_${task_id}.md5
    local_md5_file=${check_path}/${run_time}_local_file_${task_id}.md5
    err_md5_file=${check_path}/err_${run_time}_${task_id}.md5

    cat ${dispy_file}|awk -F'\t' '{if(NF==4)print $0}' > ${dispy_md5_file}

    if [ ! -f ${dispy_md5_file} ];then
	    # 告警报错
	    Print ${LOG_FATAL} "[${task_id}]---gen dispy_md5_file[${dispy_md5_file}] failed"
        send_error_mess "[${task_id}]---gen dispy_md5_file[${dispy_md5_file}] failed"
        exit 1
	fi


    # 从s3拉取文件到本机
    recv_files=$(cat ${check_path}/${run_time}_dispy_file_${task_id}.md5|awk '{print $1}')

    # recv文件md5_check
    rm ${local_md5_file} 2>/dev/null

    recv_local_path=${pydota_root_recv}/${run_time:0:4}/${run_time:4:2}/${topic_name}
    mkdir -p ${recv_local_path}

    rm ${recv_local_path}/.done_${run_time}_${topic_name} 2>/dev/null


    for recv_file in ${recv_files[@]};
    do
        Print ${LOG_NOTICE} "[${task_id}]---get recv_file start: ${recv_file}."
	    local_file=`get_recv_file ${recv_file} ${recv_local_path}`
        Print ${LOG_NOTICE} "[${task_id}]---get recv_file finish: ${recv_file}."
	    md5_sum=`md5sum ${local_file} |awk '{print $1}'`
	    line_num=`wc -l ${local_file} |awk '{print $1}'`
	    file_size=`ls -l ${local_file} |awk '{print $5}'`
        echo "${local_file} ${file_size} ${md5_sum} ${line_num}" >> ${local_md5_file}
    done

    md5_check ${dispy_md5_file} ${local_md5_file} ${err_md5_file}
    md5_return=$?
    if [[ ${md5_return} -ge 1 ]];then
        md5_error=`cat ${err_md5_file}`
        # 报警
        Print ${LOG_FATAL} "[${task_id}]---check md5_file failed"
        send_error_mess "[${task_id}]---check md5_file failed"
#        echo "${md5_error}"
        exit -1
    else
        touch ${recv_local_path}/.done_${run_time}_${topic_name}

        # wash log
        cd ${WORK_PATH}
        pro_start_time=`date "+%s"`
        sh py_dota_process_dispy.sh -t ${topic_name} -p play -s ${run_time} -f ${local_md5_file} -i ${task_id}
        pro_end_time=`date "+%s"`
        pro_time=$((pro_end_time-pro_start_time))

        echo "${task_id}" >> ${record_info_path}/${run_time:0:4}/${run_time:4:2}/${topic_name}/${run_time:0:10}_${topic_name}_${task_id}.info
        echo "${job_id}" >> ${record_info_path}/${run_time:0:4}/${run_time:4:2}/${topic_name}/${run_time:0:10}_${topic_name}_${task_id}.info
        echo "${pro_time}" >> ${record_info_path}/${run_time:0:4}/${run_time:4:2}/${topic_name}/${run_time:0:10}_${topic_name}_${task_id}.info
        Print ${LOG_NOTICE} "[${task_id}]---process wash finish: ${dispy_file}."

    fi

    sync_local_file_to_s3 ${topic_name} des

    send_info_dispy ${record_info_path}/${run_time:0:4}/${run_time:4:2}/${topic_name}/${run_time:0:10}_${topic_name}_${task_id}.info

    sync_local_file_to_s3 ${topic_name} orig
    sync_local_file_to_s3 ${topic_name} des_err
    sync_local_file_to_s3 ${topic_name} orig_err

}



#参数解析，功能调度
Main()
{
	execshell "proncess_wash $@"
}
Main "$@"