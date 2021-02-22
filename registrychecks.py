import winreg
from termcolor import colored
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
        print(type + ": Passed")
    #debugging
    print(colored("debug info" + queryresult, 'green'))

def registryindex(registry, string, type):
    #accessing registry through init HKEY
    access_registry = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
    #opening registry 
    access_key = winreg.OpenKey(access_registry,registry)
    for i in range(20):
        try:
            #results based on directory names
            x =winreg.EnumKey(access_key,i)
            if x == string:
                print(colored(type+ ": Detected", 'red'))
            else:
                print(type+ ": Passed")
        except:
            break
    #debugging
    print(colored("debug info " + x, 'green'))

a = 'null'
registrysearch(r"SYSTEM\HardwareConfig", "BIOSVendor", a, "Development Kit", "OVMF Check(0)")
registrysearch(r"SYSTEM\HardwareConfig", "BIOSVendor", a, "OVMF", "OVMF Check(1)")
registrysearch(r"SYSTEM\HardwareConfig", "SystemProductName", a, "Q35", "O35 Check(0)")
registrysearch(r"SYSTEM\HardwareConfig", "SystemVersion", a, "pc-q35", "Q35 Check(1)")
registryindex(r"SOFTWARE\WOW6432Node\RedHat", "RHEL", "RedHat Check(0)")
