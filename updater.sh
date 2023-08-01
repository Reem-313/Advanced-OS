#!/usr/bin/env bash
#
# file: updater.bash
# title: Updater
# description: Script to update local repository
#              and run auto-run script if there are updates
#

export LOG_FILE=${LOGS_PATH}/updater.log

# where the project repository located
PROJECT_PATH=${PROJECT_PATH}
# ensure script is running from project directory
cd $PROJECT_PATH

source ./lib/logger.sh
source ./lib/cpu_control.sh

set_performance


LOG_DEBUG "updater job starting"

# check if there are updates in repo
# redirecting stderr to stdout
fetch_status=$(git fetch --dry-run 2>&1)
[[ $? -ne 0 ]] && LOG_ERROR "updater failed; could not fetch possible updates from remote repository"

if [[ -z $fetch_status ]]; then
    LOG_INFO "local repository up to date, skipping updated"
else
    LOG_INFO "local repository out of date, starting update"
    # ensure repo is unchanged
    git reset --hard
    # pull updates into local repository
    git pull
    [[ $? -ne 0 ]] && LOG_ERROR "updater failed; could not pull updates from remote repository"

    # ensure autorun script is executable
    chmod +x autorun.sh
    [[ $? -ne 0 ]] && LOG_ERROR "updater failed; could not make auto-run script executable"

    ./autorun.sh
    [[ $? -ne 0 ]] && LOG_ERROR "updater failed; auto-run script exited with non-zero status"

    LOG_DEBUG "update complete"
fi

set_power_save