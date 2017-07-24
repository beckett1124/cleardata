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

all_play_topics=("mpp_vv_msite  mpp_vv_macclient_121_20151028 mpp_vv_pcweb mpp_vv_mobile mpp_vv_mobile_new_version mpp_vv_pcclient mpp_vv_padweb mpp_vv_ott ott_vv_41 ott_vv_44 mpp_vv_mobile_211_20151012 ott_vv_311_20151012 mpp_vv_win10client_511_20151030 macclient_vv_811_20151210 pcweb_1110_20151223 phonem_vod_4110_20160317")
all_live_topics=("macclient_live_8111_20160105 mobile_live_2011_20151105 mobile_live_2111_20151225 rt_live_pcweb mobile_live_2111_20151225_aws")
all_pv_topics=("mobile_pv pcweb_pv ott_pv msite_pv")
all_pvs_topics=("iphone_pvs")

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

    if [ ${sub_type} == "play" ];then
        plat="vv"
        topics=(${all_play_topics[@]} ${all_live_topics[@]})
    elif [ ${sub_type} == "pv" ];then
        plat="pv"
        topics=(${all_pv_topics[@]})
    else
        echo "wrong platform!"
        exit -1
    fi

    for i in {0..23}
    do
        cur_time=`date --date="$start_time $i hour" +%Y%m%d%H`

        nowtime_s=`date "+%Y/%m/%d %H:%M:%S"`
        echo "start sync ${cur_time}"

        for topic in ${topics[*]}
        do
            echo "start sync ${topic}"

            filename=${cur_time}*${topic}*
            err_filename=err_${cur_time}*${topic}*

            cd ${pydota_orig}/${sub_path}

            # 某一个小时时，只有所有相关topic的文件
            files=(`ls ${filename}`)
            err_files=(`ls ${err_filename}`)

            if [ ${#files[@]} -ge 1 ];then

                aws s3 sync . ${pydota_s3_orig}/${plat}/${sub_path_year}/${sub_path_month}/${sub_path_day}/${cur_time:8:2}/ --exclude "*" --include "${filename}"
            fi

            if [ ${#err_files[@]} -ge 1 ];then
                aws s3 sync . ${pydota_s3_orig}/${plat}/${sub_path_year}/${sub_path_month}/${sub_path_day}/${cur_time:8:2}/ --exclude "*" --include "${err_filename}"
            fi

            echo "end sync ${topic}"

        done

        nowtime_e=`date "+%Y/%m/%d %H:%M:%S"`
        echo "end sync ${cur_time}"

        echo "sync time: ${nowtime_s} to ${nowtime_e}"


    # for
    done


    exit 0
}

if [ -n "$1" ]; then
  sync_to_s3 $1
else
  sync_to_s3 play
fi
