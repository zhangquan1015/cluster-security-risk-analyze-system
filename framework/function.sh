#!/bin/bash  

SYSTEM_PATH=$PWD

LOADER_PATH=$PWD"/Loader"
DOWLOADER_PATH=$PWD"/Downloader"
BUILDER_PATH=$PWD"/Builder"
SCANNER_PATH=$PWD"/Scanner"
EXTRACTER_PATH=$PWD"/Extracter"
ESTIMATOR_PATH=$PWD"/Estimator"
EXPORTER_PATH=$PWD"/Exporter"


cat /dev/null > $LOADER_PATH/finish.txt


# 读取配置文件（架构特征）
    # echo "准备进行环境感知"
function_load(){
    cd $LOADER_PATH
    cat /dev/null > success_list
    cat /dev/null > fail_list
    cat /dev/null > finish
    python3 loader_1.py
    echo finish > finish 
}

# 扫描镜像漏洞
    # echo  "准备扫描镜像漏洞"
function_scan(){
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
}

# 提取漏洞特征（漏洞特征）
# echo "准备提取漏洞特征（漏洞特征）"
function_extract(){
    cd $EXTRACTER_PATH
    python3 run.py
}


# 评估集群漏洞
# echo "准备进行集群风险分析"
function_estimate(){
    cd $ESTIMATOR_PATH
    python3 run.py
}

function_begin() {
    if [ "$#" -eq  "0" ];then
        echo "      请选择工作流程      "
        echo "  1----------配置环境感知 "
        echo "  2----------镜像漏洞扫描 "
        echo "  3----------漏洞特征提取 "
        echo "  4----------集群风险分析 "
        echo "  5----------扫描镜像漏洞 "
    fi
    if [[ $1 = 1 ]]; then
        function_load
    fi
    if [[ $1 = 2 ]]; then
        function_scan
    fi
    if [[ $1 = 3 ]]; then
        function_extract
    fi
    if [[ $1 = 4 ]]; then
        function_estimate
    fi
    if [[ $1 = 5 ]]; then
        echo 1
    fi
}

function_begin $1