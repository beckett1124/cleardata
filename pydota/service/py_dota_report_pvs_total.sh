#!/bin/sh
# 从raw数据中计算各个平台一天总PVS数据

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
pydota_des="/home/dota/data/des"
pydota_report="/home/dota/data/dailyreport"

s3_report_path="s3://data-pv/dota/report"
bearychat="/home/dota/pydota_v2/pydota/bin/bearychat.sh"

localhost=`LC_ALL=C /sbin/ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | head -n 1 | awk '{ print $1}'`

mkdir -p ${pydota_report}/${sub_path} 2>/dev/null

cd ${work_path}

function report_pvs_total(){

    proctime=`date "+%Y/%m/%d %H:%M:%S"`

    filenameraw=${start_time}*

    files=`ls ${pydota_des}/${sub_path}/${filenameraw}`

    cat ${files} | awk -F, '{
    if($21=="pvs"){
      print $1","substr($2,1,2)","$22}
    }' | sort | uniq -c | awk '{print $2","$1}' | sort -n \
    > ${pydota_report}/${sub_path}/day_pvs_hour_${start_time}.csv

    cat ${pydota_report}/${sub_path}/day_pvs_hour_${start_time}.csv | awk -F, '{
    type=$1","$3;
    if(!(type in sum)){
      sum[type]=0};
      sum[type]=sum[type]+$NF
    }
    END{
      for(i in sum){
        print sum[i]" "i
      }
    }'|awk '{print $2","$1}'>${pydota_report}/${sub_path}/day_pvs_total_${start_time}.csv

    cat ${pydota_report}/${sub_path}/day_pvs_total_${start_time}.csv | awk -F, '{
    type=$1",总计";
    if(!(type in sum)){
      sum[type]=0};
      sum[type]=sum[type]+$NF
    }
    END{
      for(i in sum) {
        print sum[i]" "i
      }
    }'|awk '{print $2","$1}'>>${pydota_report}/${sub_path}/day_pvs_total_${start_time}.csv

    sed -i '1i\日期,平台,pvs'  ${pydota_report}/${sub_path}/day_pvs_total_${start_time}.csv

    aws s3 sync ${pydota_report}/${sub_path}/ ${s3_report_path}/${sub_path} --exclude "*" --include "day_pvs_total_${start_time}.csv"

    topmsg=`cat ${pydota_report}/${sub_path}/day_pvs_total_${start_time}.csv`
    report_size=`ls -lh ${pydota_report}/${sub_path}/day_pvs_total_${start_time}.csv | awk '{print $5}'`

    msg="report_size大小${report_size}
${topmsg}"
nowtime=`date "+%Y/%m/%d %H:%M:%S"`
msg="${msg}
${proctime}-${nowtime}@许国栋"
echo "${msg}" | ${bearychat} -t "${localhost}:${start_time}的各个端总pvs" -a "#ffa500"
}
report_pvs_total