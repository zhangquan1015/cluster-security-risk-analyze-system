while read line 
do
    echo 2
    # echo $line
done < ./aaa &

while read line 
do
    echo 1
    # echo $line
done < ./aaa

while read line 
do
    echo 3
    # echo $line
done < ./aaa 
