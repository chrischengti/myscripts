#!/bin/sh

if [ $# -ne 2 ]; then
	echo -e  "Need two files"
	exit 1
fi

#handle first data

if [ -e "result1.csv" ]; then
	rm result1.csv
fi
touch result1.csv

cat $1 | grep "case" | gawk -F "," 'BEGIN{OFS = "\t"} {print $1, $11, $12, $16, $23, $24, $28}' | tee -a result1.csv

#check
while read line
do
	cat $1 | grep "$line," | gawk -F "," 'BEGIN{count = 0} { if ($11 + $23 != 0) {count += 1;}}
		END{if (count != 19 && count != 0) {print "**************Warnning " $1 " has only " count " sets******************"}}' |tee -a result1.csv 
done < template.csv

#collect 18vm data
while read line
do
	cat $1 | grep "$line," | gawk -F "," 'BEGIN{r_bw = 0; r_iops = 0; w_bw = 0; w_iops = 0; r_la = 0; w_la = 0; count = 0; OFS = "\t"}
		{ if ($11 + $23 != 0 && count < 18) {
				r_bw += $11; r_iops += $12; w_bw += $23; w_iops += $24; count += 1; r_la += $16; w_la += $28;
		}}
		END{if (count != 0) {
				title = $1"-"count; print title, r_bw/(count * 1024), r_iops/count, r_la/count, w_bw/(1024 * count), w_iops/count, w_la/count
		}}' |tee -a result1.csv 
done < template.csv

#collect 1vm
while read line
do
	cat $1 | grep "$line," | gawk -F "," 'BEGIN{r_bw = 0; r_iops = 0; w_bw = 0; w_iops = 0; r_la = 0; w_la = 0; count = 0; OFS = "\t"}
		{ if ($11 + $23 != 0) {
				count += 1;
		  }
		  if (count > 18) {
				title = $1"-1"; print title, $11/1024, $12, $16, $23/1024, $24, $28
		  }
		}' |tee -a result1.csv
done < template.csv

#handle second data

if [ -e "result2.csv" ]; then
	rm result2.csv
fi
touch result2.csv

cat $2 | grep "case" | gawk -F "," 'BEGIN{OFS = "\t"} {print $1, $11, $12, $16, $23, $24, $28}' | tee -a result2.csv

#check
while read line
do
	cat $2 | grep "$line," | gawk -F "," 'BEGIN{count = 0} { if ($11 + $23 != 0) {count += 1;}}
		END{if (count != 19 && count != 0) {print "**************Warnning " $1 " has only " count " sets******************"}}' |tee -a result2.csv 
done < template.csv

#collect 18vm
while read line
do
	cat $2 | grep "$line," | gawk -F "," 'BEGIN{r_bw = 0; r_iops = 0; w_bw = 0; w_iops = 0; r_la = 0; w_la = 0; count = 0; OFS = "\t"}
		{ if ($11 + $23 != 0 && count < 18) {
				r_bw += $11; r_iops += $12; w_bw += $23; w_iops += $24; count += 1; r_la += $16; w_la += $28;
		}}
		END{if (count != 0) {
				title = $1"-"count; print title, r_bw/(count * 1024), r_iops/count, r_la/count, w_bw/(1024 * count), w_iops/count, w_la/count
		}}' |tee -a result2.csv 
done < template.csv

#collect 1vm
while read line
do
	cat $2 | grep "$line," | gawk -F "," 'BEGIN{r_bw = 0; r_iops = 0; w_bw = 0; w_iops = 0; r_la = 0; w_la = 0; count = 0; OFS = "\t"}
		{ if ($11 + $23 != 0) {
				count += 1;
		  }
		  if (count > 18) {
				title = $1"-1"; print title, $11/1024, $12, $16, $23/1024, $24, $28
		  }
		}' |tee -a result2.csv
done < template.csv

#compare two sets of data

status=`cat result1.csv|grep "has only"`
if [ "$status" != "" ]; then
    echo
	#exit 2
fi

status=`cat result2.csv|grep "has only"`
if [ "$status" != "" ]; then
    echo
	#exit 2
fi

if [ -e "result.csv" ]; then
	rm result.csv
fi
touch result.csv

echo -e  "casename\\tr_bw/s-1\\tr_bw/s-2\\tr_iops-1\\tr_iops-2\\tr_latency_usec-1\\trlatency_usec-2\\tw_bw-1\\tw_bw-2\\tw_iops-1\\tw_iops-2\\tw_latency_usec-1\\tw_latency_usec-2"|tee -a result.csv
while read line
do
	read_bw1=`cat result1.csv|sed -n '/-18\t/p'|grep "$line-"|awk -F " " '{print $2}'`
	read_iops1=`cat result1.csv|sed -n '/-18\t/p'|grep "$line-"|awk -F " " '{print $3}'`
	read_mean_latency_usec1=`cat result1.csv|sed -n '/-18\t/p'|grep "$line-"|awk -F " " '{print $4}'`
	write_bw1=`cat result1.csv|sed -n '/-18\t/p'|grep "$line-"|awk -F " " '{print $5}'`
	write_iops1=`cat result1.csv|sed -n '/-18\t/p'|grep "$line-"|awk -F " " '{print $6}'`
	write_mean_latency_usec1=`cat result1.csv|sed -n '/-18\t/p'|grep "$line-"|awk -F " " '{print $7}'`
	read_bw2=`cat result2.csv|sed -n '/-18\t/p'|grep "$line-"|awk -F " " '{print $2}'`
	read_iops2=`cat result2.csv|sed -n '/-18\t/p'|grep "$line-"|awk -F " " '{print $3}'`
	read_mean_latency_usec2=`cat result2.csv|sed -n '/-18\t/p'|grep "$line-"|awk -F " " '{print $4}'`
	write_bw2=`cat result2.csv|sed -n '/-18\t/p'|grep "$line-"|awk -F " " '{print $5}'`
	write_iops2=`cat result2.csv|sed -n '/-18\t/p'|grep "$line-"|awk -F " " '{print $6}'`
	write_mean_latency_usec2=`cat result2.csv|sed -n '/-18\t/p'|grep "$line-"|awk -F " " '{print $7}'`
#	echo -e  "$line\\t$read_bw1"|tee -a result.csv
	echo -e  "$line-18\\t$read_bw1\\t$read_bw2\\t$read_iops1\\t$read_iops2\\t$read_mean_latency_usec1\\t$read_mean_latency_usec2\\t$write_bw1\\t$write_bw2\\t$write_iops1\\t$write_iops2\\t$write_mean_latency_usec1\\t$write_mean_latency_usec2"|tee -a result.csv
done < template.csv

#read_bw1=`cat result1.csv|sed -n '/-1\t/p'|grep "randwrite-4k-1-"|awk -F " " '{print $4}'`
#echo -e  $read_bw1

while read line
do
	read_bw1=`cat result1.csv|sed -n '/-1\t/p'|grep "$line-"|awk -F " " '{print $2}'`
	read_iops1=`cat result1.csv|sed -n '/-1\t/p'|grep "$line-"|awk -F " " '{print $3}'`
	read_mean_latency_usec1=`cat result1.csv|sed -n '/-1\t/p'|grep "$line-"|awk -F " " '{print $4}'`
	write_bw1=`cat result1.csv|sed -n '/-1\t/p'|grep "$line-"|awk -F " " '{print $5}'`
	write_iops1=`cat result1.csv|sed -n '/-1\t/p'|grep "$line-"|awk -F " " '{print $6}'`
	write_mean_latency_usec1=`cat result1.csv|sed -n '/-1\t/p'|grep "$line-"|awk -F " " '{print $7}'`
	read_bw2=`cat result2.csv|sed -n '/-1\t/p'|grep "$line-"|awk -F " " '{print $2}'`
	read_iops2=`cat result2.csv|sed -n '/-1\t/p'|grep "$line-"|awk -F " " '{print $3}'`
	read_mean_latency_usec2=`cat result2.csv|sed -n '/-1\t/p'|grep "$line-"|awk -F " " '{print $4}'`
	write_bw2=`cat result2.csv|sed -n '/-1\t/p'|grep "$line-"|awk -F " " '{print $5}'`
	write_iops2=`cat result2.csv|sed -n '/-1\t/p'|grep "$line-"|awk -F " " '{print $6}'`
	write_mean_latency_usec2=`cat result2.csv|sed -n '/-1\t/p'|grep "$line-"|awk -F " " '{print $7}'`
#	echo -e  "$line\\t$read_bw1"|tee -a result.csv
	echo -e  "$line-1\\t$read_bw1\\t$read_bw2\\t$read_iops1\\t$read_iops2\\t$read_mean_latency_usec1\\t$read_mean_latency_usec2\\t$write_bw1\\t$write_bw2\\t$write_iops1\\t$write_iops2\\t$write_mean_latency_usec1\\t$write_mean_latency_usec2"|tee -a result.csv
done < template.csv

sh analyse.sh
