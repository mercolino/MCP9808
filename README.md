# MCP9808

If you need more help please visit https://itandsecuritystuffs.wordpress.com/2015/01/18/python-library-for-he-mcp9808-sensor-temperature/

MCP9808 is a python library that allows to interact with the MCP9808
temperature sensor, this library gives you access to all the registers
in the MCP9808 sensor, and there are methods that will allow you to access
the individual bits of the config register, allowing you to configure the IC
to compare temperature, set hysteresis, shutdown and lock the IC.

This Library was developed using as base the MCP9808 Adafruit library developed by Tony DiCola
that however only had the begin method and the readTemp method and didn't give you access to the
rest of the registers if you are interesetd in see the Adafruit's library you could see it here::

https://github.com/adafruit/Adafruit_Python_MCP9808


## Installation

Install this library with:

    `sudo python setup.py install`
    
To uninstall it use:

	`sudo pip uninstall MCP9808`

### Requirements

https://github.com/adafruit/Adafruit_Python_GPIO


## How to use the Library

First you should import the library using:

    `import MCP9808.mcp9808 as mcp`

Then you need to instantiate the object:

    `sensor = mcp.MCP9808()`
    
Then you could call the methods using the object recently created, for example:
```
    sensor.clearConfigReg() # Method to clear the config Register
    sensor.setResolution(0.25) # Method used to set the resolution of the sensor
```
There are some things that you should keep in mind:

- When using the method **setTempHyst(thyst)** the thyst value should be in the list [0, +1.5, +3.0, +6.0]
- When using the method **setResolution(res)** the rest value should be in the list [0.5, 0.25, 0.125 or 0.0625]
- When using the methods **setUpperTemp(temp)**, **setLowerTemp(temp)** and **setCritTemp(temp)** 
the temp value should be written to the register in steps of 0.25 degree Celsius, so every temperature passed as value
will be rounded by defect to the nearest decimal, for example: 20.40 will be written in the register as 20.25,
20,55 will be written in the register as 20.50 and 20.99 will be rounded to 20.75 degrees.
- There are some conditions when the shutdown and lock bits are set that would not allow to modify some registers or bit inside register
please refer to the Datasheet to see how it works.

In the example folder you will find an example of the use of this Library.

