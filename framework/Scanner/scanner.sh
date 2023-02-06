IMAGE_TAG=$1
# IMAGE_TAG="ubuntu:latest"

image_tag=${IMAGE_TAG//:/_}
# 判断是否有过扫描记录
if [ ! -f ./vulns_list/$image_tag.csv ]; then
    grype $IMAGE_TAG -o template -t ./csv.tmpl > ./vulns_list/$image_tag.csv
fi
echo $IMAGE_TAG >> ./image_list

# docker run --rm anchore/grype:latest $IMAGE_TAG -o template -t ./csv.tmpl > ./vulns_list/$image_tag.csv

