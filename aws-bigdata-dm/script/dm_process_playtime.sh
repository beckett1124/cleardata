#!/bin/sh

WORK_PATH=$HOME//aws-bigdata-dm
CONF_LOG_FILE="$WORK_PATH/log/process_dm_script.log"

pydota_root_dm_des="$HOME/data/dm/des"
pydota_root_dm_err="$HOME/data/dm/dm_err"
pydota_s3_des="s3://dota-archive/dota/dm-des-test"
pydota_s3_err="s3://dota-archive/dota/dm-err-test"
pydota_s3_done="s3://dota-archive/dota/done"

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

function show_help(){
    echo "  options:"
    echo "    -h, --help                        Show this help."
    echo "    -t, --topic list                  需要清洗的topic列表,topic之间用逗号分割 (eg. mobile_pv,pcweb_pv)."
    echo "    -m, --dm_info                     清洗事实表."
    echo "    -p, --Video playback type         (play|pv|live|pvs|mglive)."
    echo "    -d, --delay_hour                  当前时间延迟时间,start_hour有值时,失效."
    echo "    -s, --start time                  获取这个小时的原始日志(eg.2016011301)."
}

send_error_mess(){
    mess=$1
    localhost=`LC_ALL=C /sbin/ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'`
    error_mess="所在机器:"${localhost}"  "${mess}
    #echo $error_mess
    curl -X POST --data-urlencode "payload={\"text\":\"${error_mess}\"}" https://hook.bearychat.com/=bw7by/incoming/71a4dcf2093e6b443a8b8f33d48fdac8
}

