#!/usr/bin/env bash
#
# file: autorun.bash
# title: Auto-Run
# description: Script to be triggered when updater
#              has pulled updates, ensuring all libraries
#              and setup is handled automatically
#
set -e

cd ${PROJECT_PATH}

source ./lib/logger.sh

LOG_DEBUG "autorun job starting"

#
# Cron Update
#
# Replace crontab allowing for changes to the updater.cron
# file to be set without manual intervention
#
crontab < updater.cron

#
# Install Required Tools
#
python3 -m pip install \
    opencv-python==4 \
    git+https://github.com/Seeed-Studio/grove.py \
    git+https://github.com/Seeed-Studio/Seeed_Python_DHT

LOG_DEBUG "autorun job finished"
