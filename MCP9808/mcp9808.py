# Copyright (c) 2014 Miguel Ercolino
# Author: Miguel Ercolino
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging
import math

# Default I2C address for device.
MCP9808_I2CADDR_DEFAULT        = 0x18

# Register addresses.
MCP9808_REG_CONFIG             = 0x01
MCP9808_REG_UPPER_TEMP         = 0x02
MCP9808_REG_LOWER_TEMP         = 0x03
MCP9808_REG_CRIT_TEMP          = 0x04
MCP9808_REG_AMBIENT_TEMP       = 0x05
MCP9808_REG_MANUF_ID           = 0x06
MCP9808_REG_DEVICE_ID          = 0x07
MCP9808_REG_RESOLUTION	       = 0x08

# Configuration register values.
MCP9808_REG_CONFIG_SHUTDOWN    = 0x0100
MCP9808_REG_CONFIG_CRITLOCKED  = 0x0080
MCP9808_REG_CONFIG_WINLOCKED   = 0x0040
MCP9808_REG_CONFIG_INTCLR      = 0x0020
MCP9808_REG_CONFIG_ALERTSTAT   = 0x0010
MCP9808_REG_CONFIG_ALERTCTRL   = 0x0008
MCP9808_REG_CONFIG_ALERTSEL    = 0x0004
MCP9808_REG_CONFIG_ALERTPOL    = 0x0002
MCP9808_REG_CONFIG_ALERTMODE   = 0x0001

