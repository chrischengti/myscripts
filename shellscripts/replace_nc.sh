newip=10.101.192.12

files="runAll.sh
clear.sh
conf/tdc.conf
listvm.sh
tw_config.txt"

for file in `echo $files`
do
    sed -r '0,s/(\b[0-9]{1,3}\.){3}[0-9]{1,3}\b'/$newip/ $file
done
