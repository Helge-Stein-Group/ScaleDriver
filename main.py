import serial
import time
from scale_driver import Scale

def main():
   scale = Scale('COM7',9600,3)
#    print(scale.get(Scale.CMD_PRINT))
   print(scale.getWeight())
#    print(scale.checkConnection())
   scale.close()


if __name__ == "__main__":
    main()
