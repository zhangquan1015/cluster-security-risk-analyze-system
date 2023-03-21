#!/bin/bash

# 定义要扫描的镜像名称和版本
input=$1
if [[ "$input" == *:* ]]; then
  image_name="${input%%:*}"
  image_version="${input#*:}"
else
  image_name="$input"
  image_version="latest"
fi

# 要储存的信息位置
scan_list="./image_list"
result="./vulns_list/${image_name}_${image_version}.csv"

# 运行grype扫描并提取CVE ID
if [ ! -f "${result}" ]; then
  echo "扫描 ${image_name}:${image_version}"
  grype_result=$(grype -q ${image_name}:${image_version} -o template -t ./csv.tmpl)
  echo "${grype_result}" > "${result}"
fi
# 保存扫描过的镜像
echo "CVE IDs found in ${image_name}:${image_version}:"
echo "${image_name}:${image_version}" >> "${scan_list}"
