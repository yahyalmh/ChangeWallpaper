#!/usr/bin/env bash

# echo "XDG_CURRENT_DESKTOP: $XDG_CURRENT_DESKTOP, BASH_VERSION: ${BASH_VERSION},  GDMSESSION: $GDMSESSION"
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
  PID=$(pgrep gnome-session -n -U $UID)

  if [[ -z "${PID}" ]]; then
    PID=$(pgrep -o "cinnamon-sess|gnome-sess|mate-sess")
  fi

  dbus=$(grep -z DBUS_SESSION_BUS_ADDRESS /proc/"${PID}"/environ | tr '\0' '\n' | cut -d= -f2-)
  export DBUS_SESSION_BUS_ADDRESS=${dbus}
}

function export_dbus_second_way() {
  file=$(find /proc -maxdepth 2 -user ${user} -name environ -print -quit)
  per_file=${file}

  for i in {1..20}; do
    if [[ ! -f ${file} ]]; then
      break
    fi
    per_file=${file}
    file=$(find /proc -maxdepth 2 -user ${user} -name environ -newer "${file}" -print -quit)
  done

  dbus=$(grep -z DBUS_SESSION_BUS_ADDRESS "${per_file}" | tr '\0' '\n' | cut -d= -f2-)
  export DBUS_SESSION_BUS_ADDRESS=$dbus
}

function change_background() {
  image_address="${1}"
  if [[ "$GDMSESSION" =~ ^ubuntu.* ]]; then
    gsettings set org.gnome.desktop.background picture-uri "file://${image_address}"
  fi

  if [[ "$GDMSESSION" =~ ^cinnamon.* ]]; then
    gsettings set org.cinnamon.desktop.background picture-uri "file://${image_address}"
  fi
}

is_cron_run
is_cron=$?

if [[ "$is_cron" == "1" ]]; then
  export DISPLAY=:0
  export GSETTINGS_BACKEND=dconf
  export_dbus_second_way
  export_dbus_first_way
fi

change_background "${imageAddress}"
exit 0
