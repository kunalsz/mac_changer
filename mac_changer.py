"""
Media Access Control

how to change in kali:
ifconfig eth0 down : to disable it
ifconfig eth0 hw ether _new_mac_address_ : change the mac adress to new , should be 12 characs long
ifconfig eth0 up : to enable it

#subprocess library
used to execute sys commands thru python
subprocess.call('command',Shell=true)
It runs the process in foreground, and doesnt move fwd until this process is completed
"""

import subprocess
import optparse
import re
import random
import time

#func to get args from the command line
def get_args():
    parser = optparse.OptionParser() #make an object to handle command line args
    parser.add_option('-i','--interface',dest = "interface",help='Select the interface') # make options 
    parser.add_option('-m','--mac',dest = "new_mac",help='Type the new mac address') # make options 
    parser.add_option('-r','--random',dest='randomize',action='store_const',const=True,help='Creates a random mac') #make random mac addresses just -r flag no args needed

    (options,args) =  parser.parse_args() # returns the input

    #handling if flags not specified
    if not options.interface:
        parser.error('Specify the interface --help for help')
    elif not (options.new_mac or options.randomize):
        parser.error('Specify the new mac address or choose randomize --help for help')
    return options

#subprocess.call('ipconfig',shell=True)
options = get_args()

#random_mac generator
def random_mac():
    predefine = '0123456789abcdef'
    new_mac = ''

    for i in range(12):
        new_mac = new_mac + random.choice(predefine)
        if i%2 != 0 and len(new_mac) <= 16: #adding colon
            new_mac = new_mac + ':'
    even = random.choice('02468ace') #making the second digit even
    new_mac = new_mac[0] + even + new_mac[2:]
    return new_mac

#main function
def mac_changer():
    old_mac = str(subprocess.check_output(['ifconfig',options.interface])) #get the old mac
    old_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",old_mac)

    subprocess.call(f'ifconfig {options.interface} down',shell=True) 

    #conditions to apply
    if options.randomize:
        new_mac = random_mac()
        subprocess.call(f'ifconfig {options.interface} hw ether {new_mac}',shell=True)#assign a random mac address
    else:
        #change the mac
        subprocess.call(f'ifconfig {options.interface} hw ether {options.new_mac}',shell=True)#assign the specified mac address
    
    subprocess.call(f'ifconfig {options.interface} up',shell=True)

    ifconfig_result = str(subprocess.check_output(['ifconfig',options.interface])) #returns the ouput of the execution
    mac_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_result)
    #print(mac_result.group(0))
    print(f'Mac address changed from {old_mac.group(0)} to {mac_result.group(0)}')


while True:
    time.sleep(60) #changes mac in every 60 secs 
    try:
        mac_changer()
    except:
        pass


