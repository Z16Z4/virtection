import shutil
import time
from termcolor import colored
import os
import sys
import re
import subprocess
from ctypes import *
from psutil import virtual_memory
import psutil

wait = input("press enter to start")
if os.name == "nt":
    import winreg

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
        print(type+ colored(": Detected", 'red'))
    else:
        #'virtual machine not detected
        print(type + colored(": Passed", 'green'))
    #debugging
    #print("debug info " + colored(queryresult, 'yellow'))

def registryindex(registry, string, type):
    #accessing registry through init HKEY
    access_registry = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
    #opening registry 
    for i in range(1028):
        try:
            #results based on directory names
            access_key = winreg.OpenKey(access_registry,registry)
            x =winreg.EnumKey(access_key,i)
            if x == string:
                print(type+ colored(": Detected", 'red'))
        except:
            break
def process_exists(process_name):
    progs = str(subprocess.check_output('tasklist'))
    if process_name in progs:
        return True
    else:
        return False
    #debugging
    #print("debug info " + colored(x, 'yellow'))
if os.name == "nt":
    a = 'null'
    registrysearch(r"SYSTEM\HardwareConfig", "BIOSVendor", a, "Development Kit", "BIOS Vendor")
    registrysearch(r"SYSTEM\HardwareConfig", "BIOSVendor", a, "OVMF", "OVMF Check")
    registrysearch(r"SYSTEM\HardwareConfig", "SystemProductName", a, "Q35", "SystemProductName")
    registrysearch(r"SYSTEM\HardwareConfig", "SystemVersion", a, "pc-q35", "SystemVersion")
    registryindex(r"SOFTWARE\WOW6432Node\RedHat", "RHEL", "RedHat check: ")
    registrysearch(r"SYSTEM\DriverDatabase\DriverPackages", "Provider", a, "Red Hat", "RedHat check")
    ##registryindex(r"SYSTEM\DriverDatabase\DriverPackages", "virtdisk", "RedHat Driver Check(1)")
    #memory amount
    mem = virtual_memory()
    GB = 1073741824
    #dividing bytes to get Gigabyte
    memory = int(mem.total / GB)
    #if gigabyte below 4
    if memory < 4:
        print("RAMCheck " + colored("is less than 4GB", 'red'))
    else:
        #if higher probably not default virtual setting
        print("RAMCheck " + colored("is higher than 4GB", 'green'))
        #memory to string
    memory =''.join(str(memory))
    #debug
    #print(memory + "GB Detected")
    #store usages
    usage = shutil.disk_usage("C:\\")
    #only want full disk size
    disk_total =int(usage[0] / GB)
    #if the disk size is below 50gb probably default virtual setting
    if disk_total < 50:
        print("DiskTotal " + colored(" less than ", 'red') + "50GB")
    else:
        print("DiskTotal: " + colored(" more than ", 'green') + "50GB")
    #convert to string
    disk_total =''.join(str(disk_total))
    #print(disk_total + "GB: " + colored("Detected", 'yellow'))
    #running powershell command to detect hypervisor method#1
    result = subprocess.check_output("powershell.exe (gcim Win32_ComputerSystem).HypervisorPresent", shell=True)
    #converting to string
    result =''.join(str(result))
    #replace uneeded text in string
    result = result.replace("b'", "")
    result = result.replace("\\r\\n'", "")
    if result == "True":
        print("Hypervisor " + colored("Detected", 'red'))
        #importing c library
    time.sleep(10)
    print('-------------------')
    print(colored('Direct CPU Clock Access ', 'yellow'))
    rdtsc_c = CDLL("./rdtsc.so")
    #running rdtsc.c as c library from import
    rdtsc_c.execute()
    print('\n-------------------')
    print('\n---Process check---')
    processes  = ["qemu-ga.exe", "xenservice.exe", "prl_tools.exe", "prl_cc.exe", "vmusrvc.exe", "vmsrvc.exe", "vmacthlp.exe", "VGAuthService.exe", "vmwareuser", "vmwaretray.exe","vmtoolsd.exe","vboxtray.exe", "vboxservice.exe"]
    count = 0
    while count < len(processes):
        if process_exists(processes[count]):
            print("Process " + processes[count] + colored(": Detected", 'red'))
        else:
            print("Process " + processes[count] + colored(": Passed" , 'green'))
        count += 1
    path = 'C:\Windows\System32\drivers'
    files = os.listdir(path)
    drivers = ["VBoxMouse.sys", "VBoxGuest.sys", "VBoxSF.sys", "VBoxVideo.sys", "vboxdisp.dll", "vboxhook.dll", 
    "vboxmrxnp.dll", "vboxogl.dll", "vboxoglarrayspu.dll", 
    "vboxoglcrutil.dll", "vboxoglerrorspu.dll", "vboxoglfeedbackspu.dll", 
    "vboxoglpackspu.dll", "vboxoglpassthroughspu.dll", "vboxservice.exe", "vboxtray.exe", "VBoxControl.exe" ,
    "vmmouse.sys", "vmhgfs.sys", "vm3dmp.sys", "vmci.sys","mhgfs.sys", "vmmemctl.sys", "vmmouse.sys", "vmrawdsk.sys",
    "vmusbmouse.sys", "NdisVirtualBus.sys"]
    print('\n---Drivers check---')
    for f in files:
        for dll in drivers:
            if f == dll:
                print("Driver " + dll + colored(": Detected", 'red'))

    pause = input("\npress enter to close..")
else:
    print("I am In Linux")
    rdtsc_c = CDLL("./rdtsc.so")
    rdtsc_c.execute()
#TODO detect cpuid for hypervisor id
#TODO check number of processes on VM 
#TODO Detection for virtualbox and vmware
#TODO DECTECTING CPUIDS print(cpuid.cpu_vendor())
#TODO detect files related to virtualisation 
