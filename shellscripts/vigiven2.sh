ls -t results/Fio/ | head -n 4
file=`ls -t results/Fio/ | head | awk "NR==$1"`
echo $file

vi results/Fio/$file
