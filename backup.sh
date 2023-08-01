#!/usr/bin/env bash
#
# File: backup.sh
# Title: Backup
# Description: Script to backup logs from sensors and images 
#              from camera
# Author: Kieran Best

export LOG_FILE=${LOGS_PATH}/backup.log

# where the project repository located
PROJECT_PATH=${PROJECT_PATH}
# ensure script is running from project directory
cd $PROJECT_PATH

source ./lib/logger.sh

sshpass -p 'guest' rsync -ar /home/pi/logs /home/pi/images guest@10.150.200.112:/mnt/NAS/Data/2023/bit-lords
if [[ $? -ne 0 ]]; then 
  LOG_ERROR "backup failed"
else
  LOG_INFO "backup successful"
fi
