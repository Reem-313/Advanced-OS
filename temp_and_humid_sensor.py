#-  File: temp_and_humid_sensor.py
#-  Title: Temperature and Humidity Sensor
#-  Description: An application to record the temperature and humidity
#-  Usage: Run the script and provide with the environment variable "AVERAGE_COUNT", if not, it will be assigned the variable '4'.
#-  Author: Kieran Best

#!/usr/bin/python3
# Import necessary libraries
import seeed_dht
import time
import os
from pathlib import Path
from lib import logger


# Temperature and Humidity Sensor Readings (https://wiki.seeedstudio.com/Grove-TemperatureAndHumidity_Sensor/)

sensor = seeed_dht.DHT(seeed_dht.DHT.DHT_TYPE["DHT11"], 5) # DHT type 22, pin 5

logger.log_setup(5,str(Path(os.environ.get("LOGS_PATH","log"), "temp_and_humid.log"))) # set path for output of sensors to logging file

# Obtain sensor readings
humidity = 0
temperature = 0
count = int(os.environ.get("AVERAGE_COUNT", "4"))
for repetitions in range(0,count + 1):
    humi, temp = sensor.read()
    humidity = humidity + humi
    temperature = temperature + temp
    time.sleep(.3)
humidity = humidity/count
temperature = temperature/count

# Logging output
# Sensors working correctly
if(humidity > 20 and humidity < 80 and temperature > 0 and temperature < 50): #dht11 operating range
    logger.log_notice('Humidity {0:.1f}%, Temperature {1:.1f}C'.format(humidity, temperature))
# Temperature sensor working correctly but humidity failed
elif(humidity <= 20 or humidity >= 80 and temperature > 0 and temperature < 50):
    logger.log_critical('Humidity sensor has failed, Temperature {0:.1f}C'.format(temperature))
# Humidity sensor working correctly but temperature failed
elif(temperature <= 0 or temperature >= 50 and humidity > 20 and humidity < 80):
    logger.log_critical('Temperature sensor has failed, Humidity {0:.1f}%'.format(humidity))
# Temperature and humidity sensor failed
else:
    logger.log_critical('Both sensors have failed')
