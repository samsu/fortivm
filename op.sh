FGT_INT_PORT=fgt-int-port
FGT_EXT_PORT=fgt-ext-port

ovs-vsctl set port $FGT_INT_PORT trunks=1,3

#echo $PWD
