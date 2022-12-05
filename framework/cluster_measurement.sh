SYSTEM_PATH=$PWD
# CRAWLER_PATH=$PWD"/Crawler"
# DOWLOADER_PATH=$PWD"/Downloader"
# EXTRACTOR_PATH=$PWD"/Extractor"
# ANALYZER_PATH=$PWD"/Analyzer"
# W_NUM="$1"
LOADER_PATH=$PWD"/Reader"
DOWLOADER_PATH=$PWD"/Downloader"

echo "System: start"

# cat /dev/null > $DOWLOADER_PATH/pull_done.txt
# cat /dev/null > $DOWLOADER_PATH/lpy_download_done.txt
# cat /dev/null > $EXTRACTOR_PATH/lpy_extract_done.txt
# cat /dev/null > $EXTRACTOR_PATH/extract_done.txt
# cat /dev/null > $ANALYZER_PATH/analyze_done.txt
# cat /dev/null > $ANALYZER_PATH/md5_done.txt
cat /dev/null > $LOADER_PATH/finish.txt

# 读取配置文件（架构特征）
cd $LOADER_PATH
cat /dev/null > success_list
cat /dev/null > fail_list
cat /dev/null > finish
python3 loader_1.py
echo finish > finish

# 下载公开镜像
cd $DOWLOADER_PATH
echo $PWD
# while true
# do
# 	# echo "Dowloader: Waiting for Crawler ..."
# 	# sleep 15
# 	loader_finish=`cat $LOADER_PATH/finish.txt`
# 	if [ "$loader_finish" = "finish" ];then
# 		echo "finish" > finish.txt
# 	else
# 		echo "unfinish" > finish.txt
# 	fi
	
#     # $SYSTEM_PATH/keywords.txt 
# 	while read keyword
# 	do
#         # 检查FILE是否存在并且其大小大于零(表示它不为空)。 
# 		if [ -s "$CRAWLER_PATH/$keyword.txt" ];then 
# 			echo "Continue" > finish.txt
# 		    # $CRAWLER_PATH/$keyword.txt 
# 			while read name
# 			do
#                 # -n 或 --line-number : 在显示符合样式的那一行之前，标示出该行的列数编号。
# 				LINE=`grep -n $name pull_done.txt`

# 				#echo $LINE

# 				if [ -z "$LINE" ];then
# 					echo "Dowloader: pulling... $name"
# 					./pull.sh $name $keyword
# 					echo $name >> $DOWLOADER_PATH/pull_done.txt

# 				elif [ -n "$LINE" ];then
# 					FLAG=0
# 					for OLD_KEY in $(echo $LINE|tr "," "\n"); do
# 						OLD_KEY=${OLD_KEY#*:}
# 				#		echo $OLD_KEY
# 						if [ "$name" == "$OLD_KEY" ];then
# 							let FLAG+=1
# 							break
# 						fi
# 					done
					
# 				#	echo $FLAG
					
# 					if [ "$FLAG" -gt "0" ];then
# 						echo Downloader: $name is pulling
# 					else
# 						echo "Dowloader: pulling... $name"
# 						./pull.sh $name $keyword
# 						echo $name >> $DOWLOADER_PATH/pull_done.txt
# 					fi
# 				fi
# 			done < $CRAWLER_PATH/$keyword.txt 

# 			while read done_name
# 			do
# 				sed "\|$done_name|d" $CRAWLER_PATH/$keyword.txt > $CRAWLER_PATH/$keyword.txt
# 			done < $DOWLOADER_PATH/pull_done.txt
# 		elif [ -f "$CRAWLER_PATH/$keyword.txt" ];then 
# 			rm $CRAWLER_PATH/$keyword.txt
# 		fi		
# 	done < $SYSTEM_PATH/keywords.txt 

# 	finish=`cat finish.txt`
# 	echo "Downloader $finish"
# 	if [ "$finish" = "finish" ];then
# 		break
# 	fi
# done &
# 搭建自定义镜像

# 扫描镜像漏洞

# 提取漏洞特征（漏洞特征）

# 评估集群漏洞
