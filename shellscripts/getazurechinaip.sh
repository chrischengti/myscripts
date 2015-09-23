azure account set fb911cb9-ef41-4f12-83a1-2d1cb5ac54af
vms="net01-east
net02-east
net-cnnorth1
net-cnnorth2"

for vm in `echo $vms`
do
echo $vm
azure vm show $vm | grep "PublicIPs 0 address"
done
