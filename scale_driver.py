import serial
import time
import sys
import os
import re

class scaleError(Exception):
    def __init__(self, message):
        super().__init__(message)



class Scale():

   
    ESC = chr(27).encode("utf-8")
    CR = chr(13).encode("utf-8")
    LF = chr(10).encode("utf-8")

    CMD_PRINT = b"P"
    CMD_TARA = b"T"

    def __init__(self,conf,baud,timeout):
        """ Initializes the scale and connects to the serial port. """
        self.conf = conf
        self.baud = baud
        self.timeout = timeout
        try: 
            self.ser = serial.Serial(conf, baud, timeout=timeout)
        except serial.SerialException:
            print('Unable to connect to the scale. Check the com port and try again.')
            sys.exit(1) 

    def close(self):
        """ Closes the serial connection. """
        self.ser.close()
    
    def send(self, command):
        """ Sends a command to the scale. """
        self.ser.write(Scale.ESC + command + Scale.CR + Scale.LF)

    def readline(self):
        """ Reads bytes from the serial connection until a newline. """
        return self.ser.readline()

    def get(self, command):
        """ Sends a command and returns the available data. """
        self.send(command)
        return self.readline()
        
    def checkConnection(self):
        """ Checks if the scale is connected. """
        try:
            self.get(Scale.CMD_PRINT)
            return True
        except TimeoutError:
            return False

    def getWeight(self):
        """ Gets the weight from the scale. """
        raw_data = self.get(Scale.CMD_PRINT)
        if raw_data:
            return self.parse_measurement(raw_data)
        else:
            # propably serial connection timeout
            raise TimeoutError
        
    def parse_measurement(self,raw_data):
        ''' Gets the raw data from the scale and parses it for the weight as a float. '''
        data = raw_data.decode("utf-8").strip()
        if len(data) > 15:
            return float(re.findall("\d+\.\d+", data)[0])
        else:
            raise scaleError('Unable to read messege from the scale.')
        
        
    def collectWeightTillTime(self, CollectTime: int, TimeBetweenMeasure: int):
        ''' Uses the get function and collects weight data for a specified amount of time.'''
        weightData = []
        timeData = []
        timeStart = time.time()
        timeCurrent = time.time()
        while timeCurrent - timeStart < CollectTime:
            weightData.append(self.getWeight())
            timeCurrent = time.time()
            timeData.append(timeCurrent - timeStart)
            time.sleep(TimeBetweenMeasure)

        return weightData, timeData


    def collectWeightTillMax(self, MaxWeight: int, TimeBetweenMeasure: int):
        ''' Uses the get function and collects weight data for a specified amount of time.'''
        weightData = []
        timeData = []
        timeStart = time.time()
        timeCurrent = time.time()
        weightData.append(self.getWeight())
        timeData.append(timeCurrent - timeStart)
        while weightData[-1] < MaxWeight:
            weightData.append(self.getWeight())
            timeCurrent = time.time()
            timeData.append(timeCurrent - timeStart)

        return weightData, timeData 