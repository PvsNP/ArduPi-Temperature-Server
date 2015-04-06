#############################################################
ARDUINO TEMPERATURE SENSORS DATA RETRIEVING
#############################################################

Pay attention: the ardu_sense.ino included into this folder
is referred to a particular implementation of the temperature
data retrieving:

HARDWARE:
2 x LM35DZ  -> their meaning value is the value serial printed
Arduino Uno Rev.3 Board

SOFTWARE:
baud_rate = 9600
conversion_ratio = 9.31 
sleep_time = 6000 milliseconds -> 60000 milliseconds for each reading