#!/usr/bin/env bash
#
# file: lib/cpu_control.sh
# title: cpu control
# description: control cpu speed
# usage: source file in another bash script to use
# author: Reem Khider
# contribution: Leo Spratt


GOVDIR="/sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"

gov_power_save=powersave
gov_performance=performance

set_governor(){
    gov=$1
    echo "${gov}" | sudo tee ${GOVDIR}
}

set_power_save(){
    set_governor $gov_power_save
}
set_performance(){
    set_governor $gov_performance
}