#!/bin/bash
export WORK_PATH=`pwd`
CONF_LOG_FILE="$WORK_PATH/_build_unittest.log"

LOG_FATAL=1
LOG_WARNING=2
LOG_NOTICE=4
LOG_TRACE=8
LOG_DEBUG=16
LOG_LEVEL_TEXT=(
	[1]="FATAL"
	[2]="WARNING"
	[4]="NOTICE"
	[8]="TRACE"
	[16]="DEBUG"
)

TTY_FATAL=1
TTY_PASS=2
TTY_TRACE=4
TTY_INFO=8
TTY_MODE_TEXT=(
	[1]="[FAIL ]"
	[2]="[WARNING ]"
	[4]="[NOTICE]"
	[8]="[TRACE]"
	[16]="[DEBUG]"
)

#0  OFF  
#1  高亮显示  
#4  underline  
#5  闪烁  
#7  反白显示  
#8  不可见 

#30  40  黑色
#31  41  红色  
#32  42  绿色  
#33  43  黄色  
#34  44  蓝色  
#35  45  紫红色  
#36  46  青蓝色  
#37  47  白色 
TTY_MODE_COLOR=(
	[1]="1;31"
	[2]="1;32"
	[4]="0;36"
	[8]="1;33"
	[16]="1;35"
)

##! @BRIEF: print info to tty & log file
##! @IN[int]: $1 => tty mode
##! @IN[string]: $2 => message
##! @RETURN: 0 => sucess; 1 => failure
function Print()
{
	local tty_mode=$1
	local message="$2"
	local time=`date "+%m-%d %H:%M:%S"`
	echo "${LOG_LEVEL_TEXT[$tty_mode]}: $time: * $$ $message" >> ${CONF_LOG_FILE}
	echo -e "\e[${TTY_MODE_COLOR[$tty_mode]}m${TTY_MODE_TEXT[$tty_mode]} ${message}\e[m"
	return $?
}

function execshell()
{
	$@
	[[ $? != 0 ]] && {
		echo "$@失败"
		print_help
		exit 1
	}
	return 0
}

print_help()
{
	echo "samples:"
	echo "-----------------------------------------------------------------------------------"
	echo "sh pydota_env_init.sh"
	echo "-----------------------------------------------------------------------------------"
	return 0
}

function build_pydotaunitenv()
{
	Print ${LOG_NOTICE} "build pydota_unit test env start"
	cd ${WORK_PATH}
	{
		cd ${WORK_PATH}/../
		PROJECT_WORKSPACE=`pwd`
		#生成source_me.sh
		env_file_name="${PROJECT_WORKSPACE}/pydota/source_me.sh"
		echo "export PYTHONPATH=${PROJECT_WORKSPACE}/" > ${env_file_name}
		source ${PROJECT_WORKSPACE}/pydota/source_me.sh
	}
	cd ${WORK_PATH}
	Print ${LOG_NOTICE} "build pydota_unit test env finish."
}


#参数解析，功能调度
Main() 
{
	execshell "build_pydotaunitenv"
}
Main "$@"

