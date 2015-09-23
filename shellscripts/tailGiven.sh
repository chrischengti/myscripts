ls -t bcachelogs/ | head -n 4
file=`ls -t bcachelogs/ | head | awk "NR==$1"`
echo $file

tail -f  bcachelogs/$file
