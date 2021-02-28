import os, subprocess, shutil, display, registry, platform
from ctypes import *
from psutil import virtual_memory

#Windows Functions

#Hypervisor check
def hypervisor_check():
    display.seperator("Hypervisor check")
    result = subprocess.check_output("powershell.exe (gcim Win32_ComputerSystem).HypervisorPresent", shell=True)
    result =''.join(str(result))
    result = result.replace("b'", "")
    result = result.replace("\\r\\n'", "")
    if result == "True":
        print("Hypervisor " + display.detected())
    else:
        print("Hypervisor " + display.undetected())

#Memory check
def memory_check():
    display.seperator("Memory check")
    mem = virtual_memory()
    GB = 1073741824
    memory = int(mem.total / GB)
    if memory < 4:
        print("RAM less than 4gb " + display.detected())
    else:
        print("RAM more than 4gb " + display.undetected())

#Disk check
def disk_check():
    display.seperator("Disk check")
    usage = shutil.disk_usage("C:\\")
    GB = 1073741824
    disk_total =int(usage[0] / GB)
    if disk_total < 50:
        print("Disk total less than 50gb " + display.detected())
    else:
        print("Disk total more than 50gb " + display.undetected())

#RDSTC check
def rdstc_check():
    display.seperator("RDSTC check")
    rdtsc_c = CDLL("./rdtsc.so")
    rdtsc_c.execute()


#Process exists check
def process_exists(process_name):
    progs = str(subprocess.check_output('tasklist'))
    if process_name in progs:
        return True
    else:
        return False


#process running check
def process_check():
    display.seperator("Process check")
    processes  = [
        "qemu-ga.exe",
        "xenservice.exe",
        "prl_tools.exe",
        "prl_cc.exe",
        "vmusrvc.exe",
        "vmsrvc.exe",
        "vmacthlp.exe",
        "VGAuthService.exe",
        "vmwareuser",
        "vmwaretray.exe",
        "vmtoolsd.exe",
        "vboxtray.exe",
        "vboxservice.exe"]
    count = 0
    print("\n")
    while count < len(processes):
        if process_exists(processes[count]):
            print("Process " + processes[count] + " " + display.detected())
        else:
            print("Process " + processes[count] + " " + display.undetected())

        count += 1


#registry check
def registry_check():
    display.seperator("Registry check")
    a = 'null'
    registry.search(r"SYSTEM\HardwareConfig", "BIOSVendor", a, "Development Kit", "BIOS Vendor")
    registry.search(r"SYSTEM\HardwareConfig", "BIOSVendor", a, "OVMF", "OVMF Check")
    registry.search(r"SYSTEM\HardwareConfig", "SystemProductName", a, "Q35", "SystemProductName")
    registry.search(r"SYSTEM\HardwareConfig", "SystemVersion", a, "pc-q35", "SystemVersion")
    registry.search(r"SYSTEM\HardwareConfig", "SystemProductName", a, "VirtualBox", "VirtualBox?")
    registry.search(r"SYSTEM\HardwareConfig", "SystemFamily", a, "Virtual Machine", "Virtual Machine")
    registry.search(r"SYSTEM\HardwareConfig", "SystemBiosVersion", a, "VBOX", "VirtualBox?")
    registry.search(r"SYSTEM\HardwareConfig", "BaseBoardManufacturer", a, "Oracle Corporation", "Oracle check")
    registry.search(r"SYSTEM\HardwareConfig", "BaseBoardProduct", a, "VirtualBox", "VirtualBox?")
    registry.index(r"SOFTWARE\WOW6432Node\RedHat", "RHEL", "RedHat check: ")
    registry.search(r"SYSTEM\DriverDatabase\DriverPackages", "Provider", a, "Red Hat", "RedHat check")

#guest additions check
def guest_additions_check():
    display.seperator("Guest Additions check")
    ga_drive = r"D:\\"
    guest_additions = [
        "VboxDarwinAdditions.pkg",
        "VboxDarwinAdditionsUninstall.tool",
        "VboxLinuxAdditions.run",
        "VboxSolarisAdditions.pkg",
        "VboxWindowsAdditions.exe",
        "VboxWindowsAdditions-x86.exe",
        "VboxWindowsAdditions-amd64.exe"]
    guest_additions_dir = os.listdir(ga_drive)
    for guestaddition in guest_additions_dir:
        for found_ga in guest_additions:
            if guestaddition == found_ga:
                print("GuestAddition file " + found_ga + " " + display.detected())

#driver check
def driver_check():
    display.seperator("Driver check")
    driver_path = r"C:\Windows\System32\drivers"
    files = os.listdir(driver_path)
    drivers = [
        "VBoxMouse.sys",
        "VBoxGuest.sys",
        "VBoxSF.sys",
        "VBoxVideo.sys",
        "vboxdisp.dll",
        "vboxhook.dll",
        "vboxmrxnp.dll",
        "vboxogl.dll",
        "vboxoglarrayspu.dll",
        "vboxoglcrutil.dll",
        "vboxoglerrorspu.dll",
        "vboxoglfeedbackspu.dll",
        "vboxoglpackspu.dll",
        "vboxoglpassthroughspu.dll",
        "VBoxService.exe",
        "VBoxTray.exe",
        "VBoxControl.exe",
        "vmmouse.sys",
        "vmhgfs.sys",
        "vm3dmp.sys",
        "vmci.sys",
        "mhgfs.sys",
        "vmmemctl.sys",
        "vmmouse.sys",
        "vmrawdsk.sys",
        "vmusbmouse.sys",]
    for f in files:
        for dll in drivers:
            if f == dll:
                print("Driver " + dll + " " + display.detected())
def username_check():
    #Testing for default usernames within a windows Virtual machine
    display.seperator("Username check")
    usernames = ["zeus", 'test']
    print("actual username " + " " + os.getlogin())
    for names in usernames:
        if names == os.getlogin():
            print(names + ' ' + display.detected())
        else:
            print(names +  ' ' + display.undetected())

def hostname_check():
    display.seperator("Hostname check")
    hostname = os.environ['userdomain']
    hostnames = ["vmware", "virtualbox", "test", "vm", "virtual_machine"]
    for possible_name in hostnames:
        if possible_name == hostname:
            print(possible_name + " " + display.detected())
        else:
            print(possible_name + " " + display.undetected())