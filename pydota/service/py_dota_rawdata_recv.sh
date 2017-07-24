#!/bin/sh
if [[ -n "$HOME" && -e "$HOME/.pydota_recv" ]]; then
  . "$HOME/.pydota_recv"
else
  source ./etc/pydota_recv.conf
fi


topic=$1
start_time=$2
dm_fact=$3

sub_year=${start_time:0:4}
sub_month=${start_time:4:2}
sub_day=${start_time:6:2}
sub_hour=${start_time:8:2}

split_lplay_topics=("ott_vv_311_20151012")

function get_val_by_name(){
    name=$1
    val=$(eval "echo \$${name}")
    echo ${val}
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

    awk -F "," -v pt_index=${pt_index} '{if($pt_index=="2" || $pt_index=="5") {print}}' ${origin_des_file_name} >> ${des_dir}/${lplay_des_file_name}

    awk -F "," -v pt_index=${pt_index} '{if($pt_index=="0") {print}}' ${origin_des_file_name} >> ${des_dir}/${origin_des_file_name}_tmp

    mv ${origin_des_file_name}_tmp ${origin_des_file_name}

    echo "ok"
}


send_error_mess(){
    mess=$1
    localhost=`LC_ALL=C /sbin/ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'`
    error_mess="所在机器:"${localhost}"  "${mess}
    #echo $error_mess
    curl -X POST --data-urlencode "payload={\"text\":\"${error_mess}\"}" https://hook.bearychat.com/=bw7by/incoming/71a4dcf2093e6b443a8b8f33d48fdac8
}

file_prefix=`get_val_by_name ${topic}"_file_name"`
filename=`${file_prefix} ${sub_year} ${sub_month} ${sub_day} ${sub_hour}`

wash_dm_topics=`get_val_by_name ${dm_fact}"_wash_dm_topics"`

work_path="/home/dota/pydota_v2/pydota"

# 存原始日志的本机目录,和logserver服务器文件名一样
recv_path="/home/dota/data/recv/"
des_path="/home/dota/data/des/"
md5_check_path="/home/dota/data/md5_check/"
mkdir -p ${md5_check_path}/${sub_year}/${sub_month}/ 2>/dev/null

if [[ ${topic} == "mpp_vv_mobile_211_20151012_live" ]];then
    local_file_path=${recv_path}/${sub_year}/${sub_month}/mpp_vv_mobile_211_20151012/
    file=(`ls ${local_file_path}/${filename}`)
elif [[ ${topic} == "dau_ott_3111" ]];then
    local_file_path=${recv_path}/${sub_year}/${sub_month}/ott_pv/
    file=(`ls ${local_file_path}/${filename}`)
else
    local_file_path=${recv_path}/${sub_year}/${sub_month}/${topic}/
    file=(`ls ${local_file_path}/${filename}`)
fi

cd ${work_path}

if [ ${#file[@]} -ge 1 ];then
#    cat ${file[*]} | python format/format_${topic}.py ${start_time}
    cat ${file[*]} | python run_wash.py ${topic} ${start_time}

    py_err_no=$?
    if [[ ${py_err_no} -ne 0 ]];then
        send_error_mess "[${start_time}]process run_wash [${topic}] failed"
        exit 1
    fi

    desfiles=(`ls ${des_path}/*/*/*rawdata_${topic}_${start_time}`)

    for split_topic in ${split_lplay_topics[@]};
    do
        if [[ ${split_topic} == ${topic} ]];then
            if [ ${#desfiles[@]} -ge 1 ];then
                for desfile in ${desfiles[*]};
                do
                    split_lplay ${topic} 17 ${desfile}
                done
            fi

            touch ${md5_check_path}/${sub_year}/${sub_month}/.done_lplay_${topic}_${start_time}.md5
            break

        fi
    done
#    if [ ${#desfiles[@]} -ge 1 ];then
#        for des_file in ${desfiles[*]};
#        do
#            tmp_file_name=`basename ${des_file}`
#            cat ${des_file} | python service/made_md5.py > ${md5_check_path}/${sub_year}/${sub_month}/${tmp_file_name}.md5
#        done
#    fi

    for dm_topic in ${wash_dm_topics[@]};do
        if [[ ${dm_topic} == lplay_${topic} ]];then
            cd $HOME/aws-bigdata-dm/script

            sh dm_process_yg.sh -t lplay_${topic} -p pv -m lplay_fact -s ${start_time:0:10} &
            break
        fi
    done

    touch ${md5_check_path}/${sub_year}/${sub_month}/.done_${topic}_${start_time}.md5

    for dm_topic in ${wash_dm_topics[@]};do
        if [[ ${dm_topic} == ${topic} ]];then
            cd $HOME/aws-bigdata-dm/script

            sh dm_process_yg.sh -t ${topic} -p pv -m ${dm_fact} -s ${start_time:0:10}

            _res=$?
            if [[ _res -ne 0 ]];then
                send_error_mess "[${start_time}]process dm[${topic}] failed"
                exit 1
            fi
            break
        fi
    done

    exit 0
else
    touch ${md5_check_path}/${sub_year}/${sub_month}/.done_${topic}_${start_time}.md5
fi