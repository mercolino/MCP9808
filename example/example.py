import MCP9808.mcp9808 as MCP9808
import time

sensor = MCP9808.MCP9808()

# Optionally you can override the address and/or bus number:
#sensor = MCP9808.MCP9808(address=0x20, busnum=2)

# Initialize communication with the sensor.
sensor.begin()

# Print the Config Register
sensor.clearConfigReg()
print 'Config register: {0:#06X}'.format(sensor.getConfigReg())

# Print the Resolution Register
print sensor.getResolution()

# You could change the resolution of the sensor
sensor.setResolution(0.25)

# Set the Window and Critical temperature to use the alert output pin
sensor.setLowerTemp(20.0)
sensor.setUpperTemp(30.00)
sensor.setCritTemp(33.0)

# Enable the Alert pin, Remember that you should use a pullup resistor, for further information
# read the MCP9808 Datasheet
sensor.setAlertCtrl()

print "Window Temperature: %d - %d" %(sensor.getLowerTemp(), sensor.getUpperTemp())
print "Critical Temperature: %d" %(sensor.getCritTemp())

# Print the Config Register, Note how the config register change by setting the Alert Control pin
print 'Config register: {0:#06X}'.format(sensor.getConfigReg())

# Loop printing measurements every second.
print 'Press Ctrl-C to quit.'
while True:
	temp = sensor.readTempC()
	# Read the temperature
	print 'Temperature: {0:0.3F}*C'.format(temp)
	# Read the 3 bits to know why the alert is set, read the datasheet to kno more
	print 'Sensor Alert Output: {0:#05b}'.format(sensor.getAlertOutput())
	time.sleep(1.0)
