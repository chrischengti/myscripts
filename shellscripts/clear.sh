NC_ID=10.101.192.12

pssh -H $NC_ID -i "sudo xm shutdown -a"

while true
do
    vms=`pssh -H $NC_ID -i "sudo xm li | grep io_vm | wc -l" | grep -v $NC_ID`
    if [ $vms -eq 0 ]
    then
        break
    fi
    sleep 10
done

while true
do
	TIME=`date`
	echo "[$TIME] waiting for devices shutting down"
	sleep 60
	bcache_devs=`pssh -H $NC_ID -i "ls /sys/block | grep bcache" | grep bcache`
	for bcache in $bcache_devs
	do
		echo "sudo sh -c 'echo 1 > /sys/block/$bcache/bcache/stop'"
		pssh -H $NC_ID -i "sudo sh -c 'echo 1 > /sys/block/$bcache/bcache/stop'"
	done

	tapdevs=`pssh -H $NC_ID -i "ls /sys/class/blktap2/ | grep blktap" | grep blktap`
	for blktap in $tapdevs
	do
		echo "sudo sh -c 'echo 1 > /sys/class/blktap2/$blktap/remove'"
		pssh -H $NC_ID -i "sudo sh -c 'echo 1 > /sys/class/blktap2/$blktap/remove'"
	done
	if [ "$bcache_devs" == "" ] && [ "$tapdevs" == "" ]
	then
		break
	fi
done

