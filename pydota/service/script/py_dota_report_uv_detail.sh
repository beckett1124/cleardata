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
work_path="/home/dota/pydota/pydota"
pydota_des="/home/dota/data/des"
pydota_report="/home/dota/data/dailyreport"
bearychat="/home/dota/pydota/pydota/bin/bearychat.sh"

mkdir -p ${pydota_report}/${sub_path} 2>/dev/null

cd ${work_path}

function report_uv_detail(){

    proctime=`date "+%Y/%m/%d %H:%M:%S"`

    topic=$1

    filenameraw=${start_time}*${topic}*

    files=`ls ${pydota_des}/${sub_path}/${filenameraw}  | grep -v "live\|pvrawdata"`
    #files=`ls ${pydota_des}/${sub_path}/${filenameraw} ${pydota_des}/${sub_path_nextday}/${filenamenext}`

    cat ${files} | awk -F, '{
    if($21=="play" && $17==0){
      print $1","$16","$17","$22","$23}
    }' | sort | uniq | awk -F, '{
    type=$1","$3","$4","$5;
    if(!(type in sum)){
      sum[type]=0};
      sum[type]=sum[type]+1
    }
    END{
      for(i in sum){
        print i","sum[i]
      }
    }' | sort -n \
    > ${pydota_report}/${sub_path}/${start_time}_${topic}_version_uv.csv

    sed -i '1i\日期,播放种类,平台,版本,uv'  ${pydota_report}/${sub_path}/${start_time}_${topic}_version_uv.csv

#    topmsg=`cat ${pydota_report}/${sub_path}/${start_time}_${topic}_version_uv.csv`
#    report_size=`ls -lh ${pydota_report}/${sub_path}/${start_time}_${topic}_version_uv.csv | awk '{print $5}'`
#
#    msg="report_size大小${report_size}
#${topmsg}"
#nowtime=`date "+%Y/%m/%d %H:%M:%S"`
#msg="${msg}
#${proctime}-${nowtime}@许国栋"
#echo "${msg}" | ${bearychat} -t "OTT:10.100.5.4:${start_time}的各版本uv" -a "#ffa500"
}
report_uv_detail ott