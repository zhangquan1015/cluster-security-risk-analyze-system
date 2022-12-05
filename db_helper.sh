# 把 $1 路径下所有compose.yaml转移到./database 路径下
# $1 database

# grep -r  $1 > $files
SYSTEM_PATH=$PWD
DB_PATH=$PWD"/database"
if [ ! -d $DB_PATH ]; then
    mkdir $DB_PATH
fi

files_all="all.txt"
files_filter="tmp.txt"
# files="tmp.txt"

# PATTERN="[a-z]\.yml$"
PATTERN1="[a-z]\.yml$"
PATTERN2="[a-z]\.yaml$"
PATTERN3="compose"

cat /dev/null > $SYSTEM_PATH/$files_all
find $1 > $SYSTEM_PATH/$files_all
# for line in $(find $1 | grep '.yml$\|.yaml$')
for line in $(cat $SYSTEM_PATH/$files_all)
do
    name=${line##*/}

    if [[ $name =~ $PATTERN1 ]] || [[ $name =~ $PATTERN2 ]];then
        if [[ $name =~ $PATTERN3 ]]; then
            # echo $name  
            name=${line//// }
            arr=($name)
            newfile=${arr[-2]}"_"${arr[-1]}
            # echo $newfile
            cp -r $line $DB_PATH/$newfile
        fi  
    fi
done
# find $1 >  $SYSTEM_PATH/$files_all
# grep compose | grep '.yml$\|.yaml$'  > $SYSTEM_PATH/$files
# while read line
# do 
#     name=${line//// }
#     arr=($name)
#     newfile=${arr[-2]}"_"${arr[-1]}
#     # echo $newfile
#     cp -r $line $DB_PATH/$newfile
    
# done < $SYSTEM_PATH/$files

rm $SYSTEM_PATH/$files_all