# KEY image:tag
KEY=$1
# KEYWORD=$2

# LINE=`grep -n $KEY lpy_download_done.txt`
LINE=`grep -n $KEY download_done.txt`
# -n 或 --line-number : 在显示符合样式的那一行之前，标示出该行的列数编号
#echo $LINE

# -z 字符串	字符串的长度为零
if [ -z "$LINE" ];then
# 没有这个镜像
	echo Downloader: $KEY is new
#	sudo docker pull $KEY
	docker pull $KEY 2>pull.res
# 希望 stderr 重定向到 pull.res 拉取失败的结果
# -s 判断对象是否存在，并且长度不为0
	if [ ! -s pull.res ];then
	# 镜像拉取成功
      echo Downloader: $KEY pull done
			echo $KEY >> download_done.txt
			# echo $KEY >> download_done_$KEYWORD.txt
	else
      echo Downloader: $KEY pull fail
			RES=`cat pull.res`
			echo Downloader: $RES
			echo $RES >> pull_fail_list.txt
	fi
fi
# # -n 字符串	字符串的长度不为零
# elif [ -n "$LINE" ];then
# 	FLAG=0
# 	# -t 字符替换 (一般缺省为-t)
# 	for OLD_KEY in $(echo $LINE|tr "," "\n"); 
# 	do
# 		# 使用 # 号截取右边字符
# 		OLD_KEY=${OLD_KEY#*:}
# 		# 取完后为tag
# #		echo $OLD_KEY
# 		if [ "$KEY" == "$OLD_KEY" ];then
# 			let FLAG+=1
# 			break
# 		fi
# 	done
	
# #	echo $FLAG
	
# 	if [ "$FLAG" -gt "0" ];then
# 		echo Downloader: $KEY already exists
# 	else
# 		echo Downloader: $KEY is new
# 		sudo docker pull $KEY 2>pull.res

#     if [ ! -s pull.res ];then
#         echo Downloader: $KEY pull done
#         echo $KEY >> lpy_download_done.txt
# 				# echo $KEY >> download_done_$KEYWORD.txt
#     else
#         echo Downloader: $KEY pull fail
#         RES=`cat pull.res`
# 				echo Downloader: $RES
#         echo $RES >> pull_fail_list.txt
#     fi
# 	fi
# fi
