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
pydota_report="/home/dota/data/dailyreport"
pydota_des="/home/dota/data/des"
bearychat="${work_path}/bin/bearychat.sh"
pydota_nfs="/data/nfs/dota/"
py_dota_process_user="gibbsxu@10.100.1.141"

cd ${work_path}

function report_vv(){
    sub_topic=$1
    topic_num=$2
    # 全天运行，逐小时合并各个topic数据
    echo "DATE,TIME,CID,PLID,VID,PT,LN,CLIENTTP,CLIENTVER,VV" >${pydota_report}/${sub_path}/${start_time}_vv_${clienttype}_vid.csv
    rm ${pydota_report}/${sub_path}/.${start_time}_vv_${clienttype}_vid.done

    # 每个小时的des的.done是否都生成，有一个小时没生成，则置为1，表示数据不完整。
    all_done_file=0

    for i in {0..23}
    do
        cur_time=`date --date="$start_time $i hour" +%Y%m%d%H`

        des_done_file=${pydota_des}/${sub_path}/.${cur_time}_playrawdata.done
        if [ ! -f ${des_done_file} ];then
            all_done_file=1
        fi

        filename=${cur_time}*${sub_topic}*

        # 某一个小时时，只有所有相关topic的文件
        files=(`ls ${pydota_des}/${sub_path}/${filename}|grep -v "live\|pvrawdata\|daurawdata"`)

        if [[ ${#files[@]} -eq 0 ]];then
            continue
        fi

        cat ${files[@]} | awk -F, -v clienttype=${clienttype} '{ if($21=="play" && $22==clienttype && ($17==0 || $17==3))
        {print $1","substr($2,1,2)","$11","$12","$13","$17","$18","$22","$23} }' \
        | sort | uniq -c | sort -rn |awk '{print $2","$1}' \
        >> ${pydota_report}/${sub_path}/${start_time}_vv_${clienttype}_vid.csv

    # for
    done

    sudo cp ${pydota_report}/${sub_path}/${start_time}_vv_${clienttype}_vid.csv ${pydota_nfs}/${sub_path}/${start_time}_vv_${clienttype}_vid.csv

    if [ ${all_done_file} -eq 0 ];then
        touch ${pydota_report}/${sub_path}/.${start_time}_vv_${clienttype}_vid.done
        sudo cp ${pydota_report}/${sub_path}/.${start_time}_vv_${clienttype}_vid.done ${pydota_nfs}/${sub_path}/
    else
        localhost=`LC_ALL=C /sbin/ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'`
        mess="所在机器:${localhost} ${clienttype}
        vid .done 文件生成受影响
        @许国栋"
        curl -X POST --data-urlencode "payload={\"text\":\"${mess}\"}" ${BEARYCHAT_WEBHOOK}
    fi

    exit 0
}

if [ -n "$1" ]; then
  clienttype=$1
  if [ x"${clienttype}" == "xpcweb" ];then
    report_vv pcweb_1110 1
  elif [ x"${clienttype}" == "xipad" ];then
    report_vv mobile 3
  elif [ x"${clienttype}" == "xapad" ];then
    report_vv mobile 3
  elif [ x"${clienttype}" == "xiphone" ];then
    report_vv mobile 3
  elif [ x"${clienttype}" == "xphonem" ];then
    report_vv phonem 1
  elif [ x"${clienttype}" == "xandroid" ];then
    report_vv mobile 3
  elif [ x"${clienttype}" == "xott" ];then
    report_vv ott 4
  elif [ x"${clienttype}" == "xpcclient" ];then
    report_vv pcclient 1
  elif [ x"${clienttype}" == "xpadweb" ];then
    report_vv padweb 1
  elif [ x"${clienttype}" == "xwin10client" ];then
    report_vv win10client 1
  elif [ x"${clienttype}" == "xmacclient" ];then
    report_vv macclient 2
  else
    exit -1
  fi
else
  clienttype="phonem"
  report_vv msite 1
fi
