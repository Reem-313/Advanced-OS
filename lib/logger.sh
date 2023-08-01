#!/usr/bin/env bash
#
# file: lib/logger.sh
# title: Logger Library
# description: library following RFC 5424 standard
# usage: source file in another bash script to use
# author: Leo Spratt
#
set -euo pipefail

# Available log levels
declare -A LOG_LEVELS
export LOG_LEVELS=(
	[OFF]=8
	[DEBUG]=7
	[INFO]=6
	[NOTICE]=5
	[WARNING]=4
	[ERROR]=3
	[CRITICAL]=2
	[ALERT]=1
	[EMERGENCY]=0
)
# Log level colour codes (excluding OFF)
# SOURCE: https://www.cyberciti.biz/faq/bash-shell-change-the-color-of-my-shell-prompt-under-linux-or-unix/
declare -A LOG_LEVEL_COLOURS
LOG_COLOUR_RESET="\033[0m"
LOG_LEVEL_COLOURS=(
	[DEBUG]="\033[0;34m"
	[INFO]="\033[0;37m"
	[NOTICE]="\033[1;32m"
	[WARNING]="\033[1;33m"
	[ERROR]="\033[1;31m"
	[CRITICAL]="\033[44m"
	[ALERT]="\033[45m"
	[EMERGENCY]="\033[41m"
)
LOG_FORMAT="%TIMESTAMP %PID [%LEVEL] %MESSAGE"
LOG_TIMESTAMP_FORMAT="+%F %T %Z"
# get log level, using default INFO if not set
export LOG_LEVEL=${LOG_LEVEL:-LOG_LEVELS[INFO]}
# where to write log file to, if set
export LOG_FILE=${LOG_FILE:-""}
export LOG_SIZE_MAX=${LOG_SIZE_MAX:-"10000"}
export LOG_ARCHIVE_MAX=${LOG_ARCHIVE_MAX:-"5"}

# Internal method to create a log line, given a level and message
# Usage: create_log_line <level> <message>
create_log_line() {
    local level=$1
	local message=$2
	local timestamp=$(date "${LOG_TIMESTAMP_FORMAT}")
	local pid=$$
	local log_line="$LOG_FORMAT"
	log_line="${log_line/'%TIMESTAMP'/$timestamp}"
	log_line="${log_line/'%PID'/$pid}"
	log_line="${log_line/'%LEVEL'/$level}"
	log_line="${log_line/'%MESSAGE'/$message}"
    echo $log_line
}
# Internal method to rotate a log directory
# Usage: log_rotate
log_rotate() {
    local logs_dir=$(dirname ${LOG_FILE})
    local log_name=$(basename ${LOG_FILE})
    # get current log size in bytes
    # SOURCE: https://unix.stackexchange.com/a/6653
    local current_log_size=$(wc -c $LOG_FILE | awk '{print $1}')
    # get the amount of existing archives
    local archive_count=$(ls ${logs_dir} | grep "${log_name}.*.gz" | wc -l)
    # check if log file has reached size limit
    if [[ $current_log_size -gt $LOG_SIZE_MAX ]]; then
        echo "archiving logs ${archive_count}"
        # check if there are archives to rotate
        if [[ $archive_count -gt 0 ]]; then
            # rotate archives (1 -> 2, 2 -> 3, etc)
            # only allow LOG_ARCHIVE_MAX number of archives
            for ((i=${LOG_ARCHIVE_MAX}-1; i!=0; i--)); do
                if [[ -e "${LOG_FILE}.${i}.gz" ]]; then
                    local n=$((${i}+1))
                    mv ${LOG_FILE}.${i}.gz ${LOG_FILE}.${n}.gz
                fi
            done
        fi
        # make archive of current log, using the latest archive count
        # SOURCE: https://linuxize.com/post/gzip-command-in-linux/
        gzip -c "${LOG_FILE}" > "${LOG_FILE}.1.gz"
        # reset log file
        # SOURCE: https://superuser.com/a/90009
        echo -n "" > ${LOG_FILE}
    fi
}
# Internal method to log a message, with given configuration
# Usage: log <level> <message>
log() {
	local level=$1
    # convert log level string into level number
    local level_number=${LOG_LEVELS[${level}]}
    local message=

	# skip logging if level is disabled
	if [[ ${level_number} -gt ${LOG_LEVEL} ]] || [[ ${LOG_LEVEL} = ${LOG_LEVELS[OFF]} ]]; then
		return
	fi

    # handle if message if piped in, otherwise take from argument
    # SOURCE: https://stackoverflow.com/a/7045517
    if [[ -p /dev/stdin ]]; then
        message=$(cat -)
    else
        message=$2
    fi

    # create the log line to log
    local log_line=$(create_log_line "$level" "$message")

    if [[ -z "${LOG_FILE}" ]]; then
        # get colour for log level
        local colour=${LOG_LEVEL_COLOURS[${level}]}
        # add colour to log line with reset at end
        log_line="${colour}${log_line}${LOG_COLOUR_RESET}"
        # log to stdout/stderr depending on severity
        if [[ $level_number -lt ${LOG_LEVELS[WARNING]} ]]; then
            echo -e ${log_line} >> /dev/stderr
        else
            echo -e ${log_line} >> /dev/stdout
        fi
    else
        # log to file specified
        # ensure logging directory exists
        local log_dir=$(dirname ${LOG_FILE})
        [[ -d ${log_dir} ]] || mkdir -p ${log_dir}

        # SOURCE: https://linuxize.com/post/bash-append-to-file/
        echo "${log_line}" >>"${LOG_FILE}"

        log_rotate
    fi
}

# Public methods for logging at pre-defined levels
# Usage: LOG_<level> <message>
LOG_DEBUG() { log "DEBUG" "$@"; }
LOG_INFO() { log "INFO" "$@"; }
LOG_NOTICE() { log "NOTICE" "$@"; }
LOG_WARNING() { log "WARNING" "$@"; }
LOG_ERROR() { log "ERROR" "$@"; exit 1; }
LOG_CRITICAL() { log "CRITICAL" "$@"; exit 1; }
LOG_ALERT() { log "ALERT" "$@"; exit 1; }
LOG_EMERGENCY() { log "EMERGENCY" "$@"; exit 1; }
