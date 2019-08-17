# revised 08-17-2019 
#!/usr/bin/python
#--------------------------------------
#
#                mypi.py
#  Functions to display Pi properties
#
#  If called directly outputs :
#  - Pi Model
#  - Revision number
#  - Serial number
#  - Python version
#  - I2C,SPI and Bluetooth status
#  - Mac address
#  - IP address
#  - CPU temperature
#  - GPU temperature
#
# Author : Matt Hawkins
# Date   : 06/12/2017 Revised 08-17-2019 for my Pi Zero W (by kflmiami420)
#
# https://www.raspberrypi-spy.co.uk/
#
#--------------------------------------

import platform
import subprocess
import os
import socket

from uuid import getnode as get_mac

# Define functions

def getModel():
  # Extract Pi Model string
  try:
    mymodel = open('/proc/device-tree/model').readline()
  except:
    mymodel = "Error"

  return mymodel

def getSerial():
  # Extract serial from cpuinfo file
  mycpuserial = "Error"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        mycpuserial = line[10:26]
    f.close()
  except:
    mycpuserial = "Error"

  return mycpuserial

def getRevision():
  # Extract board revision from cpuinfo file
  myrevision = "Error"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:8]=='Revision':
        myrevision = line[11:-1]
    f.close()
  except:
    myrevision = "Error"

  return myrevision

def get_local_ip_address(target):
  ipaddr = ''
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((target, 8000))
    ipaddr = s.getsockname()[0]
    s.close()
  except:
    pass

  return ipaddr

def getCPUtemp():
  # Extract CPU temp
  try:
    temp = subprocess.check_output(['vcgencmd','measure_temp'])
    temp = temp[5:-3]
  except:
    temp = '0.0'
  temp = '{0:.2f}'.format(float(temp))
  return str(temp)

def getGPUtemp():
  # Extract GPU temp
  try:
    temp = subprocess.check_output(['cat','/sys/class/thermal/thermal_zone0/temp'])
    temp = float(temp)/1000
  except:
    temp = 0.0
  temp = '{0:.2f}'.format(temp)
  return temp

def getRAM():
  # free -m
  output = subprocess.check_output(['free','-m'])
  lines = output.splitlines()
  line  = str(lines[1])
  ram = line.split()
  # total/free  
  return (ram[1],ram[3])

def getDisk():
  # df -h
  output = subprocess.check_output(['df','-h'])
  lines = output.splitlines()
  line  = str(lines[1])
  disk  = line.split()
  # total/free
  return (disk[1],disk[3])

def getCPUspeed():
  # Get CPU frequency
  try:
    output = subprocess.check_output(['vcgencmd','get_config','arm_freq'])
    output = output.decode()
    lines = output.splitlines()
    line  = lines[0]
    freq = line.split('=')
    freq = freq[1]
  except:
    freq = '0'
  return freq

def getUptime():
  # uptime
  # tupple uptime, 5 min load average
  return 0

def getPython():
  # Get current Python version
  # returns string
  pythonv = platform.python_version()
  return pythonv

def getSPI():
  # Check if SPI bus is enabled
  # by checking for spi_bcm2### modules
  # returns a string
  spi = "False"
  try:
    c=subprocess.Popen("lsmod",stdout=subprocess.PIPE)
    gr=subprocess.Popen(["grep" ,"spi_bcm2"],stdin=c.stdout,stdout=subprocess.PIPE)
    output = gr.communicate()[0]
    if output[:8]=='spi_bcm2':
      spi = "True"
  except:
    pass
  return spi

def getI2C():
  # Check if I2C bus is enabled
  # by checking for i2c_bcm2### modules
  # returns a string
  i2c = "False"
  try:
    c=subprocess.Popen("lsmod",stdout=subprocess.PIPE)
    gr=subprocess.Popen(["grep" ,"i2c_bcm2"],stdin=c.stdout,stdout=subprocess.PIPE)
    output = gr.communicate()[0]
    if output[:8]=='i2c_bcm2':
      i2c = "True"
  except:
    pass
  return i2c

def getBT():
  # Check if Bluetooth module is enabled
  # returns a string
  bt = "False"
  try:
    c=subprocess.Popen("lsmod",stdout=subprocess.PIPE)
    gr=subprocess.Popen(["grep" ,"bluetooth"],stdin=c.stdout,stdout=subprocess.PIPE)
    output = gr.communicate()[0]
    if output[:9]==b'bluetooth':
      bt = "True"
  except:
    pass
  return bt

if __name__ == '__main__':
  # Script has been called directly

  myRAM = getRAM()
  myDisk = getDisk()
  host = socket.gethostname()
  mac = get_mac()

  macString = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))


  print("----------------------------------------")
  print("Pi Model             : " + getModel())
  print("----------------------------------------")
  print("Host                 :", host)
  print("----------------------------------------")
  print("System               : " + platform.platform())
  print("Revision Number      : " + getRevision())
  print("Serial Number        : " + getSerial())
  print("Python version       : " + platform.python_version())
  print("----------------------------------------")
  print("I2C enabled          : " + getI2C())
  print("SPI enabled          : " + getSPI())
  print("Bluetooth enabled    : " + getBT())
  print("----------------------------------------")
  print("CPU Clock            : " + getCPUspeed() + "MHz")
  print("CPU Temperature      : " + getCPUtemp() + u"\u00b0" +"C")
  print("GPU Temperature      : " + getGPUtemp() + u"\u00b0" +"C")
  print("RAM (Available)      : " + myRAM[0] + "MB (" + myRAM[1] + "MB)")
  print("Disk (Available)     : " + myDisk[0] + " (" + myDisk[1] + ")")
  print("----------------------------------------")
  print("Wireless IP Address  : " + get_local_ip_address('10.0.1.1'))
  print("Wireless MAC Address : " + macString )

