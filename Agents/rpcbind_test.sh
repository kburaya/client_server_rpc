#!/bin/bash

usage() {
    echo "Script usage: $0 ns_name [start|stop]"
}

MOUNT_SRC=/var/run/rpcbind.netns

# add_mount <ns> <ext>
add_mount() {
    dst=/var/run/rpcbind.$2
    if [ `mount | grep $dst | wc -l` != 0 ]; then
        umount $dst 2> /dev/null
    fi
    touch $MOUNT_SRC/$1.$2
    mount --bind $MOUNT_SRC/$1.$2 $dst
}

# del_mount <ns> <ext>
del_mount() {
    umount $MOUNT_SRC/$1.$2 2> /dev/null
    rm $MOUNT_SRC/$1.$2
}

start_in_ns() {
    echo "^^^start^^^"
    ip link set lo up

    add_mount $1 lock
    add_mount $1 sock

    /sbin/rpcbind

    pid=`lsof -bt -i4 -a -i TCP:sunrpc`
    echo "pid=$pid"
}

stop_in_ns() {
    echo "^^^stop^^^"

    pid=`lsof -bt -i4 -a -i TCP:sunrpc`
    echo "pid=$pid"

    if [ ! -z $pid ]; then
        kill -ABRT $pid
    fi

    del_mount $1 lock
    del_mount $1 sock
}

### script body ###

if [ $# -lt 2 -o -z "$1" ]; then
    usage
    exit 1
fi

ns="$1"
op="$2"

case "$op" in
    "start")
        if [ ! -d $MOUNT_SRC ]; then
            mkdir -p $MOUNT_SRC
        fi
        if [ ! -f /var/run/netns/$ns ]; then
            ip netns add "$ns"
        fi
        ip netns exec "$ns" $0 "$ns" start-in-ns
        ;;
    "stop")
        ip netns exec "$ns" $0 "$ns" stop-in-ns
        ip netns del "$ns"
        ;;
    "start-in-ns")
        start_in_ns "$ns"
        ;;
    "stop-in-ns")
        stop_in_ns "$ns"
        ;;
    *)
        usage
        exit 1
        ;;
esac