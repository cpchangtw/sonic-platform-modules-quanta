#!/usr/bin/env python
#
# Copyright (C) 2018 Quanta Computer Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Usage: %(scriptName)s [options] command object

options:
    -h | --help     : this help message
    -d | --debug    : run with debug mode
    -f | --force    : ignore error during installation or clean 
command:
    install     : install drivers and generate related sysfs nodes
    clean       : uninstall drivers and remove related sysfs nodes    
"""

import os
import commands
import sys, getopt
import logging
import re
import time
from collections import namedtuple

DEBUG = False
args = []
FORCE = 0
i2c_prefix = '/sys/bus/i2c/devices/'


if DEBUG == True:
    print sys.argv[0]
    print 'ARGV      :', sys.argv[1:]   


def main():
    global DEBUG
    global args
    global FORCE
        
    if len(sys.argv)<2:
        show_help()
         
    options, args = getopt.getopt(sys.argv[1:], 'hdf', ['help',
                                                       'debug',
                                                       'force',
                                                          ])
    if DEBUG == True:                                                           
        print options
        print args
        print len(sys.argv)
            
    for opt, arg in options:
        if opt in ('-h', '--help'):
            show_help()
        elif opt in ('-d', '--debug'):            
            DEBUG = True
            logging.basicConfig(level=logging.INFO)
        elif opt in ('-f', '--force'): 
            FORCE = 1
        else:
            logging.info('no option')                          
    for arg in args:            
        if arg == 'install':
           install()
        elif arg == 'clean':
           uninstall()
        else:
            show_help()
            
            
    return 0              

def show_help():
    print __doc__ % {'scriptName' : sys.argv[0].split("/")[-1]}
    sys.exit(0)
           
def show_log(txt):
    if DEBUG == True:
        print "[IX2-56X]"+txt
    return

def exec_cmd(cmd, show):
    logging.info('Run :'+cmd)  
    status, output = commands.getstatusoutput(cmd)    
    show_log (cmd +"with result:" + str(status))
    show_log ("      output:"+output)    
    if status:
        logging.info('Failed :'+cmd)
        if show:
            print('Failed :'+cmd)
    return  status, output

instantiate =[
# Expose PSOC that behind PCA9641
'i2cset -y 0 0x8 0x5 0xfb',
'i2cset -y 0 0x8 0x1 0x5',
# Turn on module power
'echo 37 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio37/direction',
'echo 1 >/sys/class/gpio/gpio37/value',
# Export pca9698 for qsfp present
'echo 82 > /sys/class/gpio/export',
'echo in > /sys/class/gpio/gpio82/direction',
'echo 86 > /sys/class/gpio/export',
'echo in > /sys/class/gpio/gpio86/direction',
'echo 90 > /sys/class/gpio/export',
'echo in > /sys/class/gpio/gpio90/direction',
'echo 94 > /sys/class/gpio/export',
'echo in > /sys/class/gpio/gpio94/direction',
'echo 98 > /sys/class/gpio/export',
'echo in > /sys/class/gpio/gpio98/direction',
'echo 102 > /sys/class/gpio/export',
'echo in > /sys/class/gpio/gpio102/direction',
'echo 106 > /sys/class/gpio/export',
'echo in > /sys/class/gpio/gpio106/direction',
'echo 110 > /sys/class/gpio/export',
'echo in > /sys/class/gpio/gpio110/direction',
# Export pca9698 for qsfp reset
'echo 80 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio80/direction',
'echo 1 >/sys/class/gpio/gpio80/value',
'echo 84 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio84/direction',
'echo 1 >/sys/class/gpio/gpio84/value',
'echo 88 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio88/direction',
'echo 1 >/sys/class/gpio/gpio88/value',
'echo 92 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio92/direction',
'echo 1 >/sys/class/gpio/gpio92/value',
'echo 96 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio96/direction',
'echo 1 >/sys/class/gpio/gpio96/value',
'echo 100 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio100/direction',
'echo 1 >/sys/class/gpio/gpio100/value',
'echo 104 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio104/direction',
'echo 1 >/sys/class/gpio/gpio104/value',
'echo 108 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio108/direction',
'echo 1 >/sys/class/gpio/gpio108/value',
# Export pca9698 for qsfp lpmode
'echo 83 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio83/direction',
'echo 0 >/sys/class/gpio/gpio83/value',
'echo 87 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio87/direction',
'echo 0 >/sys/class/gpio/gpio87/value',
'echo 91 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio91/direction',
'echo 0 >/sys/class/gpio/gpio91/value',
'echo 95 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio95/direction',
'echo 0 >/sys/class/gpio/gpio95/value',
'echo 99 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio99/direction',
'echo 0 >/sys/class/gpio/gpio99/value',
'echo 103 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio103/direction',
'echo 0 >/sys/class/gpio/gpio103/value',
'echo 107 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio107/direction',
'echo 0 >/sys/class/gpio/gpio107/value',
'echo 111 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio111/direction',
'echo 0 >/sys/class/gpio/gpio111/value',
# export GPIO of CPLD-LED
'echo 65 > /sys/class/gpio/export',
'echo out > /sys/class/gpio/gpio65/direction',
'echo 1 >/sys/class/gpio/gpio65/value',
# SFP28 Module TxEnable
'echo 0 > /sys/class/cpld-sfp28/port-1/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-2/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-3/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-4/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-5/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-6/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-7/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-8/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-9/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-10/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-11/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-12/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-13/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-14/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-15/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-16/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-17/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-18/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-19/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-20/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-21/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-22/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-23/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-24/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-25/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-26/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-27/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-28/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-29/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-30/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-31/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-32/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-33/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-34/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-35/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-36/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-37/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-38/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-39/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-40/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-41/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-42/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-43/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-44/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-45/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-46/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-47/tx_dis',
'echo 0 > /sys/class/cpld-sfp28/port-48/tx_dis',
]

drivers =[
'lpc_ich',
'i2c-i801',
'i2c-dev',
'i2c-mux-pca954x',
'gpio-pca953x',
'qci_pmbus',
'leds-gpio',
'qci_cpld_sfp28',
'quanta_hwmon_ix_series',
'quanta_platform_ix2'
]
 

                    
def system_install():
    global FORCE
	
    #remove default drivers to avoid modprobe order conflicts
    status, output = exec_cmd("rmmod i2c_ismt ", 1)
    status, output = exec_cmd("rmmod i2c-i801 ", 1)
    #setup driver dependency
    status, output = exec_cmd("depmod -a ", 1)
    #install drivers
    for i in range(0,len(drivers)):
       status, output = exec_cmd("modprobe "+drivers[i], 1)
    if status:
	   print output
	   if FORCE == 0:                
	      return status             
    				 
    #instantiate devices
    for i in range(0,len(instantiate)):
       #time.sleep(1)
       status, output = exec_cmd(instantiate[i], 1)
    if status:
	   print output
	   if FORCE == 0:                
	      return status   
    
    #for i in range(22,30):
    #    status, output =exec_cmd("echo sff8436 0x50 > /sys/bus/i2c/devices/i2c-0/i2c-4/i2c-"+str(i)+"/new_device", 1)
    #    if status:
    #        print output
    #        if FORCE == 0:            
    #            return status   
    
    return 
     
        
def system_ready():
    if not device_found(): 
        return False
    return True
               
def install():                      
    if not device_found():
        print "No device, installing...."     
        status = system_install() 
        if status:
            if FORCE == 0:        
                return  status        
    else:
        print " ix2 driver already installed...."
    return

def uninstall():
    global FORCE
    #uninstall drivers
    for i in range(len(drivers)-1,-1,-1):
       status, output = exec_cmd("rmmod "+drivers[i], 1)
    if status:
	   print output
	   if FORCE == 0:                
	      return status
    return

def device_found():
    ret1, log = exec_cmd("ls "+i2c_prefix+"i2c-0", 0)
    return ret1				

if __name__ == "__main__":
    main()



