#-  File: grove_gas_sensor_mq5.py
#-  Title: Gas MQ5 Sensor
#-  Description: An application to record a gas reading
#-  Usage: Run the script and provide with the environment variable "AVERAGE_COUNT", if not, it will be assigned the variable '4'.
#-  Author: Reem Khider
#-  Sources : Gas Sensor Readings based (https://wiki.seeedstudio.com/Grove-Gas_Sensor-MQ5/)
#-  contribution towards the determining gas name : Kieran Best

import sys
import time
import os
from grove.adc import ADC
from lib import logger
from pathlib import Path

class GroveGasSensorMQ5:
    def __init__(self, channel):
        self.channel = channel
        self.adc = ADC()
    @property
    def MQ5(self):
        # get raw senor reading
        value = self.adc.read(self.channel)
        return value

# determine exact gas name based on created readings.
# code and logic is taken from and based on (https://github.com/CompEng0001/IoT-and-Our-Schools-Environments-for-Education/blob/master/DashBoardv2.html)
Grove = GroveGasSensorMQ5
def getGasDetails(average):
    average = f"{getClosestGas(average):.2f}"
    GasLookupTable = {
        "TwoHunPPM": ["0.70", "0.95", "1.80", "3.50", "3.90"],
        "FiveHunPPM": ["0.48", "0.68", "1.30", "2.90", "3.30"],
        "EightHunPPM": ["0.39", "0.56", "1.10", "2.70", "3.00"],
        "OneThouPPM": ["0.37", "0.52", "1.00", "2.60", "2.90"],
        "OneSixThouPPM": ["0.30", "0.45", "0.89", "2.40", "2.80"],
        "TwoThouPPM": ["0.28", "0.40", "0.81", "2.30", "2.70"],
        "ThreeThouPPM": ["0.24", "0.34", "0.78", "2.10", "2.60"],
        "FiveThouPPM": ["0.19", "0.28", "0.73", "1.80", "2.50"],
        "TenThouPPM": ["0.16", "0.21", "0.68", "1.60", "2.35", "6.50"],
        "GasNames": ["LPG", "Methane (CH4)", "Hydrogen (H2)", "Ethanol/Methanol", "Carbon-dioxide (C0)", "Normal Air"],
        "PPM": [200, 500, 800, 1000, 1600, 2000, 3000, 5000, 10000]
    }

    counter = 0
    for key in GasLookupTable:
        try:
            GasLookupTable[key].index(average)
            gasIndex = GasLookupTable[key].index(average)
            gasDetails = GasLookupTable["GasNames"][gasIndex]
            gasPPM = f"{GasLookupTable['PPM'][counter]} PPM"
            return gasDetails, gasPPM
        except ValueError:
            pass
        counter += 1
    return "", ""

def getClosestGas(num):
    # sorted array
    gasArray = [0.16, 0.19, 0.21, 0.24, 0.28, 0.28, 0.3, 0.34, 0.37, 0.39, 0.4, 0.45, 0.48, 0.52, 0.56, 0.68, 0.68, 0.7, 0.73, 0.78, 0.81, 0.89, 0.95, 1.0, 1.1, 1.3, 1.6, 1.8, 1.8, 2.1, 2.3, 2.35, 2.4, 2.5, 2.6, 2.6, 2.7, 2.7, 2.8, 2.9, 2.9, 3.0, 3.3, 3.5, 3.9, 6.5]
    closest = gasArray[0]
    for i  in range(len(gasArray)):
        closestDiff = abs(num - closest)
        currentDiff = abs(num - gasArray[i])
        if currentDiff < closestDiff:
            closest = gasArray[i]

    # returns first element that is closest to number
    return closest

def main():
    logger.log_setup(5,str(Path(os.environ.get("LOGS_PATH","log"), "gas.log")))

    if len(sys.argv) < 2:
        print('Usage: {} adc_channel'.format(sys.argv[0]))
        sys.exit(1)

    #getting the port number that the gas plugged in
    portNum = int(sys.argv[1])
    sensor = GroveGasSensorMQ5(portNum)

    #S_Val=12  //sensor reading value
    # #S_Volt= S_Val / 1024*5
    # #RS_Air= (5 - S_Volt) / S_Vol   //The value of RS via in a clean air
    # R0 = RS_Air / 6.5 = 12.97436  //The ratio of RS_Air/R0 is 6.5 in a clean air from Graph
    R0= 12.97436

    # getting the average value of the sensor reading to get the gas concentration of gas from the graph in the datasheet
    average=0
    count = int(os.environ.get("AVERAGE_COUNT", "4"))
    for _ in range(0, count+1):
        sensorValue= sensor.MQ5  # sensor reading value
        sensorVolt= sensorValue/1024*5
        RS_Gas= (5-sensorVolt)/sensorVolt
        ratio= RS_Gas/R0
        average += ratio
        time.sleep(.3)

    average=average/count
    gasDetails,gasPPM = getGasDetails(average)
    logger.log_notice('Gas {0:.2f}, Gas Name {1}, Gas PPM {2}'.format(average,gasDetails,gasPPM))

if __name__ == '__main__':
    main()