class MCP9808(object):
	"""Class to represent an Adafruit MCP9808 precision temperature measurement
	board.
	"""

	def __init__(self, address=MCP9808_I2CADDR_DEFAULT, i2c=None, **kwargs):
		"""Initialize MCP9808 device on the specified I2C address and bus number.
		Address defaults to 0x18 and bus number defaults to the appropriate bus
		for the hardware.
		"""
		self._logger = logging.getLogger('MCP9808')
		if i2c is None:
			import Adafruit_GPIO.I2C as I2C
			self._i2c = I2C
		self._device = self._i2c.get_i2c_device(address, **kwargs)


	def begin(self):
		"""Start taking temperature measurements. Returns True if the device is 
		intialized, False otherwise.
		"""
		# Check manufacturer and device ID match expected values.
		mid = self._device.readU16BE(MCP9808_REG_MANUF_ID)
		did = self._device.readU16BE(MCP9808_REG_DEVICE_ID)
		self._logger.debug('Read manufacturer ID: {0:#06X}'.format(mid))
		self._logger.debug('Read device ID: {0:#06X}'.format(did))
		return mid == 0x0054 and did == 0x0400

        def getConfigReg(self):
		"""Returns the Config register value"""
		# Read Config Register value
		return self._device.readU16BE(MCP9808_REG_CONFIG)

	def clearConfigReg(self):
		"""Clear the Config Register value"""
		self._device.write16(MCP9808_REG_CONFIG, 0x0000)		

	def setTempHyst(self, thyst=0):
		"""Set the Temperature hysteresis, the valid values are 0, +1.5, +3.0, +6.0 Celsius Degrees
		if the thyst is not a valid then it will not make any modification to the register, this function
		returns a list with [a,b], a is 1 if thyst was valid and 0 if it was not, b is the new value of the 
		config register if it was successfull and if was not it returns an Error String"""
		# Read the config Register
		config = self._device.readU16BE(MCP9808_REG_CONFIG)
		# Validate thyst
		if thyst == 0:
			t = 0x0000
			new_config = (config & 0xF9FF) | t
			self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))
			self._logger.debug('Temperature Hysteresis set: {0:#06X}'.format(new_config))
			return [1, self._device.readU16BE(MCP9808_REG_CONFIG)]
		elif thyst == 1.5:
			t = 0x0200
			new_config = (config & 0xF9FF) | t
                        self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))
                        self._logger.debug('Temperature Hysteresis set: {0:#06X}'.format(new_config))
			return [1, self._device.readU16BE(MCP9808_REG_CONFIG)]
		elif thyst == 3:
			t = 0x0400
			new_config = (config & 0xF9FF) | t
                        self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))
                        self._logger.debug('Temperature Hysteresis set: {0:#06X}'.format(new_config))
			return [1, self._device.readU16BE(MCP9808_REG_CONFIG)]
		elif thyst== 6:
			t = 0x0600
			new_config = (config & 0xF9FF) | t
                        self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))
                        self._logger.debug('Temperature Hysteresis set: {0:#06X}'.format(new_config))
			return [1, self._device.readU16BE(MCP9808_REG_CONFIG)]
		else:
			return [0, 'Temperature Hysteresis is not valid, Valid Values are: 0, +1.5, +3, +6']
			self._logger.debug('Error setting the Temperature Hysteresis')

	def setShutdown(self):
		"""Set shutdown bit on the config register"""
		# Read the config Register
        	config = self._device.readU16BE(MCP9808_REG_CONFIG)
		# Set the shutdown bit
		self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(config | MCP9808_REG_CONFIG_SHUTDOWN))
		self._logger.debug('The Shutdown set: {0:#06X}'.format(config | MCP9808_REG_CONFIG_SHUTDOWN))

	def clearShutdown(self):
		"""Clear shutdown bit on the config register"""
		# Read the config Register
		config = self._device.readU16BE(MCP9808_REG_CONFIG)
		# Clear the Shutdown bit
		self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(config & ~MCP9808_REG_CONFIG_SHUTDOWN))
		self._logger.debug('The Shutdown Clear: {0:#06X}'.format(config | ~MCP9808_REG_CONFIG_SHUTDOWN))
    
    	def setCritLock(self):
		"""Set Critical lock bit on the config register, be careful once set it can only be cleared by an internal power reset"""
		# Read the config Register
		config = self._device.readU16BE(MCP9808_REG_CONFIG)
		# Set the CritLock bit
		new_config = config | MCP9808_REG_CONFIG_CRITLOCKED
		if new_config < 0x00FF:
			self._device.write16(MCP9808_REG_CONFIG, new_config << 8)
		else:
			self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))

	def setWinLock(self):
		"""Set Window lock bit on the config register, be careful once set it can only be cleared by an internal power reset"""
		# Read the config Register
		config = self._device.readU16BE(MCP9808_REG_CONFIG)
		# Set the WinLock bit
		new_config = config | MCP9808_REG_CONFIG_WINLOCKED
		if new_config < 0x00FF:
			self._device.write16(MCP9808_REG_CONFIG, new_config << 8)
		else:
			self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))
	
	def isLock(self):
		"""Check if the lock bits are set"""
		# Read the config Register
		config = self._device.readU16BE(MCP9808_REG_CONFIG) & 0x00C0
		if config == 0x00C0 or config == 0x0040 or config==0x0080:
			return True
		else:
			return False
	
	def setIntClr(self):
		"""Set Interrrupt Clear bit on the config register"""
		# Read the config Register
        	config = self._device.readU16BE(MCP9808_REG_CONFIG)
		# Set the Interrupt Clear bit
		new_config = config | MCP9808_REG_CONFIG_INTCLR
		self._logger.debug('Setting Interrupt Clear bit: {0:#06X}'.format(new_config))
		if new_config < 0x00FF:
			self._device.write16(MCP9808_REG_CONFIG, new_config << 8)
		else:
			self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))

	def clearIntClr(self):
		"""Clear Interrupt Clear bit on the config register"""
		# Read the config Register
		config = self._device.readU16BE(MCP9808_REG_CONFIG)
		# Clear the Interrupt Clear bit
		new_config = config & ~MCP9808_REG_CONFIG_INTCLR
		self._logger.debug('Clearing Interrupt Clear bit: {0:#06X}'.format(new_config))
		if new_config < 0x00FF:
			self._device.write16(MCP9808_REG_CONFIG, new_config << 8)
		else:
			self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))
	
	def setAlertStat(self):
		"""Set Alert Status bit on the config register"""
		# Read the config Register
        	config = self._device.readU16BE(MCP9808_REG_CONFIG)
		# Set the Alert Status bit
		new_config = config | MCP9808_REG_CONFIG_ALERTSTAT
		self._logger.debug('Setting Alert Status bit: {0:#06X}'.format(new_config))
		if new_config < 0x00FF:
			self._device.write16(MCP9808_REG_CONFIG, new_config << 8)
		else:
			self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))

	def clearAlertStat(self):
		"""Clear Alert Status bit on the config register"""
		# Read the config Register
		config = self._device.readU16BE(MCP9808_REG_CONFIG)
		# Clear the Alert Status bit
		new_config = config & ~MCP9808_REG_CONFIG_ALERTSTAT
		self._logger.debug('Clearing Alert Status bit: {0:#06X}'.format(new_config))
		if new_config < 0x00FF:
			self._device.write16(MCP9808_REG_CONFIG, new_config << 8)
		else:
			self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))
	
	def setAlertCtrl(self):
		"""Set Alert Control bit on the config register"""
		# Read the config Register
        	config = self._device.readU16BE(MCP9808_REG_CONFIG)
		# Set the Alert Control bit
		new_config = config | MCP9808_REG_CONFIG_ALERTCTRL
		self._logger.debug('Setting Alert Control bit: {0:#06X}'.format(new_config))
		if new_config < 0x00FF:
			self._device.write16(MCP9808_REG_CONFIG, new_config << 8)
		else:
			self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))

	def clearAlertCtrl(self):
		"""Clear Alert Control bit on the config register"""
		# Read the config Register
		config = self._device.readU16BE(MCP9808_REG_CONFIG)
		# Clear the Alert Control bit
		new_config = config & ~MCP9808_REG_CONFIG_ALERTCTRL
		self._logger.debug('Clearing Alert Control bit: {0:#06X}'.format(new_config))
		if new_config < 0x00FF:
			self._device.write16(MCP9808_REG_CONFIG, new_config << 8)
		else:
			self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))
	
	def setAlertSel(self):
		"""Set Alert Select bit on the config register"""
		# Read the config Register
        	config = self._device.readU16BE(MCP9808_REG_CONFIG)
		# Set the Alert Select bit
		new_config = config | MCP9808_REG_CONFIG_ALERTSEL
		self._logger.debug('Setting Alert Select bit: {0:#06X}'.format(new_config))
		if new_config < 0x00FF:
			self._device.write16(MCP9808_REG_CONFIG, new_config << 8)
		else:
			self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))

	def clearAlertSel(self):
		"""Clear Alert Select bit on the config register"""
		# Read the config Register
		config = self._device.readU16BE(MCP9808_REG_CONFIG)
		# Clear the Alert Select bit
		new_config = config & ~MCP9808_REG_CONFIG_ALERTSEL
		self._logger.debug('Clearing Alert Select bit: {0:#06X}'.format(new_config))
		if new_config < 0x00FF:
			self._device.write16(MCP9808_REG_CONFIG, new_config << 8)
		else:
			self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))
	
	def setAlertPol(self):
		"""Set Alert Polarity bit on the config register"""
		# Read the config Register
        	config = self._device.readU16BE(MCP9808_REG_CONFIG)
		# Set the Alert Polarity bit
		new_config = config | MCP9808_REG_CONFIG_ALERTPOL
		self._logger.debug('Setting Alert Polarity bit: {0:#06X}'.format(new_config))
		if new_config < 0x00FF:
			self._device.write16(MCP9808_REG_CONFIG, new_config << 8)
		else:
			self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))

	def clearAlertPol(self):
		"""Clear Alert Polarity bit on the config register"""
		# Read the config Register
		config = self._device.readU16BE(MCP9808_REG_CONFIG)
		# Clear the Alert Polarity bit
		new_config = config & ~MCP9808_REG_CONFIG_ALERTPOL
		self._logger.debug('Clearing Alert Polarity bit: {0:#06X}'.format(new_config))
		if new_config < 0x00FF:
			self._device.write16(MCP9808_REG_CONFIG, new_config << 8)
		else:
			self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))
	
	def setAlertMode(self):
		"""Set Alert Mode bit on the config register"""
		# Read the config Register
        	config = self._device.readU16BE(MCP9808_REG_CONFIG)
		# Set the Alert Mode bit
		new_config = config | MCP9808_REG_CONFIG_ALERTMODE
		self._logger.debug('Setting Alert Mode bit: {0:#06X}'.format(new_config))
		if new_config < 0x00FF:
			self._device.write16(MCP9808_REG_CONFIG, new_config << 8)
		else:
			self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))

	def clearAlertMode(self):
		"""Clear Alert Mode bit on the config register"""
		# Read the config Register
		config = self._device.readU16BE(MCP9808_REG_CONFIG)
		# Clear the Alert Mode bit
		new_config = config & ~MCP9808_REG_CONFIG_ALERTMODE
		self._logger.debug('Clearing Alert Mode bit: {0:#06X}'.format(new_config))
		if new_config < 0x00FF:
			self._device.write16(MCP9808_REG_CONFIG, new_config << 8)
		else:
			self._device.write16(MCP9808_REG_CONFIG, self._i2c.reverseByteOrder(new_config))

	def readTempC(self):
		"""Read sensor and return its value in degrees celsius."""
		# Read temperature register value.
		t = self._device.readU16BE(MCP9808_REG_AMBIENT_TEMP)
		self._logger.debug('Raw ambient temp register value: 0x{0:04X}'.format(t & 0xFFFF))
		# Scale and convert to signed value.
		upperByte = t & 0x0F00
		lowerByte = t & 0x00FF
		if t & 0x1000:
			temp = (((upperByte >> 8) * 16) + (lowerByte / 16.0)) * (-1)
		else:
			temp = ((upperByte >> 8) * 16) + (lowerByte / 16.0)
		return temp
	
	def getAlertOutput(self):
		"""This function will return the cause of the alert output trigger, it will return
		the bits 13 14 and 15 of the TA Register mapped into an int"""
		# Read temperature register value.
		t = self._device.readU16BE(MCP9808_REG_AMBIENT_TEMP)
		return (t & 0xE000) >> 13
	
	def setResolution(self, res = 0.0625):
		"""Set the Sensor Resolution, the resolution could be set to 0.5, 0.25, 0.125 or 0.0625 this function
		returns a list with [a,b], a is 1 if resolution is valid and 0 if it is not, b is the new value of the 
		config register if it was successfull and if was not it returns an Error String"""
		# Validate res
		if res == 0.5:
			self._device.write8(MCP9808_REG_RESOLUTION, 0x00)
			self._logger.debug('Resolution Set to: {0:#04X}'.format(0x00))
			return [1, self._device.readU16BE(MCP9808_REG_RESOLUTION)]
		elif res == 0.25:
                        self._device.write8(MCP9808_REG_RESOLUTION, 0x01)
                        self._logger.debug('Resolution Set to: {0:#04X}'.format(0x01))
			return [1, self._device.readU16BE(MCP9808_REG_RESOLUTION)]
		elif res == 0.125:
                        self._device.write8(MCP9808_REG_RESOLUTION, 0x02)
                        self._logger.debug('Resolution Set to: {0:#04X}'.format(0x02))
			return [1, self._device.readU16BE(MCP9808_REG_RESOLUTION)]
		elif res == 0.0625:
                        self._device.write8(MCP9808_REG_RESOLUTION, 0x03)
                        self._logger.debug('Resolution Set to: {0:#04X}'.format(0x03))
			return [1, self._device.readU16BE(MCP9808_REG_RESOLUTION)]
		else:
			return [0, 'Sensor Resolution is not valid, Valid Values are: 0.5, 0.25, 0.125, +0.0625']
			self._logger.debug('Error with the resolution passed')

	def getResolution(self):
		"""Get Resolution Register, return a string with the resolution configured"""
		# Read the Resolution Register
		resolution = self._device.readU8(MCP9808_REG_RESOLUTION)
		self._logger.debug('The Resolution is: {0:#06X}'.format(resolution))
		if resolution == 0x00:
			return 'Resolution is set to 0.5 Degrees Celsius'
		elif resolution == 0x01:
			return 'Resolution is set to 0.25 Degrees Celsius'
		elif resolution == 0x02:
			return 'Resolution is set to 0.125 Degrees Celsius'
		elif resolution == 0x03:
			return 'Resolution is set to 0.0625 Degrees Celsius'
			
	def setUpperTemp(self, temp=0):
		"""Set the Temperature Upper Register with a resolution of 0.25 Degree Celsius, if the temperature passed
		to the funcition is not in that resolution it will be rounded by defect to the nearest decimal resolution"""
		#Check if temp is float
		if isinstance(temp, int):
			temp = float(temp)
		#Divide Integer from decimal parts
		t = math.modf(abs(temp))
		temp_int = int(t[1])
		temp_dec = t[0]
		# Round decimal parts to 0.25 steps
		if temp_dec >= 0 and temp_dec < 0.25:
			temp_dec = 0x00
		elif temp_dec >= 0.25 and temp_dec < 0.5:
			temp_dec = 0x01
		elif temp_dec >= 0.5 and temp_dec < 0.75:
			temp_dec = 0x02
		elif temp_dec >= 0.75 and temp_dec < 1:
			temp_dec = 0x03
		#Calculate the new temperature to write
		new_temp = 0
		new_temp = ((temp_int << 4) | (temp_dec << 2)) & 0x0FFC
		#Set Sign if it is negative
		if temp < 0:
			new_temp = new_temp | 0x1000
		# Write to Register
		self._logger.debug('Raw temp set in Upper temp register: {0:#06X}'.format(new_temp))
		self._device.write16(MCP9808_REG_UPPER_TEMP, self._i2c.reverseByteOrder(new_temp))
	
	def getUpperTemp(self, temp=0):
		"""Get the Temperature Upper Register"""
		t = self._device.readU16BE(MCP9808_REG_UPPER_TEMP)
		upperByte = t & 0x0F00
		lowerByte = t & 0x00FC
		if t & 0x1000:
			temp = (((upperByte >> 8) * 16) + (lowerByte / 16.0)) * (-1)
		else:
			temp = ((upperByte >> 8) * 16) + (lowerByte / 16.0)
		return temp
		
	def setLowerTemp(self, temp=0):
		"""Set the Temperature Lower Register with a resolution of 0.25 Degree Celsius, if the temperature passed
		to the funcition is not in that resolution it will be rounded by defect to the nearest decimal resolution"""
		#Check if temp is float
		if isinstance(temp, int):
			temp = float(temp)
		#Divide Integer from decimal parts
		t = math.modf(abs(temp))
		temp_int = int(t[1])
		temp_dec = t[0]
		# Round decimal parts to 0.25 steps
		if temp_dec >= 0 and temp_dec < 0.25:
			temp_dec = 0x00
		elif temp_dec >= 0.25 and temp_dec < 0.5:
			temp_dec = 0x01
		elif temp_dec >= 0.5 and temp_dec < 0.75:
			temp_dec = 0x02
		elif temp_dec >= 0.75 and temp_dec < 1:
			temp_dec = 0x03
		#Calculate the new temperature to write
		new_temp = 0
		new_temp = ((temp_int << 4) | (temp_dec << 2)) & 0x0FFC
		#Set Sign if it is negative
		if temp < 0:
			new_temp = new_temp | 0x1000
		# Write to Register
		self._logger.debug('Raw temp set in Lower temp register: {0:#06X}'.format(new_temp))
		self._device.write16(MCP9808_REG_LOWER_TEMP, self._i2c.reverseByteOrder(new_temp))
	
	def getLowerTemp(self, temp=0):
		"""Get the Temperature Lower Register"""
		t = self._device.readU16BE(MCP9808_REG_LOWER_TEMP)
		upperByte = t & 0x0F00
		lowerByte = t & 0x00FC
		if t & 0x1000:
			temp = (((upperByte >> 8) * 16) + (lowerByte / 16.0)) * (-1)
		else:
			temp = ((upperByte >> 8) * 16) + (lowerByte / 16.0)
		return temp
	
	def setCritTemp(self, temp=0):
		"""Set the Temperature Lower Register with a resolution of 0.25 Degree Celsius, if the temperature passed
		to the funcition is not in that resolution it will be rounded by defect to the nearest decimal resolution"""
		#Check if temp is float
		if isinstance(temp, int):
			temp = float(temp)
		#Divide Integer from decimal parts
		t = math.modf(abs(temp))
		temp_int = int(t[1])
		temp_dec = t[0]
		# Round decimal parts to 0.25 steps
		if temp_dec >= 0 and temp_dec < 0.25:
			temp_dec = 0x00
		elif temp_dec >= 0.25 and temp_dec < 0.5:
			temp_dec = 0x01
		elif temp_dec >= 0.5 and temp_dec < 0.75:
			temp_dec = 0x02
		elif temp_dec >= 0.75 and temp_dec < 1:
			temp_dec = 0x03
		#Calculate the new temperature to write
		new_temp = 0
		new_temp = ((temp_int << 4) | (temp_dec << 2)) & 0x0FFC
		#Set Sign if it is negative
		if temp < 0:
			new_temp = new_temp | 0x1000
		# Write to Register
		self._logger.debug('Raw temp set in Critical temp register: {0:#06X}'.format(new_temp))
		self._device.write16(MCP9808_REG_CRIT_TEMP, self._i2c.reverseByteOrder(new_temp))
	
	def getCritTemp(self, temp=0):
		"""Get the Temperature Lower Register"""
		t = self._device.readU16BE(MCP9808_REG_CRIT_TEMP)
		upperByte = t & 0x0F00
		lowerByte = t & 0x00FC
		if t & 0x1000:
			temp = (((upperByte >> 8) * 16) + (lowerByte / 16.0)) * (-1)
		else:
			temp = ((upperByte >> 8) * 16) + (lowerByte / 16.0)
		return temp
