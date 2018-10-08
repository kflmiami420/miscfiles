#  This version is modded for Pi Zero W Oct 2018
#!/usr/bin/python
#--------------------------------------
#
#                mypizero.py
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
# Date   : 06/12/2017
#
# https://www.raspberrypi-spy.co.uk/
#
#--------------------------------------
#!/usr/bin/python

import platform
import subprocess
import os

from twython import Twython



def getModel():

  try:
    mymodel = open('/proc/device-tree/model').readline()
  except:
    mymodel = "Error"

  return mymodel

def getSerial():

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

def getEthName():

  try:
    for root,dirs,files in os.walk('/sys/class/net'):
      for dir in dirs:
        if dir[:3]=='enx' or dir[:3]=='eth':
          interface=dir
  except:
    interface="None"
  return interface

def getMAC(interface='eth0'):

  try:
    line = open('/sys/class/net/%s/address' %interface).read()
  except:
    line = "None"
  return line[0:17]

def getIP(interface='eth0'):

  try:
    filename = 'ifconfig_' + interface + '.txt'
    os.system('ifconfig ' + interface + ' > /home/pi/' + filename)
    f = open('/home/pi/' + filename, 'r')
    line = f.readline()
    line = f.readline()
    line = line.strip()
    line = line.strip()
    f.close()

    if line.startswith('inet '):
      a,b,c = line.partition('inet ')
      a,b,c = c.partition(' ')
      a=a.replace('addr:','')
    else:
      a = 'None'

    return a

  except:
    return 'Error'

def getCPUtemp():

  try:
    temp = subprocess.check_output(['vcgencmd','measure_temp'])
    temp = temp[5:-3]
  except:
    temp = '0.0'
  temp = '{0:.2f}'.format(float(temp))
  return str(temp)

def getGPUtemp():

  try:
    temp = subprocess.check_output(['cat','/sys/class/thermal/thermal_zone0/tem$
    temp = float(temp)/1000
  except:
    temp = 0.0
  temp = '{0:.2f}'.format(temp)
  return temp

def getRAM():

  output = subprocess.check_output(['free','-m'])
  lines = output.splitlines()
  line  = str(lines[1])
  ram = line.split()

  return (ram[1],ram[3])

def getDisk():

  output = subprocess.check_output(['df','-h'])
  lines = output.splitlines()
  line  = str(lines[1])
  disk  = line.split()

  return (disk[1],disk[3])

def getCPUspeed():

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


  return 0

def getPython():


  pythonv = platform.python_version()
  return pythonv
                                    
def getSPI():

  spi = "False"
  try:
    c=subprocess.Popen("lsmod",stdout=subprocess.PIPE)
    gr=subprocess.Popen(["grep" ,"spi_bcm2"],stdin=c.stdout,stdout=subprocess.P$
    output = gr.communicate()[0]
    if output[:8]=='spi_bcm2':
      spi = "True"
  except:
    pass
  return spi
  
def getI2C():

  i2c = "False"
  try:
    c=subprocess.Popen("lsmod",stdout=subprocess.PIPE)
    gr=subprocess.Popen(["grep" ,"i2c_bcm2"],stdin=c.stdout,stdout=subprocess.P$
    output = gr.communicate()[0]
    if output[:8]=='i2c_bcm2':
      i2c = "True"
  except:
    pass
  return i2c

def getBT():

  bt = "False"
  try:
    c=subprocess.Popen("lsmod",stdout=subprocess.PIPE)
    gr=subprocess.Popen(["grep" ,"bluetooth"],stdin=c.stdout,stdout=subprocess.$
    output = gr.communicate()[0]
    if output[:9]==b'bluetooth':
      bt = "True"
  except:
    pass
  return bt

if __name__ == '__main__':

  myRAM = getRAM()
  myDisk = getDisk()
  ethName = getEthName()

  print("----------------------------------------")
  print("Pi Model             : " + getModel())
  print("----------------------------------------")
  print("System               : " + platform.platform())
  print("Revision Number      : " + getRevision())
  print("Serial Number        : " + getSerial())
  print("Python version       : " + platform.python_version())
  print("----------------------------------------")
  print("I2C enabled          : " + getI2C())
  print("SPI enabled          : " + getSPI())
  print("----------------------------------------")
  print("Ethernet Name        : " + ethName)
  print("Ethernet MAC Address : " + getMAC(ethName))
  print("Ethernet IP Address  : " + getIP(ethName))
  print("Wireless MAC Address : " + getMAC('wlan0'))
  print("Wireless IP Address  : " + getIP('wlan0'))
  print("----------------------------------------")
  print("CPU Clock            : " + getCPUspeed() + "MHz")
  print("CPU Temperature      : " + getCPUtemp() + u"\u00b0" +"C")
  print("GPU Temperature      : " + getGPUtemp() + u"\u00b0" +"C")
  print("RAM (Available)      : " + myRAM[0] + "MB (" + myRAM[1] + "MB)")
  print("Disk (Available)     : " + myDisk[0] + " (" + myDisk[1] + ")")
  print("----------------------------------------")
                      
                        
                        
                        
                                    
