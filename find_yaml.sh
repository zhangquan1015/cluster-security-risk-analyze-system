# 把 $1 路径下所有compose.yaml转移到./database 路径下
# $1 database
files="tmp.txt"
find $1 | grep yaml > $files
while read line
do 
    name=${line//// }
    arr=($name)
    newfile=${arr[-2]}"_"${arr[-1]}
    # echo $newfile
    cp $line ./database/$newfile
    
done < $files

rm $files