echo write 18vm iodepth
grep randwrite-16k result1.csv | grep '\-18' | awk '{print $6}'
echo write 1vm iodepth
grep randwrite-16k result1.csv | grep -v '\-18' | awk '{print $6}'
echo read 18vm iodepth
grep randread-16k result1.csv | grep '\-18' | awk '{print $3}'
echo read 1vm iodepth
grep randread-16k result1.csv | grep -v '\-18' | awk '{print $3}'
