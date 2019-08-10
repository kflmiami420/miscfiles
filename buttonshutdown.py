#!/usr/bin/python
#--------------------------------------
#    ___  ___  _ ____          
#   / _ \/ _ \(_) __/__  __ __ 
#  / , _/ ___/ /\ \/ _ \/ // / 
# /_/|_/_/  /_/___/ .__/\_, /  
#                /_/   /___/   
#
#  RetroPie Shutdown Button Script
#
# This script enables a RetroPie based
# system to shutdown by pressing a button
# without needing to use the menu.
# 
# It uses the GpioZero library and is based on:
# https://gpiozero.readthedocs.io/en/stable/recipes.html#shutdown-button
#
# Please see https://www.raspberrypi-spy.co.uk/
# for more information.
#
# Author : Matt Hawkins
# Date   : 18/03/2018
#
#--------------------------------------

from gpiozero import Button
from subprocess import check_call
from signal import pause

# Define GPIO number
myGPIO=22

# Define number of seconds button should be pressed
myHoldTime=6

def buttonHeld():
  print("Button pressed for "+ str(myHoldTime) +" seconds")
  check_call(['sudo', 'poweroff'])

# Create a button object and define what function is
# run when it is held down for the hold_time
button=Button(myGPIO,pull_up=False,hold_time=myHoldTime)
button.when_held=buttonHeld

pause ()
