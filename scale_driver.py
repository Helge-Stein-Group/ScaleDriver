import serial
import time


class scaleError(Exception):
    def __init__(self, message):
        super().__init__(message)



class scale():

    ESC = chr(27).encode("utf-8")
    CR = chr(13).encode("utf-8")
    LF = chr(10).encode("utf-8")

    CMD_PRINT = b"P"
    CMD_TARA = b"T"

    def __init__(self,conf):
        self.ser = serial.Serial(conf['port'], conf['baud'], timeout=conf['timeout'])

    def send(self, command):
        """ Sends a command to the scale. """
        self.connection.write(ESC + command + CR + LF)

    def readline(self):
        """ Reads bytes from the serial connection until a newline. """
        return self.connection.readline()

    def get(self, command):
        """ Sends a command and returns the available data. """
        self.send(command)
        return self.readline()
        
    def checkConnection(self):
        """ Checks if the scale is connected. """
        

    def getWeight(self):
        """ Gets the weight from the scale. """
        raw_data = self.get(CMD_PRINT)
        if raw_data:
            return parse_measurement(raw_data)
        else:
            # propably serial connection timeout
            raise TimeoutError
        

    def parse_measurement(raw_data):
        ''' Gets the raw data from the scale and parses it for the weight as a float. '''
        data = raw_data.decode("utf-8").strip()
        if len(data) > 15:
            return float(re.findall("\d+\.\d+", data))
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






    def parse_measurement(raw_data):
        """ parses the raw data from a measurement """
        if len(raw_data) <= 16:
            return _parse_16_char_output(raw_data)
        else:
            return _parse_22_char_output(raw_data)


    def _parse_22_char_output(raw_data):
        """ parse a 16 character measurement output

        The scale can be set to return two different types of output. This
        function parses a 16 character output.
        """

        mode = raw_data[:6].strip()
        rest = raw_data[6:]

        return _parse_16_char_output(rest, mode)

    def _is_message(raw_data):
        """ returns the message that occured in a measurement or False """
        for identifier in ("high", "low", "cal", "err", "--"):
            if identifier in raw_data.lower():
                return True
        return False

    def _parse_16_char_output(raw_data, mode="unknown"):
        """ parse a 16 character measurement output

        The scale can be set to return two different types of output. This
        function parses a 16 character output.
        """

        if _is_message(raw_data):
            msg = raw_data.strip()
            return Measurement(None, None, None, None, msg)

        raw_data = _remove_calibration_note(raw_data)

        sign = raw_data[0].strip()
        value_and_unit = raw_data[1:].strip()
        parts = value_and_unit.rsplit(" ", 1)
        raw_value = parts[0]
        value = sign + "".join(raw_value.split())

        if len(parts) == 2:
            unit = parts[1]
            stable = True
        else:
            unit = None
            stable = False

        return Measurement(mode, value, unit, stable, None)


    def _remove_calibration_note(raw_data):
        """ adjusts the raw data string if a calibration note is present

        According to the manual, this should not happen in SBI mode of the
        scale. This is included to prevent hiccups but probably not handled
        the right way....

        The data with a calibration node on in put and output of this method

        in:  "+123.4567[8]g  "
        out: "+123.45678  g  "

        """
        if "[" in raw_data:
            raw_data = raw_data.replace("[", "").replace("]", "  ")
        return raw_data

