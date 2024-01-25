import serial
import time
from scale_driver import Scale

def main():
   scale = Scale('COM7',9600,3)
   print(scale.get(Scale.CMD_PRINT))
   print(scale.getWeight())
   scale.collectWeightTillMax(5,0.1)
   scale.close()


if __name__ == "__main__":
    main()
