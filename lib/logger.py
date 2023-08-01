#-  File: lib/logger.py
#-  Title: Logger Library.
#-  Description: library following RFC 5424 standard.
#-  Usage: Import as a library, call log_setup and provide with 
#          path and log level, then call different log functions 
#          (log_debug("Message")).
#-  Author: Joshua-Yuill


#- Importing Required Libraries
from string import Template
from datetime import datetime
from pathlib import Path
import gzip
import shutil
import os

#- Variable Declaration (CAPS IS CONST)
LOG_FORMAT = Template("$timestamp $pid [$level] $message")

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S UTC"

log_level = int(os.environ.get("LOG_LEVEL","6")) # <Source> Environment variables in python (https://www.twilio.com/blog/environment-variables-python)
log_file = os.environ.get("LOG_FILE","")

LOG_SIZE= 20000

LOG_ARCHIVE_COUNT = 5

LOG_LEVELS = {
    "OFF":8,
    "DEBUG":7,
    "INFO":6,
    "NOTICE":5,
    "WARNING":4,
    "ERROR":3,
    "CRITICAL":2,
    "ALERT":1,
    "EMERGENCY":0    
}

LOG_NAMES = {
    8:"OFF",
    7:"DEBUG",
    6:"INFO",
    5:"NOTICE",
    4:"WARNING",
    3:"ERROR",
    2:"CRITICAL",
    1:"ALERT",
    0:"EMERGENCY"   
}


def create_log_line(level,message):
    pid = os.getpid() # <Source> Get process id in python (https://superfastpython.com/multiprocessing-get-pid/)
    timestamp = datetime.utcnow().strftime(TIMESTAMP_FORMAT)
    
    log_line = LOG_FORMAT.substitute(timestamp = timestamp,
                                     pid = pid,
                                     level = level,
                                     message = message)
    return log_line

def log(level_num,message):
    level_num = int(level_num)
    
    if level_num == LOG_LEVELS["OFF"]:
        return
    
    level_name = LOG_NAMES[level_num]
    
    logline = create_log_line(level_name,message)
    
    if log_file == "":
        print(logline)
    else:
        with open(log_file, "a") as fo:
            fo.write(logline +"\n")
        log_rotate()

def log_rotate():
    logpath = Path(log_file)
    logdir = logpath.parent
    logsize = logpath.stat().st_size
    
    archive_count = len(list(logdir.glob(logpath.name+".*.gz")))
    
    if logsize > LOG_SIZE:
        if archive_count > 0:
            for i in range(min(archive_count,(LOG_ARCHIVE_COUNT - 1)),0,-1):
                n = i + 1
                logdir.joinpath(f"{logpath.name}.{n}.gz").unlink(missing_ok=True) #- <Source> Delete path in python (https://www.codecademy.com/resources/docs/python/files/unlink)
                logdir.joinpath(f"{logpath.name}.{i}.gz").rename(logdir.joinpath(f"{logpath.name}.{n}.gz"))
        
        #- <Source> GZip in python (https://docs.python.org/3/library/gzip.html)
        with open(logpath, 'rb') as f_in: 
            with gzip.open(logdir.joinpath(f"{logpath.name}.1.gz"), 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        #-
        
        with open(logpath,"w") as fo:
            fo.write("")

#- Public functions to be called by other programs
def log_setup(level,path):
    global log_level, log_file
    
    log_level = level
    log_file = path
    try: # <Source> Create a directory python (https://www.geeksforgeeks.org/create-a-directory-in-python/)
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print("Invalid permissions to create directory. Halted")
        exit(1)


def log_debug(message):
    log(LOG_LEVELS["DEBUG"],message)

def log_info(message):
    log(LOG_LEVELS["INFO"],message)

def log_notice(message):
    log(LOG_LEVELS["NOTICE"],message)

def log_warning(message):
    log(LOG_LEVELS["WARNING"],message)

def log_error(message):
    log(LOG_LEVELS["ERROR"],message)
    
def log_critical(message):
    log(LOG_LEVELS["CRITICAL"],message)

def log_alert(message):
    log(LOG_LEVELS["ALERT"],message)

def log_emergency(message):
    log(LOG_LEVELS["EMERGENCY"],message)

if __name__ == "__main__":
    log_info("This is a test of the logging system")