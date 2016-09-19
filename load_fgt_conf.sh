FGT_HOST=169.254.254.100
FTP_SERVER=10.160.37.57

MAX_WAITING_TIME=100
FILE="/tmp/testfile_$(date +%s)"
HEADSTYLE='[   ]'

trap cleanup EXIT
trap terminate SIGINT 
trap hideinput CONT

hideinput()
{
  if [ -t 0 ]; then
     stty -echo -icanon time 0 min 0
  fi
}

cleanup()
{
  if [ -t 0 ]; then
    stty sane
  fi
}

terminate()
{
    cleanup
    print_fail
    exit 1
}

function status() {
    spin='-\|/'
    i=0
    if [ ! -z $1 ]; then
        PID=$1
    fi
    while kill -0 $PID 2>/dev/null; do
        sleep 1s
        i=$(( (i+1) %4 ))
        printf "\r[ ${spin:$i:1}"
    done
}

function print_pass() {
    printf '\r[ \e[1;32m%s\e[0m\n' "✔"
}

function print_fail() {
    printf '\r[ \e[1;31m%s\e[0m\n' "x"
}

function set_return() {
    if [ ! -z $1 ]; then
        if [[ "${1^^}" == "TRUE" ]]; then
            touch $FILE >/dev/null
        fi
    fi
}

function run() {
    if [ "$#" -eq 0 ]; then
        return
    fi
    rm -rf $FILE 2>&1 >/dev/null
    $@ &
    status $!
    if [ -e $FILE ]; then
        print_pass
        rm -rf $FILE 2>&1 >/dev/null
    else
        print_fail
    fi
}

function pinghost() {
    FILE=${FILE:-'/tmp/test_pinghost'}
    PINGABLE=False
    start=$SECONDS
    duration=$(( SECONDS - start ))    
    printf "${HEADSTYLE} Checking the connectivity of the host [ ${FGT_HOST} ]."
    if [ ! -z $1 ];then
        sleep $1
    fi
    while [[ "$PINGABLE" == "False" && "$duration" -lt $MAX_WAITING_TIME ]]; do
        sleep 2s
        duration=$(( SECONDS - start ))
        ping -c 1 ${FGT_HOST} > /dev/null
        if [ $? -eq 0 ]; then
            PINGABLE=True
        fi
    done
    set_return $PINGABLE
}

function load_init() {
    LOADED=False
    A="
99
config global
execute restore config ftp backup.conf ${FTP_SERVER} root root
y
exit
"
#echo "$A"
    printf "${HEADSTYLE} Load the initial configure to the host [ ${FGT_HOST} ]."
    ssh -o StrictHostKeyChecking=no -o ConnectTimeout=10 -tt admin@${FGT_HOST} <<EOF >/dev/null 2>&1 &
$A
EOF
    if wait $!; then
        LOADED=True
    fi
    set_return $LOADED
}

hideinput
run pinghost
run load_init
run pinghost 10 
