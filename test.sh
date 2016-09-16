BR_FGT=br-fgt
NET_MGMT=net-mgmt

# create a nat network for the fgtvm management plane.
brctl show |grep  $BR_FGT >> /dev/null
if [[ $? -ne 0 ]]; then
    echo "create bridge"
    cat > $NET_MGMT.xml << EOF
<network>
  <name>$NET_MGMT</name>
  <bridge name="$BR_FGT"/>
  <forward mode="nat"/>
  <ip address="169.254.254.1" netmask="255.255.255.0">
    <dhcp>
      <range start="169.254.254.100" end="169.254.254.254"/>
    </dhcp>
  </ip>
</network>
EOF
    virsh net-define $NET_MGMT.xml
    virsh net-start $NET_MGMT
    virsh net-autostart $NET_MGMT
else   
    echo "bridge existed"
fi

if [[ ! -z $1 ]]; then
    echo "params=$1"
    echo "deleting $NET_MGMT"
    virsh net-destroy $NET_MGMT
    virsh net-undefine $NET_MGMT
fi
