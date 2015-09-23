if [ "$#" -lt 1 ] || ([ $1 != "writeback" ] && [ $1 != "writethrough" ]); then
	echo "Usage: $0 writeback|writethrough"
	exit 1
fi

NC_ID=10.218.169.156

sudo cp lib/helper_$1.py lib/helper.py 

qapython s18vm.py

pssh -H $NC_ID -i "sudo /opt/acache/acache_ctl all all cache_on"
if [ $1 == "writeback" ]; then
	pssh -H $NC_ID -i "sudo /opt/acache/acache_ctl all all cache_mode writeback"
fi

qapython twdd.py

qapython fio-dirtylimit.py

