#!/bin/bash
# SYSTEM_PATH=$PWD
cd ..
LOADER_PATH=$PWD"/Loader"

echo "准备进行环境感知"
cd $LOADER_PATH
cat /dev/null > success_list
cat /dev/null > fail_list
cat /dev/null > finish
python3 loader_1.py
echo finish > finish 