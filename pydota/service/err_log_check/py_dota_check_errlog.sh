#!/bin/sh
# 从raw数据中计算各个平台一天总VV数据
# py_dota_report_total.sh 20151007

#设置bearychat发送目标为dota-内部日报
export BEARYCHAT_WEBHOOK="https://hook.bearychat.com/=bw7by/incoming/1d2c96785da623e3299c1d742c4a26fb"

if [ $# -ge 1 ];then
    start_time=$1
else
    start_time=`date -d yesterday +%Y%m%d`
fi

if [ -n "$2" ];then
    topics=("$2")
else
    topics=("mpp_vv_pcweb mpp_vv_mobile mpp_vv_mobile_new_version mpp_vv_pcclient mpp_vv_padweb mpp_vv_ott ott_vv_41 ott_vv_44 \
mpp_vv_mobile_211_20151012 ott_vv_311_20151012 mpp_vv_win10client_511_20151030 macclient_vv_811_20151210 pcweb_1110_20151223 \
mobile_pv pcweb_pv ott_pv msite_pv iphone_pvs aphone_pvs mac_pv mgliveaphone_vodplay mgliveaphone_auplay mgliveaphone_rmplay \
mgliveiphone_vodplay mgliveiphone_auplay mgliveiphone_rmplay dau_ott dau_ott_44 dau_ott_340 dau_ott_3111 dau_ott_41")
fi

# 10.27.103.103＝54.222.137.93 云谷使用外网IP
aws_hosts="54.222.137.93"
topics_aws=("aphone_pvs iphone_pvs mac_pv mgliveaphone_vodplay mgliveaphone_auplay mgliveaphone_rmplay mgliveiphone_vodplay mgliveiphone_auplay mgliveiphone_rmplay")

sub_path_year=${start_time:0:4}
sub_path_month=${start_time:4:2}
sub_path_day=${start_time:6:2}

sub_path=${sub_path_year}/${sub_path_month}
work_path="/home/dota/pydota_v2/pydota"
pydota_des="/home/dota/data/des"
pydota_orig="/home/dota/data/orig"
pydota_errreport="/home/dota/data/errcount"
bearychat="/home/dota/pydota/pydota/bin/bearychat.sh"

mkdir -p ${pydota_errreport}/${sub_path} 2>/dev/null

cd ${work_path}

function errlog_check(){

    proctime=`date "+%Y/%m/%d %H:%M:%S"`

    # 从aws copy des日志到5.4机器进行计算
    for aws_host in ${aws_hosts};
    do
        for topic_aws in ${topics_aws};
        do
            filename_tmp=err_${start_time}*${topic_aws}*
            scp -l 2000000 dota@${aws_host}:${pydota_des}/${sub_path}/${filename_tmp} ${pydota_des}/${sub_path}/
        done
    done

    for topic in ${topics};
    do
        echo "[${proctime}]start check ${topic}"

        filenameraw=err_${start_time}*${topic}_${start_time:0:4}*

        files_des=(`ls ${pydota_des}/${sub_path}/${filenameraw}`)
        files_orig=(`ls ${pydota_orig}/${sub_path}/${filenameraw}`)

        if [[ ${#files_des[@]} -ge 1 || ${#files_orig[@]} -ge 1 ]];then

            cat ${files_des[@]} ${files_orig[@]} | awk -F, '{print $1}'|sort|uniq -c|awk -v start_time=${start_time} -v topic=${topic} '
            {total_num=total_num+$1;
             print start_time","topic","$2","$1}
            END{
                print start_time","topic",total,"total_num
            }'>${pydota_errreport}/${sub_path}/dota_day_${start_time}_${topic}.csv

        fi

        proctime=`date "+%Y/%m/%d %H:%M:%S"`
        echo "[${proctime}]end check ${topic}"

    done

}

#function check_errlog(){
#
#    proctime=`date "+%Y/%m/%d %H:%M:%S"`
#
#    for topic in ${topics};
#    do
#
#        filenameraw=err_${start_time}*${topic}*
#
#        files_des=(`ls ${pydota_des}/${sub_path}/${filenameraw}`)
#        files_orig=(`ls ${pydota_orig}/${sub_path}/${filenameraw}`)
#
#        if [[ ${#files_des[@]} -ge 1 || ${#files_orig[@]} -ge 1 ]];then
#
#            cat ${files_des[@]} ${files_orig[@]} | awk -F, '{print $1}'|sort|uniq -c|awk -v start_time=${start_time} -v topic=${topic} 'BEGIN{
#            print "date "start_time}
#            {total_num=total_num+$1;
#             res[$2]=$1}
#            END{
#                print topic" "total_num
#                for(key in res){
#                print key" "res[key]}
#            }'|
#            awk '{for(i=1;i<=NF;i++){
#                    a[FNR,i]=$i}
#            }
#            END{
#                for(i=1;i<=NF;i++){
#                    for(j=1;j<=FNR;j++){printf a[j,i]","};
#                    print ""
#                }
#            }'>${pydota_errreport}/${sub_path}/dota_day_${start_time}_${topic}.csv
#
##            nowtime=`date "+%Y/%m/%d %H:%M:%S"`
##            msg="${msg}
##            ${proctime}-${nowtime}@许国栋"
##            echo "${msg}" | ${bearychat} -t "10.100.5.4:${start_time}的各个端总vv" -a "#ffa500"
#
#        fi
#    done
#}

errlog_check