# 将记录分发到各自的小时文件
function split_file_to_hour()
{
    split_time=$1
    split_topic_name=$2
    split_dm_fact=$3

    split_file_path="${pydota_root_dm_des}/${topic}_${split_dm_fact}/${split_time:0:4}/${split_time:4:2}/${split_time:6:2}/${split_time:8:2}"

    cd ${split_file_path}

    split_files=`ls ${split_time}*${split_time}`
    echo "`date +%Y%m%d%H%M%S` hour file ${split_topic_name} is ${split_time}"
    if [[ ${#split_files[@]} -ge 1 ]];then
        cat ${split_files[@]} |awk -F "," -v split_topic_name=${split_topic_name} -v path=${split_file_path} -v recv_time=${split_time} -v dm_fact=${split_dm_fact} '{print > path"/tmp_"$2$3$4$5"_dm_"split_topic_name"_"dm_fact"_"recv_time}'
    fi

    tmp_split_files=`ls tmp_*`
    for fil in ${tmp_split_files[@]};
	do
        des_file_name=${fil##*/}
        time_file_name=${des_file_name#*tmp_}

        file_path_tmp=${pydota_root_dm_des}/${split_topic_name}_${split_dm_fact}/${time_file_name:0:4}/${time_file_name:4:2}/${time_file_name:6:2}/${time_file_name:8:2}
        if [ ! -d ${file_path_tmp} ]; then
            mkdir -p ${file_path_tmp}
        fi

        mv ${fil} ${file_path_tmp}/${time_file_name}
	done

    echo "ok"
}


function sync_local_file_to_s3()
{
    des_topic=$1
    des_fact=$2
    data_tpye=$3
    if [[ ${data_tpye} == "dm_des" ]];then
        desfiles=(`ls ${pydota_root_dm_des}/*/*/*/*/*/${start_hour}_dm_${des_topic}_${des_fact}_*`)
        s3_root_path=${pydota_s3_des}
    elif [[ ${data_tpye} == "dm_err" ]];then
        desfiles=(`ls ${pydota_root_dm_err}/*/*/*/*/*/err_${start_hour}_${des_topic}_${des_fact}_*`)
        s3_root_path=${pydota_s3_err}
    else
        Print ${LOG_WARNING} "-sync file to s3 failed: data_tpye[${data_tpye}] is illegal."
        return 1
    fi

    failed_des=()

	for fil in ${desfiles[*]};
	do
        dir=`dirname ${fil}`
        des_file_name=${fil##*/}
        time_file_name=${des_file_name#*err_}


        s3_des_path=${s3_root_path}/${des_topic}/${des_fact}/${time_file_name:0:4}/${time_file_name:4:2}/${time_file_name:6:2}/${time_file_name:8:2}
	    msg=`aws s3 sync ${dir} ${s3_des_path} --exclude "*" --include "${des_file_name}" 2>&1`
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

        s3_des_path=${s3_root_path}/${des_topic}/${des_fact}/${time_file_name_f:0:4}/${time_file_name_f:4:2}/${time_file_name_f:6:2}/${time_file_name_f:8:2}
	    msg_f=`aws s3 sync ${dir} ${s3_des_path} --exclude "*" --include "${des_file_name_f}" 2>&1`
        s3_sync_return_mess=$?
        if [[ ${s3_sync_return_mess} -ne 0 ]];then
            Print ${LOG_WARNING} "-[${des_topic}]sync des to s3 failed: [${fil_f}]."
            Print ${LOG_WARNING} "-err_msg:[${msg_f}]."
            send_error_mess "${des_topic}---${fil_f}: sync des to s3 失败 错误码:${s3_sync_return_mess}"
            return 1
        fi
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

if [[ ${platform} == "" ]]; then
    echo "请输入原始日志播放类型 -p"
    exit
fi

if [[ ${topics} == "" ]]; then
    echo "请输入topic列表 -t"
    exit
else
    OLD_IFS="$IFS"
    IFS=","
    arr_tmp=(${topics})
    IFS="$OLD_IFS"
    topics=(${arr_tmp[@]})
fi

if [[ ${start_hour} == "" ]]; then
    if [[ ${delay_hour} == "" ]]; then
        start_hour=`date --date="$DATE - 1 hour" +%Y%m%d%H`
    else
        start_hour=`date --date="$DATE - $delay_hour hour" +%Y%m%d%H`
    fi
fi

echo "topic_list:"${topics[*]}  "平台:"${platform} "dm_wash开始日志时间:"${start_hour}


topics_tmp=`echo ${topics[*]}`

start_time=${start_hour}"00"
work_path="$HOME/aws-bigdata-dm/"

sub_year=${start_time:0:4}
sub_month=${start_time:4:2}
sub_day=${start_time:6:2}
sub_hour=${start_time:8:2}

# 存des文件的本机目录,和logserver服务器文件名一样
des_path="$HOME/data/des/"
md5_check_path="$HOME/data/md5_check"
dm_done_path="$HOME/data/done"

mkdir -p ${dm_done_path}/${sub_year}/${sub_month}


cd ${work_path}


len=${#topics[@]}
if [ ${len} -eq 0 ];then
    echo "topics is null"
    exit -1
fi

for topic in ${topics[*]};
do
    local_file_path="${des_path}/${topic}/${start_hour:0:4}/${start_hour:4:2}/${start_hour:6:2}/${start_hour:8:2}"

    files=(`ls ${local_file_path}/*|grep -v "_SUCCESS"`)

    des_done=${md5_check_path}/${sub_year}/${sub_month}/${topic}_${start_hour}.done

    if [ ! -f ${des_done} ];then
        send_error_mess "[${start_hour}]${topic} des_done 文件未生成. dm_wash 失败"
        exit 1
    fi

    if [ ${#files[@]} -ge 1 ];then
        cat ${files[*]} | python app.py ${topic} ${dm_fact} ${start_hour}

        dm_err=$?
        if [[ ${dm_err} -ne 0 ]];then
            exit 1
        fi

        split_file_to_hour ${start_hour} ${topic} ${dm_fact}
        sync_local_file_to_s3 ${topic} ${dm_fact} dm_des

        sync_err=$?
        if [[ ${sync_err} -ne 0 ]];then
            exit 1
        fi

        sync_local_file_to_s3 ${topic} ${dm_fact} dm_err
    fi

    # 生成done文件，并上传到s3
    dm_done=${dm_done_path}/${sub_year}/${sub_month}/${topic}_${start_hour}.done

    touch ${dm_done}
    err_msg=`aws s3 cp ${dm_done} ${pydota_s3_done}/ 2>&1`
    err_num=$?
    if [[ ${err_num} -ne 0 ]];then
        send_error_mess "[${start_hour}]${topic} des_done 文件上传s3失败. err_msg:[${err_msg}]"
        exit 1
    fi

done