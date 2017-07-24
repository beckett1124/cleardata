#!/bin/sh
if [[ -n "$HOME" && -e "$HOME/.pydota_recv" ]]; then
  . "$HOME/.pydota_recv"
else
  source $HOME/pydota_v2/pydota/service/etc/pydota_recv.conf
fi


topic=$1
start_time=$2
file_md5=$3
task_id=$4
sub_year=${start_time:0:4}
sub_month=${start_time:4:2}
sub_day=${start_time:6:2}
sub_hour=${start_time:8:2}

function get_val_by_name(){
    name=$1
    val=$(eval "echo \$${name}")
    echo ${val}
}

file_prefix=`get_val_by_name ${topic}"_file_name"`
filename=`${file_prefix} ${sub_year} ${sub_month} ${sub_day} ${sub_hour}`

work_path="$HOME/pydota_v2/pydota"

# 存原始日志的本机目录,和logserver服务器文件名一样
recv_path="$HOME/data/recv/"
des_path="$HOME/data/des/"
md5_check_path="$HOME/data/md5_check/"
record_info_path="$HOME/data/record_info/"
mkdir -p ${md5_check_path}/${sub_year}/${sub_month}/ 2>/dev/null
mkdir -p ${record_info_path}/${sub_year}/${sub_month}/${topic} 2>/dev/null


#if [[ ${topic} == "mpp_vv_mobile_211_20151012_live" ]];then
#    local_file_path=${recv_path}/${sub_year}/${sub_month}/mpp_vv_mobile_211_20151012/
#    file=(`ls ${local_file_path}/${filename}`)
#elif [[ ${topic} == "dau_ott_3111" ]];then
#    local_file_path=${recv_path}/${sub_year}/${sub_month}/ott_pv/
#    file=(`ls ${local_file_path}/${filename}`)
#else
#    local_file_path=${recv_path}/${sub_year}/${sub_month}/${topic}/
#    file=(`ls ${local_file_path}/${filename}`)
#fi

file=$(cat ${file_md5}|awk '{print $1}')

cd ${work_path}

if [ ${#file[@]} -ge 1 ];then
#    cat ${file[*]} | python format/format_${topi}.py ${start_time}
    info_row=`cat ${file[*]} | python run_wash_dispy.py ${topic} ${start_time}`

    if [[ ${info_row} == "" ]];then
        continue
    else
        echo ${info_row} > ${record_info_path}/${sub_year}/${sub_month}/${topic}/${start_time:0:10}_${topic}_${task_id}.info
    fi

    desfiles=(`ls ${des_path}/*/*/*rawdata_${topic}_${start_time}`)

    if [ ${#desfiles[@]} -ge 1 ];then
        for des_file in ${desfiles[*]};
        do
            tmp_file_name=`basename ${des_file}`
            cat ${des_file} | python service/made_md5.py > ${md5_check_path}/${sub_year}/${sub_month}/${tmp_file_name}.md5
        done
    fi

    touch ${md5_check_path}/${sub_year}/${sub_month}/.done_${topic}_${start_time}.md5

    exit 0
else
    touch ${md5_check_path}/${sub_year}/${sub_month}/.done_${topic}_${start_time}.md5
fi