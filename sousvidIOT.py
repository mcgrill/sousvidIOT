# nicholas.h.mcgill@gmail.com

# Imports
import os
import glob
import time
import RPi.GPIO as GPIO

# GPIO Setups
SSR_PIN = 12			# SSR = Solid State Relay
GPIO.setmode(GPIO.BOARD)
GPIO.setup(SSR_PIN, GPIO.OUT)
#pin 18, or GPIO12

targetTemp = 80

# Make the DS18B20 work correctly on the pi
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# Functions
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0

        if temp_f <= targetTemp:
            GPIO.output(SSR_PIN, 1)
            heater_on = True
        else:
            GPIO.output(SSR_PIN, 0)
            heater_on = True

        return temp_c, temp_f, heater_on
	
# Main
while True:

    try:
        targetTemp=int(raw_input('Enter target temp in F:'))
        s = 'Setting sights for' + repr(targetTemp) + 'F'
    except ValueError:
        print "Not a number"
    
    while True:
        try:
            print(read_temp())
            time.sleep(0)
        # Handle Ctrl-C
        except KeyboardInterrupt:
            GPIO.cleanup()