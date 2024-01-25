#This is an example file for a serial connection to your scale.
from scale_driver import Scale

my_scale = Scale('COM7',9600,timeout=3) #Change this to your sepecific serial port and baud rate

print(my_scale.checkConnection())
print(my_scale.getWeight())
   
my_scale.close()