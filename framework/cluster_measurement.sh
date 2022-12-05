SYSTEM_PATH=$PWD
# CRAWLER_PATH=$PWD"/Crawler"
# DOWLOADER_PATH=$PWD"/Downloader"
# EXTRACTOR_PATH=$PWD"/Extractor"
# ANALYZER_PATH=$PWD"/Analyzer"
# W_NUM="$1"
LOADER_PATH=$PWD"/Loader"
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
# images=`ls $LOADER_PATH/image | tr ' ' '\n'`
# echo $images
ls $LOADER_PATH/image | while read line
do
  if [ -s $LOADER_PATH/image/$line ]
  then
      while read name
      do
        # echo $line
        # echo $name
         ./pull.sh $name
      done < $LOADER_PATH/image/$line
  fi
done

# 搭建自定义镜像

# 扫描镜像漏洞

# 提取漏洞特征（漏洞特征）

# 评估集群漏洞
