FGT_HOST=169.254.254.100
FTP_SERVER=10.160.37.57

function checkstatus () {
    start=$SECONDS
    duration=$(( SECONDS - start ))
    sleep 10s
    while [[ "$duration" -lt 30 ]]; do
        duration=$(( SECONDS - start ))
        sleep 1s
        ping -c 2 ${FGT_HOST} > /dev/null
        if [ $? -eq 0 ]; then          
            break        
        fi
    done
}

ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 -tt admin@${FGT_HOST} << EOF
99
config global
execute restore config ftp backup.conf ${FTP_SERVER} root root
y
exit
EOF

checkstatus

ssh -o StrictHostKeyChecking=no -tt admin@${FGT_HOST} << 'EOF' > fgt.log &
99
config global
diag debug enable
diag debug application httpsd 255
diag debug cli 8
EOF

