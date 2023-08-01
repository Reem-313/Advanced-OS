#!/usr/bin/env bash
#
# file: capture_readings.sh
# title: capture readings
# description: take measurements from the sensors and camera
# author: Reem Khider
# contribution: Leo Spratt

# where the project repository located
PROJECT_PATH=${PROJECT_PATH}
# ensure script is running from project directory
cd $PROJECT_PATH

source ./lib/cpu_control.sh

set_performance

python3 temp_and_humid_sensor.py
python3 grove_gas_sensor_mq5.py 0
python3 pi_cam_capture.py

set_power_save
