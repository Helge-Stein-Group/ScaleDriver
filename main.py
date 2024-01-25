import serial
import time
from scale_driver import Scale

def main():
   scale = Scale('COM7',9600,timeout=3)
   print(scale.getWeight())
   scale.close()


if __name__ == "__main__":
    main()
