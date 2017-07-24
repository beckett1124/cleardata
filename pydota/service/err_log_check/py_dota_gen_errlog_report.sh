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

topics=("mpp_vv_pcweb mpp_vv_mobile mpp_vv_mobile_new_version mpp_vv_pcclient mpp_vv_padweb mpp_vv_ott ott_vv_41 ott_vv_44 mpp_vv_mobile_211_20151012 ott_vv_311_20151012 mpp_vv_win10client_511_20151030 macclient_vv_811_20151210 pcweb_1110_20151223")
topics_pv=("pcweb_pv mobile_pv ott_pv msite_pv iphone_pvs mac_pv aphone_pvs")
topics_mglive=("mgliveaphone_vodplay mgliveaphone_auplay mgliveaphone_rmplay mgliveiphone_vodplay mgliveiphone_auplay mgliveiphone_rmplay")
topics_dau=("dau_ott dau_ott_44 dau_ott_340 dau_ott_3111 dau_ott_41")

sub_path_year=${start_time:0:4}
sub_path_month=${start_time:4:2}
sub_path_day=${start_time:6:2}

sub_path=${sub_path_year}/${sub_path_month}
work_path="/home/dota/pydota_v2/pydota"
pydota_des="/home/dota/data/des"
pydota_orig="/home/dota/data/orig"
pydota_errreport="/home/dota/data/errcount"
bearychat="/home/dota/pydota/pydota/bin/bearychat.sh"


index_file=${pydota_errreport}/${sub_path}/index_${start_time}


mkdir -p ${pydota_errreport}/${sub_path} 2>/dev/null

cd ${work_path}

function gen_report(){
    if [ -n "$1" ];then
        topic=$1
    else
        echo "uninput topic name"
        exit 1
    fi

    nfs_report_path=$2

    err_files=()

    for((day=29;day>=0;day--));
    do
        start_time_tmp=`date -d "${day} day ago ${start_time}" +%Y%m%d`
        err_files_tmp=(`ls ${pydota_errreport}/${start_time_tmp:0:4}/${start_time_tmp:4:2}/dota_day_${start_time_tmp}_${topic}.csv`)
        if [[ ${#err_files_tmp[@]} -ge 1 ]];then
            err_files=(${err_files[@]} ${err_files_tmp[@]})
        fi
    done

    if [[ ${#err_files[@]} -ge 1 ]];then
        cat ${err_files[@]} | awk -F, -v topic=${topic} '{
        if(!($3 in errtag)){
            errtag[$3]=1}
        if(!($1 in errtag)){
            time[$1]=1}
        type=$1"_"$3;
        num[type]=$NF
        }
        END{
            title="date,"topic",";
            for(tag in errtag){
                if(tag!="total"){
                    title=title""tag","}
            }
            print title
            for(date in time){
                prefix=date","
                record=""
                for(tag in errtag){
                    key=date"_"tag
                    if(tag=="total"){
                        prefix=prefix""num[key]",";
                        continue}
                    if(num[key]==""){
                        record=record"0,"
                    }
                    else{
                        record=record""num[key]","}
                }
                print prefix""record
            }
        }' |sort -t',' -k1,1n >${pydota_errreport}/${sub_path}/dota_${start_time}_${topic}.csv

        # cp到nfs目录。供页面展示
        sudo cp ${pydota_errreport}/${sub_path}/dota_${start_time}_${topic}.csv ${nfs_report_path}
    fi
}

function gen_total_report(){
    platform=$1

    echo "date" > ${index_file}

    for((day=29;day>=0;day--));
    do
        start_time_tmp=`date -d "${day} day ago ${start_time}" +%Y%m%d`
        echo ${start_time_tmp} >> ${index_file}
    done

    if [[ ${platform} == "pv" ]];then
        topics_tmp=${topics_pv}
        nfs_report_path="/data/nfs/errcount/pv/"
        report_file=${pydota_errreport}/${sub_path}/dota_${start_time}_pv_total.csv
        rm ${report_file} 2>/dev/null
    elif [[ ${platform} == "mglive" ]];then
        topics_tmp=${topics_mglive}
        nfs_report_path="/data/nfs/errcount/mglive/"
        report_file=${pydota_errreport}/${sub_path}/dota_${start_time}_mglive_total.csv
        rm ${report_file} 2>/dev/null
    elif [[ ${platform} == "dau" ]];then
        topics_tmp=${topics_dau}
        nfs_report_path="/data/nfs/errcount/dau/"
        report_file=${pydota_errreport}/${sub_path}/dota_${start_time}_dau_total.csv
        rm ${report_file} 2>/dev/null
    else
        topics_tmp=${topics}
        nfs_report_path="/data/nfs/errcount/"
        report_file=${pydota_errreport}/${sub_path}/dota_${start_time}_total.csv
        rm ${report_file} 2>/dev/null
    fi

    for topic in ${topics_tmp};
    do
        if [ -f ${report_file} ];then
            col_num=`head -n 1 ${report_file}|awk -F, '{print NF}'`
            out_col=""
            for((i=1;i<=${col_num};i++));do
                out_col="${out_col} 1.${i}"
            done

            echo ${out_col}

            if [ "${out_col}" == "" ];then
                echo "File [${report_file}] col_num[${col_num}] is wrong"
            else
                if [ -f ${pydota_errreport}/${sub_path}/dota_${start_time}_${topic}.csv ];then
                    join -t $',' -a 1 -e 0 -o ${out_col} 2.2 ${report_file} ${pydota_errreport}/${sub_path}/dota_${start_time}_${topic}.csv > ${report_file}_tmp
                    mv ${report_file}_tmp ${report_file}
                fi
            fi
        else
            if [ -f ${pydota_errreport}/${sub_path}/dota_${start_time}_${topic}.csv ];then
                join -t $',' -a 1 -e 0 -o 1.1 -o 2.2 ${index_file} ${pydota_errreport}/${sub_path}/dota_${start_time}_${topic}.csv > ${report_file}
            fi
        fi
    done

    # cp到nfs目录。供页面展示
    sudo cp ${report_file} ${nfs_report_path}

}


function run_report(){
    platform=$1

    if [[ ${platform} == "pv" ]];then
        topics_tmp=${topics_pv}
        nfs_report_path="/data/nfs/errcount/pv/"
    elif [[ ${platform} == "mglive" ]];then
        topics_tmp=${topics_mglive}
        nfs_report_path="/data/nfs/errcount/mglive/"
    elif [[ ${platform} == "dau" ]];then
        topics_tmp=${topics_dau}
        nfs_report_path="/data/nfs/errcount/dau/"
    else
        topics_tmp=${topics}
        nfs_report_path="/data/nfs/errcount/"
    fi

    for topic in ${topics_tmp};
    do
        proctime=`date "+%Y/%m/%d %H:%M:%S"`
        echo "[${proctime}]start gen_report ${topic}"

        gen_report ${topic} ${nfs_report_path}

        proctime=`date "+%Y/%m/%d %H:%M:%S"`
        echo "[${proctime}]end gen_report ${topic}"

    done

}

run_report play
gen_total_report play

run_report pv
gen_total_report pv

run_report mglive
gen_total_report mglive

run_report dau
gen_total_report dau
