import winreg

#function used to do search queries in windows registry 
def registrysearch(registry, query, queryresult, string, type):
    #accessing registry through init HKEY
    access_registry = winreg.ConnectRegistry(None,winreg.HKEY_LOCAL_MACHINE)
    #opening registry 
    access_key = winreg.OpenKey(access_registry,registry)
    for i in range(20):
        try:
            #subkey of registry, subname 
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
        print(type + ": Failed")
    else:
        #'virtual machine not detected
        print(type + ": Success")
    #debugging
    print("debug info" + queryresult)

#registrysearch(REGISTRY__PATH, REGISTRYNAME, NULL, SEARCH QUERY, TYPE OF CHECK)
registrysearch(r"SYSTEM\HardwareConfig", "BIOSVendor", "null", "Development Kit", "OVMF Check(0)")
registrysearch(r"SYSTEM\HardwareConfig", "BIOSVendor", "null", "OVMF", "OVMF Check(1)")
registrysearch(r"SYSTEM\HardwareConfig", "SystemProductName", "null", "Q35", "O35 Check(0)")
registrysearch(r"SYSTEM\HardwareConfig", "SystemVersion", "null", "pc-q35", "Q35 Check(1)")
