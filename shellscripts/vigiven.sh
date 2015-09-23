ls -t bcachelogs/ | head -n 4
file=`ls -t bcachelogs/ | head | awk "NR==$1"`
echo $file

vi bcachelogs/$file
