#!/bin/sh
# 从raw数据中计算各个平台一天总uv数据
# py_dota_report_total.sh 20160107

#设置bearychat发送目标为dota-内部日报
export BEARYCHAT_WEBHOOK="https://hook.bearychat.com/=bw7by/incoming/1d2c96785da623e3299c1d742c4a26fb"

if [ $# -ge 1 ];then
    start_time=$1
else
    start_time=`date -d yesterday +%Y%m%d`
fi
sub_path_year=${start_time:0:4}
sub_path_month=${start_time:4:2}
sub_path_day=${start_time:6:2}
sub_path_hour=${start_time:8:2}


sub_path=${sub_path_year}/${sub_path_month}
work_path="/home/dota/pydota_v2/pydota"
pydota_report="/home/dota/data/dailyreport"
pv_uv_tmp="/home/dota/data/pv_uv_tmp"

bearychat="/home/dota/pydota_v2/pydota/bin/bearychat.sh"

localhost=`LC_ALL=C /sbin/ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | head -n 1 | awk '{ print $1}'`

mkdir -p ${pydota_report}/${sub_path} 2>/dev/null
mkdir -p ${pv_uv_tmp}/${sub_path} 2>/dev/null

cd ${work_path}


function report_week_pv_uv_total(){
    proctime=`date "+%Y/%m/%d %H:%M:%S"`

    report_week_file=${start_time}_week_pv_uv.csv

    for((day=6;day>=0;day--));
    do
        start_time_tmp=`date -d "${day} day ago ${start_time}" +%Y%m%d`
        pv_cookie_file=${start_time_tmp}_pv_cookie.csv
        pv_cookie_file_tmp=(`ls ${pv_uv_tmp}/${start_time_tmp:0:4}/${start_time_tmp:4:2}/${pv_cookie_file}`)
        if [[ ${#pv_cookie_file_tmp[@]} -ge 1 ]];then
            pv_files=(${pv_files[@]} ${pv_cookie_file_tmp[@]})
        fi
    done

    if [[ ${#pv_files[@]} -ge 1 ]];then
        cat ${pv_files[@]} | awk -F, '{if(NF==4){print $2","$3}}'|sort | uniq | awk -F, '{print $2}' \
        |sort |uniq -c | awk -v time=${start_time} '{print time","$2","$1}' \
        > ${pydota_report}/${sub_path}/${report_week_file}

        cat ${pydota_report}/${sub_path}/${report_week_file} | awk -F, '{
        type=$1",总计";
        if(!(type in sum)){
            sum[type]=0};
        sum[type]=sum[type]+$NF
        }
        END{
            for(i in sum) {
                print i","sum[i]
            }
        }' >>${pydota_report}/${sub_path}/${report_week_file}

        sed -i '1i\日期,平台,uv'  ${pydota_report}/${sub_path}/${report_week_file}

        topmsg=`cat ${pydota_report}/${sub_path}/${report_week_file}`
        report_size=`ls -lh ${pydota_report}/${sub_path}/${report_week_file} | awk '{print $5}'`

        msg="report_size大小${report_size}
${topmsg}"
        nowtime=`date "+%Y/%m/%d %H:%M:%S"`
        msg="${msg}
${proctime}-${nowtime}@许国栋"
        echo "${msg}" | ${bearychat} -t "10.100.5.4:${start_time}该周各个端pv的uv" -a "#ffa500"

    fi
}


report_week_pv_uv_total