#!/bin/bash

cd ..
LOADER_PATH=$PWD"/Loader"
SCANNER_PATH=$PWD"/Scanner"

echo  "准备扫描镜像漏洞"
# 扫描镜像漏洞
cd $SCANNER_PATH
if [ ! -d vulns_list ];then
  mkdir vulns_list
fi
cat /dev/null > image_list

ls $LOADER_PATH/image | while read line
do
# 判断不为空
  if [ -s $LOADER_PATH/image/$line ]
  then
      while read name
      do
        # echo $name
        ./scanner.sh $name
      done < $LOADER_PATH/image/$line
  fi
done