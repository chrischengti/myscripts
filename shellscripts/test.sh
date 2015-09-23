func () {
echo $testmode
#sleep 100
if [ $vmnum -eq 18 ] ; then
echo $vmnum xxxx
fi
}

testmode='hi nihao'
vmnum=$1

time func
