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
pydota_des="/home/dota/data/des"
pydota_report="/home/dota/data/dailyreport"
bearychat="/home/dota/pydota_v2/pydota/bin/bearychat.sh"

localhost=`LC_ALL=C /sbin/ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | head -n 1 | awk '{ print $1}'`

mkdir -p ${pydota_report}/${sub_path} 2>/dev/null

cd ${work_path}

function report_uv_total(){

    proctime=`date "+%Y/%m/%d %H:%M:%S"`

    filenameraw=${start_time}*
    report_filie=day_uv_total_${start_time}.csv

    files=`ls ${pydota_des}/${sub_path}/${filenameraw}  | grep -v "live\|pvrawdata\|mpp_vv_pcweb"`
    #files=`ls ${pydota_des}/${sub_path}/${filenameraw} ${pydota_des}/${sub_path_nextday}/${filenamenext}`

    cat ${files} | awk -F, '{
    if($21=="play" && $17==0){
      print $1","$16","$22}
    }' | sort | uniq | awk -F, '{
    type=$1","$3;
    if(!(type in sum)){
      sum[type]=0};
      sum[type]=sum[type]+1
    }
    END{
      for(i in sum){
        print i","sum[i]
      }
    }' | sort -n \
    > ${pydota_report}/${sub_path}/${report_filie}

    cat ${pydota_report}/${sub_path}/${report_filie} | awk -F, '{
    type=$1",总计";
    if(!(type in sum)){
      sum[type]=0};
      sum[type]=sum[type]+$NF
    }
    END{
      for(i in sum) {
        print i","sum[i]
      }
    }' >>${pydota_report}/${sub_path}/${report_filie}

    sed -i '1i\日期,平台,uv'  ${pydota_report}/${sub_path}/${report_filie}

    topmsg=`cat ${pydota_report}/${sub_path}/${report_filie}`
    report_size=`ls -lh ${pydota_report}/${sub_path}/${report_filie} | awk '{print $5}'`

    msg="report_size大小${report_size}
${topmsg}"
nowtime=`date "+%Y/%m/%d %H:%M:%S"`
msg="${msg}
${proctime}-${nowtime}@许国栋"
echo "${msg}" | ${bearychat} -t "10.100.5.4:${start_time}的各个端点播uv" -a "#ffa500"
}

function report_lixian_uv_total(){

    proctime=`date "+%Y/%m/%d %H:%M:%S"`

    filenameraw=${start_time}*
    lixian_report_uv_file=day_lixian_uv_total_${start_time}.csv

    files=`ls ${pydota_des}/${sub_path}/${filenameraw}  | grep -v "live\|pvrawdata\|pcweb_1110"`
    #files=`ls ${pydota_des}/${sub_path}/${filenameraw} ${pydota_des}/${sub_path_nextday}/${filenamenext}`

    cat ${files} | awk -F, '{
    if($21=="play" && $17==3){
      print $1","$16","$22}
    }' | sort | uniq | awk -F, '{
    type=$1","$3;
    if(!(type in sum)){
      sum[type]=0};
      sum[type]=sum[type]+1
    }
    END{
      for(i in sum){
        print i","sum[i]
      }
    }' | sort -n \
    > ${pydota_report}/${sub_path}/${lixian_report_uv_file}

    cat ${pydota_report}/${sub_path}/${lixian_report_uv_file} | awk -F, '{
    type=$1",总计";
    if(!(type in sum)){
      sum[type]=0};
      sum[type]=sum[type]+$NF
    }
    END{
      for(i in sum) {
        print i","sum[i]
      }
    }' >>${pydota_report}/${sub_path}/${lixian_report_uv_file}

    sed -i '1i\日期,平台,uv'  ${pydota_report}/${sub_path}/${lixian_report_uv_file}

    topmsg=`cat ${pydota_report}/${sub_path}/${lixian_report_uv_file}`
    report_size=`ls -lh ${pydota_report}/${sub_path}/${lixian_report_uv_file} | awk '{print $5}'`

    msg="report_size大小${report_size}
${topmsg}"
nowtime=`date "+%Y/%m/%d %H:%M:%S"`
msg="${msg}
${proctime}-${nowtime}@许国栋"
echo "${msg}" | ${bearychat} -t "${localhost}:${start_time}的各个端离线播放uv" -a "#ffa500"
}

report_uv_total
report_lixian_uv_total