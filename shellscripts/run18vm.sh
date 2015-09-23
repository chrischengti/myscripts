NC_ID=10.101.192.12
modes="writebackr0d0
writebackr1d128m
writethrough
cacheoff"

#modes="writethrough"
#modes="nocachemod"
#modes="cacheoff"
#modes="writebackr0d0"
#modes="writebackr1d128m"

preparevm(){
#sudo cp lib/helper_$mode.py lib/helper.py
if [[ $mode == *"writeback"* ]]; then
sed -i 's/barrier=[0-1]/barrier=1/' lib/helper.py
elif [[ $mode == *"writethrough"* ]]; then
sed -i 's/barrier=[0-1]/barrier=0/' lib/helper.py
else
sed -i 's/barrier=[0-1]/barrier=0/' lib/helper.py
fi

echo preparing vms
#time qapython s18vm.py
time qapython s18vm.py
echo vm prepared
}

preparefile(){
echo prepareing test file on guests
time qapython twdd.py
}

writethrough(){

pssh -H $NC_ID -i "sudo /opt/acache/acache_ctl all all cache_on"
pssh -H $NC_ID -i "sudo /opt/acache/acache_ctl all all cache_mode writethrough"

}
writeback(){
pssh -H $NC_ID -i "sudo /opt/acache/acache_ctl all all cache_on"
pssh -H $NC_ID -i "sudo /opt/acache/acache_ctl all all cache_mode writeback"
}
writebackr0d0(){
pssh -H $NC_ID -i "sudo /opt/acache/acache_ctl all all cache_on"
pssh -H $NC_ID -i "ls /sys/block |grep tapdev | xargs -I {} sudo sh -c 'cat /sys/block/{}/bcache/writeback_running'"
pssh -H $NC_ID -i "ls /sys/block |grep tapdev | xargs -I {} sudo sh -c 'echo 0 > /sys/block/{}/bcache/writeback_running'"
pssh -H $NC_ID -i "sudo /opt/acache/acache_ctl all all dirty_limits 0"
}

writebackr1d128m(){
pssh -H $NC_ID -i "sudo /opt/acache/acache_ctl all all cache_on"
pssh -H $NC_ID -i "sudo /opt/acache/acache_ctl all all dirty_limits 128000000"
}
nocachemod(){
echo cachemod must have been removed
}
cacheoff(){
pssh -H $NC_ID -i "sudo /opt/acache/acache_ctl all all cache_off"
}

bcacheTest(){
echo starting test mode $mode
date

preparevm

#mode specific setup
$mode

preparefile

echo starting io test
#time qapython fio-dirtylimit.py
time qapython fio-dirtylimit18.py

#show test results
sh handlegiven.sh 1

echo clearing  vms
time sh clear.sh

echo finishing test mode $mode
}


for mode in `echo $modes`
do
	logname=$mode`date +%s`
        echo $mode
        echo $logname
	time bcacheTest > bcachelogs/$logname 2>&1
   #save test results to file with mode info 
    echo "18vm test results mode" $mode
    cat data.csv | awk '{print $2}' > bcachelogs/$(logname)result
    cat data.csv | awk '{print $3}' >> bcachelogs/$(logname)result
done

