#!/usr/bin/env bash

imageAddress="$1"
user=$(whoami)

function is_cron_run() {
    is_cron=0
    if [[ -z "$PS1" ]]; then
        is_cron=1
    else
        is_cron=0
    fi
    return ${is_cron}
}

function export_dbus_first_way() {
    pid_gnome=$(pgrep gnome-session -n -U $UID)

    DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/${pid_gnome}/environ| tr '\0' '\n'|cut -d= -f2-)
    export DBUS_SESSION_BUS_ADDRESS=${DBUS_SESSION_BUS_ADDRESS}
}
function export_dbus_second_way() {
    file=$(find /proc -maxdepth 2 -user ${user} -name environ -print -quit)
    per_file=${file}

    for i in {1..20}
    do
        if [[ ! -f ${file} ]] ; then
             break
        fi
        per_file=${file}
        file=$(find /proc -maxdepth 2 -user ${user} -name environ -newer "${file}" -print -quit)
    done

    export DBUS_SESSION_BUS_ADDRESS=$(grep -z DBUS_SESSION_BUS_ADDRESS "${per_file}" | tr '\0' '\n'| cut -d= -f2-)
}
function change_background() {
    image_address="${1}"
    gsettings set org.gnome.desktop.background picture-uri "file://${image_address}"
}

is_cron_run
is_cron=$?

if [[ "$is_cron"="1" ]] ; then
    export DISPLAY=:0
    export GSETTINGS_BACKEND=dconf
    export_dbus_second_way
    export_dbus_first_way
fi

change_background "${imageAddress}"
exit 0
