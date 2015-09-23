if [ $# -lt 1 ]; then
    echo 'Usage: sh batch_exec.sh <command>'
    exit 1
fi

sudo xenstore-list /local/domain | grep -v ^0 | xargs -n 1 -I {} sudo xm gshell -d {} -a exec -t -1 -l "$*"
