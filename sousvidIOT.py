# nicholas.h.mcgill@gmail.com

# Run this first to set up the DS18B20
# sudo modprobe w1-gpio && sudo modprobe w1_therm

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

        return temp_c, temp_f
	
# Main
while True:

    try:
        targetTemp=int(raw_input('Enter target temp in F:'))
        s = 'Setting sights for ' + repr(targetTemp) + 'F'
        print s
    except ValueError:
        print "Not a number"
    
    while True:
        try:
            try:
                temp_c, temp_f = read_temp()
            except TypeError:
                # Handle failures
		print 'temp fail'
            diff = targetTemp - temp_f
	    s_temp_f = "%.3f" % temp_f
	    if diff > 0:
                GPIO.output(SSR_PIN, 1)
                heater_on = True
	        s_diff = "%.3f" % diff
                s = s_temp_f + ':' + s_diff + ' below target. capn, we are putting on more heat!'
                print s
            else:
                GPIO.output(SSR_PIN, 0)
                heater_on = True
	        s_diff = "%.3f" % (-1*diff)
                s = s_temp_f + ':' + s_diff + ' above target. whoa nelly! pump the brakes'
                print s
            time.sleep(0)
        # Handle Ctrl-C
        except KeyboardInterrupt:
            GPIO.cleanup()
