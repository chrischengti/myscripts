modes="writeback"
#modes="writethrough"

NC_ID=10.101.192.12

prepare(){
#sudo cp lib/helper_$mode.py lib/helper.py
if [ $mode == "writeback" ]; then

sed -i 's/barrier=[0-1]/barrier=1/' lib/helper.py
else
sed -i 's/barrier=[0-1]/barrier=0/' lib/helper.py
fi
echo preparing vms
time qapython s18vm.py

pssh -H $NC_ID -i "sudo /opt/acache/acache_ctl all all cache_on"
if [ $mode == "writeback" ]; then
    echo $mode
    pssh -H $NC_ID -i "sudo /opt/acache/acache_ctl all all cache_mode writeback"
else
    echo $mode
    pssh -H $NC_ID -i "sudo /opt/acache/acache_ctl all all cache_mode writethrough"
fi

echo preparing test file
#time qapython twdd.py
}

bcacheTest(){
echo starting test mode $mode
date

prepare

echo starting io test
#time qapython fio-dirtylimit.py

echo clearing  vms
#time sh clear.sh

echo finishing test mode $mode
}

nopeFunc(){
echo nopefunc
}

for mode in `echo $modes`
do
	logname=$mode`date +%s`
        echo $mode
        echo $logname
	#time ls > bcachelogs/$logname 2>&1
	#time nopeFunc > bcachelogs/$logname 2>&1
	time bcacheTest > bcachelogs/$logname 2>&1
done

