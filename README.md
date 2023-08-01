# U14553-Bit Lords

## 👋Introduction
 This project is to implement a system that can monitor the engineering spaces environment with constrained resources, for the Operations Manager at CCCU Engineering to support the development of smart systems for Industry 4 and 5, including the built environment. The devices used for monitoring are to send data to edge nodes for processing and then transmit the processed data to cloud storage within the CCCU network.

## 🏗️ Prerequisites
To run a Raspberry Pi we need the following
* Ubuntu Server : Ubuntu Server version 22.04 has been used with the following requirements:
    - RAM: 512MB
    - CPU: 1 GHz
    - Storage: 1 GB disk space (1.75 GB for all features to be installed)

* Camera Module V2
* Grove - Temperature & Humidity Sensor (DHT11) (Digital - DX)
* Grove - Gas Sensor(MQ5) (Analog - AX)
* GPIO On Ubuntu
* Raspberry Pi 4
* GrovePi


## 🔧 Installation
- Install [Ubuntu 22.04](https://ubuntu.com/download/raspberry-pi) OS for Raspberry Pi
- [Clone repo](https://github.com/cccu-uk/smartsystemsmonitor-bit-lords/tree/main) to "/home/pi/project"
- run the `install.sh` file as root user
- Run autorun.sh to install required devices
    - Raspberry Pi Camera version 4 - python-opencv==4\
    - Grove library for the Raspberry hat - `git+https://github.com/Seeed-Studio/grove.py`
    - Temperature and Humidity Sensor - `git+https://github.com/Seeed-Studio/Seeed_Python_DHT`
- Plug senors into defined ports
    - Camera - "Camera"
    - Temperature and Humidity Sensor - "pin D5"
    - Gas Sensor - "A0"
- To test if devices are functional do:
    - Camera:
        - set environment variable "CAMERA_OUTPUT_DST" to where you want images to be stored
        - "./pi_cam_capture.py"
        - Download image from stored location
    - Temperature and Humidity Sensor:
        - "./temp_and_humid_sensor.py"
        - "tail -1 log/gas.log"
    - Gas Sensor:
        - "grove_gas_sensor_mq5.py 0"
        - "tail -1 logs.temp_and_humid.log"
## 💡Other:
### Logging
To use the logger library it must be first saved in a lib file in your project directory. As such an example of the file structure layout can be seen below.

```
Project_Folder/
├─ lib/
│  ├─ logger.sh
│  ├─ logger.py
├─ Project_Files
```

#### Levels
There are several different logging levels, these can be seen below:

```log
[OFF] = 8
[DEBUG] = 7
[INFO] = 6
[NOTICE] = 5
[WARNING] = 4
[ERROR] = 3
[CRITICAL] = 2
[ALERT] = 1
[EMERGENCY] = 0
```

#### Usage: Python
To import the library into your python code you can use:

```python
from lib import logger
```

This imports our library from lib into the code. We can then setup the logging with the following command:

```python
logger.log_setup(<Default logging level>,<Path to log location/filename>)
#Example:
logger.log_setup(5,"logs/log.log")
```

To add to the logging file you can use the following line of code:

```python
logger.<log_level>(<log message>)
#Example of critical error:
logger.log_critical("No path set. Set Path. Exited")
#Example of notice log:
logger.log_notice("Capture Taken")
```
You can log at any of the levels that were listed above. To disable logging you can use "OFF" or 8.

#### Usage Bash
The bash library can be used by sourcing the file inside of another script.

```bash
#!/usr/bin/env bash

source ./lib/logger.sh

# Set level & log file destination

# LOG_LEVEL=<level number>
# LOG_FILE=<log file-path>

# Log something
# LOG_<level name (caps)> "<message>"

# Example of critical log:
LOG_CRITICAL "No path set. Set Path. Exited"
# Example of notice log:
LOG_NOTICE "Capture Taken"
```

## 👫 Contributors
### __Leo Spratt__ (_Project Manager_):
- Installed OS
- `lib/logger.sh`
- `autorun.sh`
- `updater.sh`
- Bash logger docs

### __Joshua Yuill__:
My contributions to this project were as follows,
- I wrote the script that is used to take pictures with the pi's camera [pi_cam_capture.py](pi_cam_capture.py)
- I also wrote the python-based logging library to log program functions [logger.py](lib/logger.py)
- I wrote the logging.py library documentation on the readme file
### __Kieran Best__:
My contributions to this project were as follows:
- I created the script to record the temperature and humidity sensor readings [temp_and_humid_sensor.py](temp_and_humid_sensor.py)
- I wrote the "Installation" within the [README.md](README.md)
- I contributed to Reem's gas sensor reading with accessing gas names based on created readings.
- I wrote the backup script [backup.sh](backup.sh)
### __Reem Khider__:
My contributions to this project were as follows:
- I created the script to record the gas sensor readings [grove_gas_sensor_mq5.py](grove_gas_sensor_mq5.py)
- I wrote the "Introduction" and the "Prerequisites" within the [README.md](README.md)
- I wrote the script to control the cpu speed [cpu_control.sh](lib/cpu_control.sh)
- I wrote the script to take measurements from the sensors and camera [capture_readings.sh](capture_readings.sh)
