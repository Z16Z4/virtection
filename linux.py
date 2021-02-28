import display, shutil, os
from psutil import virtual_memory
#Linux Functions
def apply_patches():
    display.seperator("Applying patches...")
    #build kernal and test patches first, important
    #fileinput, edit kernal and add modifications 
    #build kernal need system detection incase build kernal commands differ
    #host windows iso for download for kvm 
    #xml host configuration can be copied, options to enter in settings
    #possible gpu passthrough function, using identical gpu method for automation (can only do on arch)
    #documentation of implementation on dynamic analysis platform


def guest_check():
    display.seperator("Guest or Host check")
    host_system = 0
    guest_system = 0
    gorh = input("guest or host? (host/guest): ")
    if gorh == 'host':
        host_system = 1
        patches_y_n = input("apply rdstc patches? (y/n)")
        if patches_y_n == 'y':
            apply_patches()
            return host_system
        else:
            print("failed to apply patches")
            return host_system
    elif gorh == "guest":
        guest_system = 1
        return guest_system

def memory_check():
    display.seperator("Memory check")
    mem = virtual_memory()
    GB = 1073741824
    memory = int(mem.total / GB)
    if memory < 4:
        print("RAM less than 4gb " + display.detected())
    else:
        print("RAM more than 4gb " + display.undetected())

def disk_check():
    display.seperator("Disk check")
    usage = shutil.disk_usage("/")
    GB = 1073741824
    disk_total =int(usage[0] / GB)
    if disk_total < 50:
        print("Disk total less than 50gb " + display.detected())
    else:
        print("Disk total more than 50gb " + display.undetected())

def docker_check():
    display.seperator("Docker check")
    if os.path.isfile('/.dockerenv'):
        print("Docker-container (env) " + " " +display.detected())
    else:
        print("Docker-container (env) " + " " +display.undetected())
    if os.path.isfile('/etc/default/grub'):
        print("Docker-container (grub) " + " " +display.undetected())
    else:
        print("Docker-container (grub) " + " " +display.detected())

def basic_vm_check():
    #checks vmware/virtualbox 
    #includes information about memory and product
    #TODO implement system detection on linux
    dmidecode = 'sudo apt-get install dmidecode -y || sudo pacman -S dmidecode -y &&'
    os.system("sudo apt-get install dmidecode || sudo pacman -S dmidecode")
    productids = os.system("dmidecode  | grep -i product")
    print(productids)
