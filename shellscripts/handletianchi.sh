ls -t results/Fio/ | head -n 4
file=`ls -t results/Fio/ |  awk "NR==$1"`
echo $file

cp results/Fio/$file ./
./handle.sh $file $file  | grep Warn

#cat data.csv | awk '{print $2}'
#cat data.csv | awk '{print $3}'
cat data.csv 
