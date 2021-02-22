import winreg
import shutil
from termcolor import colored
import os
import re
import subprocess
import time
from psutil import virtual_memory
#function used to do search queries in windows registry 
def registrysearch(registry, query, queryresult, string, type):
    #accessing registry through init HKEY
    access_registry = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
    #opening registry 
    access_key = winreg.OpenKey(access_registry,registry)
    for i in range(20):
        try:
            #results based on registry keys
            asubkey_name=winreg.EnumKey(access_key,i)
            asubkey=winreg.OpenKey(access_key, asubkey_name)
            #searching all queries
            queryresult = winreg.QueryValueEx(asubkey, query)
        except:
            break
    #converting query output to string
    queryresult =''.join(str(queryresult))
    #checking query against possible keywords
    if string in queryresult:
        #virtual machine detected
        print(colored(type+ ": Detected", 'red'))
    else:
        #'virtual machine not detected
        print(colored(type + ": Passed", 'green'))
    #debugging
    print(colored("debug info" + queryresult, 'yellow'))

def registryindex(registry, string, type):
    #accessing registry through init HKEY
    access_registry = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
    #opening registry 
    access_key = winreg.OpenKey(access_registry,registry)
    for i in range(1028):
        try:
            #results based on directory names
            x =winreg.EnumKey(access_key,i)
            if x == string:
                print(colored(type+ ": Detected", 'red'))
        except:
            break
    #debugging
    print(colored("debug info " + x, 'yellow'))

a = 'null'
registrysearch(r"SYSTEM\HardwareConfig", "BIOSVendor", a, "Development Kit", "OVMF Check(0)")
registrysearch(r"SYSTEM\HardwareConfig", "BIOSVendor", a, "OVMF", "OVMF Check(1)")
registrysearch(r"SYSTEM\HardwareConfig", "SystemProductName", a, "Q35", "O35 Check(0)")
registrysearch(r"SYSTEM\HardwareConfig", "SystemVersion", a, "pc-q35", "Q35 Check(1)")
registryindex(r"SOFTWARE\WOW6432Node\RedHat", "RHEL", "RedHat Check(0)")
registrysearch(r"SYSTEM\DriverDatabase\DriverPackages", "Provider", a, "Red Hat", "RedHat Check (1)")
##registryindex(r"SYSTEM\DriverDatabase\DriverPackages", "virtdisk", "RedHat Driver Check(1)")
#TODO add virtualbox and vmware registry checks here
#memory amount
mem = virtual_memory()
GB = 1073741824
#dividing bytes to get Gigabyte
memory = int(mem.total / GB)
#if gigabyte below 4
if memory < 4:
    print(colored("RAM is less than 4GB probably a virtual machine", 'red'))
else:
    #if higher probably not default virtual setting
    print(colored("RAM is higher than 4 most likely a real machine", 'green'))
#memory to string
memory =''.join(str(memory))
#debug
print(colored(memory + "GB Detected", 'yellow'))
#store usages
usage = shutil.disk_usage("C:\\")
#only want full disk size
disk_total =int(usage[0] / GB)
#if the disk size is below 50gb probably default virtual setting
if disk_total < 50:
    print(colored("disk total is lower than 50GB", 'red'))
else:
    print(colored("disk total is higher than 50GB", 'green'))
#convert to string
disk_total =''.join(str(disk_total))
print(colored(disk_total + "GB Detected", 'yellow'))
#running powershell command to detect hypervisor method#1
result = subprocess.check_output("powershell.exe (gcim Win32_ComputerSystem).HypervisorPresent", shell=True)
#converting to string
result =''.join(str(result))
#replace uneeded text in string
result = result.replace("b'", "")
result = result.replace("\\r\\n'", "")
if result == "True":
    print(colored("Hypervisor detected", 'red'))


#TODO detect cpu rdtscp Frequency for timestamp detection and vm exit
# TODO detect cpuid for hypervisor id
#TODO check number of processes on VM 
#Detection for virtualbox and vmware
