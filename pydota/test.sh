#!/bin/sh
# 从raw数据中计算各个平台每个小时的数据
# py_dota_report_vv_detail_hour.sh pcweb 20151007

# 设置bearychat发送目标为报警频道
BEARYCHAT_WEBHOOK="https://hook.bearychat.com/=bw7by/incoming/71a4dcf2093e6b443a8b8f33d48fdac8"

if [ $# -eq 2 ];then
    start_time=$2
else
    start_time=`date +%Y%m%d`
fi

sub_path_year=${start_time:0:4}
sub_path_month=${start_time:4:2}
sub_path_day=${start_time:6:2}
sub_path=${sub_path_year}/${sub_path_month}

work_path="/home/dota/pydota/pydota"
pydota_orig="/home/dota/data/orig"
pydota_s3_orig="s3://dota-archive/dota/data/orig"
pydota_s3_des="s3://dota-archive/dota/data/des"

cd ${work_path}

function sync_to_s3(){
    sub_type=$1
    # 全天运行，逐小时合并各个topic数据

    for i in {0..23}
    do
        cur_time=`date --date="$start_time $i hour" +%Y%m%d%H`

        filename=${cur_time}*
        err_filename=err_${cur_time}*

        cd ${pydota_orig}/${sub_path}

        # 某一个小时时，只有所有相关topic的文件
        files=(`ls ${filename}`)
        err_files=(`ls ${err_filename}`)


        nowtime_s=`date "+%Y/%m/%d %H:%M:%S"`
        echo "start sync ${sub_type} ${cur_time}"

        if [ ${sub_type} == "pv" ];then

            plat="pv"
            aws s3 sync . ${pydota_s3_orig}/${plat}/${sub_path_year}/${sub_path_month}/${sub_path_day}/${cur_time:8:2}/ --exclude "*" --include "${filename}pv*"
            aws s3 sync . ${pydota_s3_orig}/${plat}/${sub_path_year}/${sub_path_month}/${sub_path_day}/${cur_time:8:2}/ --exclude "*" --include "${err_filename}pv*"

        elif [ ${sub_type} == "play" ];then

            plat="vv"
            aws s3 sync . ${pydota_s3_orig}/${plat}/${sub_path_year}/${sub_path_month}/${sub_path_day}/${cur_time:8:2}/ --exclude "*" --include "${filename}" --exclude "*pv*"
            aws s3 sync . ${pydota_s3_orig}/${plat}/${sub_path_year}/${sub_path_month}/${sub_path_day}/${cur_time:8:2}/ --exclude "*" --include "${err_filename}" --exclude "*pv*"

        else
            echo "wrong platform!"
            exit 1
        fi

        nowtime_e=`date "+%Y/%m/%d %H:%M:%S"`
        echo "end sync ${sub_type} ${cur_time}"

        echo "sync ${sub_type} time: ${nowtime_s} to ${nowtime_e}"


    # for
    done
}


function split_lplay(){
    topic=$1
    pt_index=$2
    desfile=$3

    des_dir=`dirname ${desfile}`
    origin_des_file_name=${desfile##*/}

    lplay_des_file_name=`echo "${origin_des_file_name}"| sed 's/rawdata/&_lplay/'`

    time_log=${origin_des_file_name:0:12}

    if [ ! -d ${des_dir} ]; then
        mkdir -p ${des_dir}
    fi

    echo -n "" > ${des_dir}/${lplay_des_file_name}
    echo -n "" > ${des_dir}/${origin_des_file_name}_tmp

    cd ${des_dir}

    echo "`date +%Y%m%d%H%M%S` hour file ${origin_des_file_name}"

    awk -F "," -v pt_index=${pt_index} '{if($pt_index=="2") {print}}' ${origin_des_file_name} >> ${des_dir}/${lplay_des_file_name}

    awk -F "," -v pt_index=${pt_index} '{if${pt_index=="0") {print}}' ${origin_des_file_name} >> ${des_dir}/${origin_des_file_name}_tmp

    mv ${origin_des_file_name}_tmp ${origin_des_file_name}

    echo "ok"
}

split_lplay ott_vv_311_20151012 17