#!/bin/sh

if [ ! -f "result1.csv" ]; then
	echo -e  "result1.csv not found"
	exit 1
fi

if [ -f "data.csv" ]; then
	rm data.csv
fi
touch data.csv

echo -e  'vmNum\t\t\t18vm\t\t\t\t1vm'|tee -a data.csv

#remvoe the data after dot

sed -ri 's/([0-9]{1,10})\.[0-9]{1,10}/\1/g' result1.csv
#read_iops
echo -e  -n "read_iops"|tee -a data.csv
result_18vm=`cat result1.csv|grep "randread-4k-128-18"|awk -F " " '{print $3*18}'`
result_1vm=`cat result1.csv|grep 'randread-4k-128-1'|sed -n '/-18/d;p'|awk -F " " '{print $3}'`
echo -e  "\t\t$result_18vm\t\t\t\t$result_1vm"|tee -a data.csv

#read_bw
echo -e  -n "read_bw_MB/s"|tee -a data.csv
result_18vm=`cat result1.csv|grep "read-1M-128-18"|awk -F " " '{print  $2*18}'`
echo -e  -n "\t\t$result_18vm"|tee -a data.csv
result_1vm=`cat result1.csv|grep 'read-1M-128-1'|sed -n '/-18/d;p'|awk -F " " '{print $2}'`
echo -e   "\t\t\t\t$result_1vm"|tee -a data.csv


#read_latency
result_18vm=`cat result1.csv|grep "randread-4k-1-18"|awk -F " " '{print $4}'`
result_1vm=`cat result1.csv|grep "randread-4k-1-1"|sed -n '/-18/d;p'|awk -F " " '{print $4}'`
echo -e  "read_mean_latency_usec\t$result_18vm\t\t\t\t$result_1vm"|tee -a data.csv


#write_iops
echo -e  -n "write_iops"|tee -a data.csv
result_18vm=`cat result1.csv|grep "randwrite-4k-128-18"|awk -F " " '{print $6*18}'`
result_1vm=`cat result1.csv|grep "randwrite-4k-128-1"|sed -n '/-18/d;p'|awk -F " " '{print $6}'`
echo -e  "\t\t$result_18vm\t\t\t\t$result_1vm"|tee -a data.csv

#write_bw
echo -e  -n "write_bw_MB/s"|tee -a data.csv
result_18vm=`cat result1.csv|grep "write-1M-128-18"|awk -F " " '{print $5*18}'`
echo -e  -n "\t\t$result_18vm"|tee -a data.csv
result_1vm=`cat result1.csv|grep "write-1M-128-1"|sed -n '/-18/d;p'|awk -F " " '{print $5}'`
echo -e   "\t\t\t\t$result_1vm"|tee -a data.csv

#write_latency
result_18vm=`cat result1.csv|grep "randwrite-4k-1-18"|awk -F " " '{print $7}'`
result_1vm=`cat result1.csv|grep "randwrite-4k-1-1"|sed -n '/-18/d;p'|awk -F " " '{print $7}'`
echo -e  "write_mean_latency_usec\t$result_18vm\t\t\t\t$result_1vm"|tee -a data.csv

#rw_iops
echo -e  -n "rw_iops"|tee -a data.csv
result_18vm=`cat result1.csv|grep "randrw-4k-128-18"|awk -F " " '{print $6*18}'`
result_1vm=`cat result1.csv|grep "randrw-4k-128-1"|sed -n '/-18/d;p'|awk -F " " '{print $6}'`
echo -e  "\t\t\t$result_18vm\t\t\t\t$result_1vm"|tee -a data.csv

#rw_bw
echo -e  -n "rw_bw_MB/s"|tee -a data.csv
result_18vm=`cat result1.csv|grep "rw-1M-128-18"|awk -F " " '{print $5*18}'`
echo -e  -n "\t\t$result_18vm"|tee -a data.csv
result_1vm=`cat result1.csv|grep "rw-1M-128-1"|sed -n '/-18/d;p'|awk -F " " '{print $5}'`
echo -e   "\t\t\t\t$result_1vm"|tee -a data.csv

#rw_latency
result_18vm=`cat result1.csv|grep "randrw-4k-1-18"|awk -F " " 'BEGIN{OFS = "/"}{print $4, $7}'`
result_1vm=`cat result1.csv|grep "randrw-4k-1-1"|sed -n '/-18/d;p'|awk -F " " 'BEGIN{OFS = "/"}{print $4, $7}'`
echo -e  "rw_mean_latency_usec\t\t$result_18vm\t\t\t$result_1vm"|tee -a data.csv
