#!/bin/sh
if [[ -n "$HOME" && -e "$HOME/.pydota_s3" ]]; then
  . "$HOME/.pydota_s3"
else
  source ../etc/pydota_s3.conf
fi


topic=$1
start_time=$2
sub_year=${start_time:0:4}
sub_month=${start_time:4:2}
sub_day=${start_time:6:2}
sub_hour=${start_time:8:2}
sub_time_path=${sub_year}/${sub_month}/${sub_day}/${sub_hour}


function get_val_by_name(){
    name=$1
    val=$(eval "echo \$${name}")
    echo ${val}
}

file_prefix=`get_val_by_name ${topic}"_file_name"`
filename=`${file_prefix} ${sub_year} ${sub_month} ${sub_day} ${sub_hour}`

work_path="/home/dota/pydota_v2/pydota"

# 存原始日志的本机目录,和logserver服务器文件名一样
recv_path="/home/dota/data/recv/"
des_path="/home/dota/data/des/"
md5_check_path="/home/dota/data/md5_check/"
mkdir -p ${md5_check_path}/${sub_year}/${sub_month}/ 2>/dev/null

if [[ ${topic} == "mpp_vv_mobile_211_20151012_live" ]];then
    recv_server_path=`get_val_by_name "mpp_vv_mobile_211_20151012_path"`

    local_file_path=${recv_root_path}/${recv_server_path}/${sub_time_path}
    file=(`ls ${local_file_path}/${filename}`)
else
    recv_server_path=`get_val_by_name ${topic}"_path"`

    local_file_path=${recv_root_path}/${recv_server_path}/${sub_time_path}
    file=(`ls ${local_file_path}/${filename}`)
fi

cd ${work_path}

if [ ${#file[@]} -ge 1 ];then
#    cat ${file[*]} | python format/format_${topic}.py ${start_time}
    cat ${file[*]} | python run_wash.py ${topic} ${start_time}

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